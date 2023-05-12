import datetime
import functools
import os
import re
from pathlib import Path
from typing import Optional

from components.performer_helpers import (
    apply_performers_exclude_genders,
    apply_performers_limit,
    apply_performers_order_by,
)
from components.studio_helpers import (
    get_parent_studio,
    get_studio_family,
    get_studio_hierarchy,
)
from models.config import FileNameConfig, PerformersConfig
from models.scene import Scene, SceneFile, ScenePerformer, SceneTag
from models.studio import Studio
from models.template_variables_config import TemplateVariablesConfig

OS_PATH_SEPARATOR = os.path.sep


def fill_template_file_name(
    template: str,
    scene: Scene,
    studios: list[Studio],
    file: SceneFile,
    template_variables_config: TemplateVariablesConfig,
):
    return fill_template(template, scene, studios, file, template_variables_config)


def fill_template_file_dir(
    template: str,
    scene: Scene,
    studios: list[Studio],
    file: SceneFile,
    template_variables_config: TemplateVariablesConfig,
):
    return fill_template(template, scene, studios, file, template_variables_config)


def fill_template(
    template: str,
    scene: Scene,
    studios: list[Studio],
    file: SceneFile,
    template_variables_config: TemplateVariablesConfig,
) -> str:
    """Fill the template with the scene and studio data"""

    replacers = {
        "{title}": create_title_replacer(scene.title),
        "{studio}": create_studio_replacer(scene.studio),
        "{parent_studio}": create_parent_studio_replacer(scene.studio, studios),
        "{studio_family}": create_studio_family_replacer(scene.studio, studios),
        "{performers}": create_performers_replacer(
            scene.performers,
            template_variables_config.PERFORMERS_CONFIG or PerformersConfig(),
        ),
        r"({date}|{date(?:\:.+?)})": create_date_replacer(scene.date),
        "{resolution}": create_resolution_replacer(file.resolution),
        "{resolution_name}": create_resolution_name_replacer(file.resolution_name),
        r"({duration}|{duration(?:\:.+?)})": create_duration_replacer(file.duration),
        "{bit_rate_mbps}": create_bit_rate_mbps_replacer(file.bit_rate_mbps),
        "{tags}": create_tags_replacer(scene.tags),
        "{video_codec}": create_video_codec_replacer(file.video_codec),
        "{audio_codec}": create_audio_codec_replacer(file.audio_codec),
        "{movie_scene_number}": create_movie_scene_number_replacer(
            scene.movie_scene_number
        ),
        "{movie_name}": create_movie_name_replacer(scene.movie_name),
        r"({movie_date}|{movie_date(?:\:.+?)})": create_movie_date_replacer(
            scene.movie_date
        ),
        "{scene_stash_id}": create_scene_stash_id_replacer(scene.stash_id),
        "{performers_stash_ids}": create_performers_stash_ids_replacer(
            scene.performers,
            template_variables_config.PERFORMERS_CONFIG or PerformersConfig(),
        ),
        "{studio_code}": create_studio_code_replacer(scene.studio_code),
        "{oshash}": create_oshash_replacer(file.oshash),
        "{phash}": create_phash_replacer(file.phash),
        "{src}": create_src_replacer(file.path),
        "{rating}": create_rating_replacer(scene.rating),
        "{studio_hierarchy}": create_studio_hierarchy_replacer(scene.studio, studios),
    }

    for template_var, replacer in replacers.items():
        template = re.sub(
            template_var,
            lambda match: replacer(match.group()),
            template,
        )

    # replace multiple white spaces with a single space
    template = re.sub(r"\s+", " ", template)
    # remove leading and trailing white spaces
    template = template.strip()

    return template


def sanitize_file_name(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)

        # use typewriter for Apostrophe
        text = re.sub("[’‘”“]+", "'", text)

        # remove illegal characters for Windows file names
        return re.sub(r'[<>:"/\\|?*]', "", text)

    return wrapper


def create_title_replacer(scene_title: Optional[str]):
    @sanitize_file_name
    def title_replacer(match_group: str):
        return scene_title or ""

    return title_replacer


def create_studio_replacer(scene_studio: Optional[Studio]):
    @sanitize_file_name
    def studio_replacer(match_group: str):
        if scene_studio is None:
            return ""
        return scene_studio.name

    return studio_replacer


def create_resolution_replacer(file_resolution: Optional[str]):
    @sanitize_file_name
    def resolution_replacer(match_group: str):
        return file_resolution or ""

    return resolution_replacer


def create_resolution_name_replacer(file_resolution_name: Optional[str]):
    @sanitize_file_name
    def resolution_name_replacer(match_group: str):
        return file_resolution_name or ""

    return resolution_name_replacer


def create_performers_replacer(
    performers: Optional[list[ScenePerformer]], performers_config: PerformersConfig
):
    @sanitize_file_name
    def performers_replacer(match_group: str):
        if performers is None or len(performers) == 0:
            return performers_config.NO_PERFORMER_NAME or ""

        new_performers = performers
        new_performers = apply_performers_exclude_genders(
            new_performers, performers_config.EXCLUDE_GENDERS
        )
        new_performers = apply_performers_order_by(
            new_performers, performers_config.ORDER_BY
        )
        new_performers = apply_performers_limit(new_performers, performers_config.LIMIT)

        performers_str = performers_config.SEPARATOR.join(
            [performer.name for performer in new_performers]
        )

        return performers_str

    return performers_replacer


def create_date_replacer(scene_date: Optional[datetime.date]):
    @sanitize_file_name
    def date_replacer(match_group: str):
        if scene_date is None:
            return ""

        if re.match(r"{date}", match_group):
            return scene_date.isoformat()

        if match := re.match(r"{date:(.+?)}", match_group):
            date_format = match.group(1)
            return scene_date.strftime(date_format)

        return ""

    return date_replacer


def create_oshash_replacer(file_oshash: Optional[str]):
    @sanitize_file_name
    def oshash_replacer(match_group: str):
        return file_oshash or ""

    return oshash_replacer


def create_phash_replacer(file_phash: Optional[str]):
    @sanitize_file_name
    def phash_replacer(match_group: str):
        return file_phash or ""

    return phash_replacer


def create_duration_replacer(file_duration: Optional[datetime.time]):
    @sanitize_file_name
    def duration_replacer(match_group: str):
        if file_duration is None:
            return ""

        if re.match(r"{duration}", match_group):
            return file_duration.strftime("%H.%M.%S")

        if match := re.match(r"{duration:(.+?)}", match_group):
            duration_format = match.group(1)
            return file_duration.strftime(duration_format)

        return ""

    return duration_replacer


def create_bit_rate_mbps_replacer(file_bit_rate_mbps: Optional[str]):
    @sanitize_file_name
    def bit_rate_mbps_replacer(match_group: str):
        return file_bit_rate_mbps or ""

    return bit_rate_mbps_replacer


def create_parent_studio_replacer(studio: Optional[Studio], studios: list[Studio]):
    @sanitize_file_name
    def parent_studio_replacer(match_group: str):
        if studio is None:
            return ""
        return get_parent_studio(studio, studios).name

    return parent_studio_replacer


def create_studio_family_replacer(studio: Optional[Studio], studios: list[Studio]):
    @sanitize_file_name
    def studio_family_replacer(match_group: str):
        if studio is None:
            return ""
        return get_studio_family(studio, studios).name

    return studio_family_replacer


def create_rating_replacer(scene_rating: Optional[int]):
    @sanitize_file_name
    def rating_replacer(match_group: str):
        return str(scene_rating) or ""

    return rating_replacer


def create_tags_replacer(scene_tags: Optional[list[SceneTag]]):
    @sanitize_file_name
    def tags_replacer(match_group: str):
        if scene_tags is None:
            return ""

        return ", ".join([tag.name for tag in scene_tags])

    return tags_replacer


def create_video_codec_replacer(file_video_codec: Optional[str]):
    @sanitize_file_name
    def video_codec_replacer(match_group: str):
        return file_video_codec or ""

    return video_codec_replacer


def create_audio_codec_replacer(file_audio_codec: Optional[str]):
    @sanitize_file_name
    def audio_codec_replacer(match_group: str):
        return file_audio_codec or ""

    return audio_codec_replacer


def create_movie_name_replacer(movie_name: Optional[str]):
    @sanitize_file_name
    def movie_name_replacer(match_group: str):
        return movie_name or ""

    return movie_name_replacer


def create_movie_date_replacer(movie_date: Optional[datetime.date]):
    @sanitize_file_name
    def movie_date_replacer(match_group: str):
        if movie_date is None:
            return ""

        if re.match(r"{movie_date}", match_group):
            return movie_date.isoformat()

        if match := re.match(r"{movie_date:(.+?)}", match_group):
            date_format = match.group(1)
            return movie_date.strftime(date_format)

        return ""

    return movie_date_replacer


def create_movie_scene_number_replacer(movie_scene_number: Optional[int]):
    @sanitize_file_name
    def movie_scene_number_replacer(match_group: str):
        return str(movie_scene_number) or ""

    return movie_scene_number_replacer


def create_scene_stash_id_replacer(scene_stash_id: Optional[str]):
    @sanitize_file_name
    def scene_stash_id_replacer(match_group: str):
        return scene_stash_id or ""

    return scene_stash_id_replacer


def create_studio_code_replacer(studio_code: Optional[str]):
    @sanitize_file_name
    def studio_code_replacer(match_group: str):
        return studio_code or ""

    return studio_code_replacer


def create_performers_stash_ids_replacer(
    performers: Optional[list[ScenePerformer]], performers_config: PerformersConfig
):
    @sanitize_file_name
    def performers_stash_ids_replacer(match_group: str):
        if performers is None or len(performers) == 0:
            return performers_config.NO_PERFORMER_NAME or ""

        new_performers = performers
        new_performers = apply_performers_exclude_genders(
            new_performers, performers_config.EXCLUDE_GENDERS
        )
        new_performers = apply_performers_order_by(
            new_performers, performers_config.ORDER_BY
        )
        new_performers = apply_performers_limit(new_performers, performers_config.LIMIT)

        performers_str = performers_config.SEPARATOR.join(
            [performer.stash_id or "" for performer in new_performers]
        )

        return performers_str

    return performers_stash_ids_replacer


def create_src_replacer(src: Optional[str]):
    def src_replacer(match_group: str):
        if not src:
            return ""

        return str(Path(src).parent) or ""

    return src_replacer


def create_studio_hierarchy_replacer(studio: Optional[Studio], studios: list[Studio]):
    def studio_hierarchy_replacer(match_group: str):
        if studio is None:
            return ""

        @sanitize_file_name
        def sanitize_studio_name(name: str):
            return name

        return OS_PATH_SEPARATOR.join(
            [
                sanitize_studio_name(studio.name)
                for studio in get_studio_hierarchy(studio, studios)
            ]
        )

    return studio_hierarchy_replacer
