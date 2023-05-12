import logging
from pathlib import Path
from typing import Optional

import components.setup_logging
from components.studio_helpers import contains_studio, find_studio_with_name
from models.config import FileDirTemplateConfig, FileNameTemplateConfig
from models.scene import Scene, SceneFile
from models.studio import Studio

logger = logging.getLogger(__name__)


def find_matching_template(
    scene: Scene,
    studios: list[Studio],
    file: SceneFile,
    template_configs: list[FileNameTemplateConfig] | list[FileDirTemplateConfig],
):
    for idx, template_config in enumerate(template_configs, 1):
        logger.debug("Checking TEMPLATE %d: '%s'", idx, template_config.TEMPLATE)
        if matches_template_config(
            scene=scene,
            studios=studios,
            file=file,
            template_config=template_config,
        ):
            return template_config.TEMPLATE

    return None


def matches_template_config(
    scene: Scene,
    studios: list[Studio],
    file: SceneFile,
    template_config: FileNameTemplateConfig | FileDirTemplateConfig,
):
    filter_funcs = [
        create_matches_studio_filter(template_config.matches_studio),
        create_matches_part_of_studio_filter(template_config.matches_part_of_studio),
        create_matches_all_tags_filter(template_config.matches_all_tags),
        create_matches_any_tags_filter(template_config.matches_any_tags),
        create_matches_organized_value_filter(template_config.matches_organized_value),
        create_matches_scene_with_no_performers_filter(
            template_config.matches_scene_with_no_performers
        ),
    ]

    filter_descriptions = [
        f'{{"matches_studio": "{template_config.matches_studio}"}}',
        f'{{"matches_part_of_studio": "{template_config.matches_part_of_studio}"}}',
        f'{{"matches_all_tags": "{template_config.matches_all_tags}"}}',
        f'{{"matches_any_tags": "{template_config.matches_any_tags}"}}',
        f'{{"matches_organized_value": "{template_config.matches_organized_value}"}}',
        f'{{"matches_scene_with_no_performers": "{template_config.matches_scene_with_no_performers}"}}',
    ]

    if type(template_config) == FileDirTemplateConfig:
        filter_funcs.append(
            create_matches_src_filter(template_config.matches_src),
        )
        filter_descriptions.append(
            f'{{"matches_src": "{template_config.matches_src}"}}'
        )

    for idx, filter_func in enumerate(filter_funcs):
        if not filter_func(scene=scene, studios=studios, file=file):
            logger.debug(
                f"Template Does Not Match. Failed Filter: %s", filter_descriptions[idx]
            )
            return False

    return True


def create_matches_studio_filter(filter_value: Optional[str]):
    def matches_studio_filter(scene: Scene, studios: list[Studio], file: SceneFile):
        if filter_value is None:
            return True

        # A scene with no studio will never match a studio filter
        if scene.studio is None:
            return False

        # Get the full studio object of the filter value (aka studio name)
        match_studio = find_studio_with_name(studio_name=filter_value, studios=studios)

        if match_studio is None:
            raise ValueError(
                f"Unknown studio name in matches_studio filter: {filter_value}"
            )

        return match_studio.id == scene.studio.id

    return matches_studio_filter


def create_matches_part_of_studio_filter(filter_value: Optional[str]):
    def matches_part_of_studio_filter(
        scene: Scene, studios: list[Studio], file: SceneFile
    ):
        if filter_value is None:
            return True

        # A scene with no studio will never match a studio filter
        if scene.studio is None:
            return False

        # If the filter value is empty, raise an error
        if not filter_value.strip():
            raise ValueError(
                f"Empty filter value in matches_part_of_studio filter: {filter_value}"
            )

        # Get the full studio object of the filter value (aka studio name)
        match_studio = find_studio_with_name(studio_name=filter_value, studios=studios)

        if match_studio is None:
            raise ValueError(
                f"Unknown studio name in matches_studio filter: {filter_value}"
            )

        return contains_studio(
            studio=scene.studio,
            target_studio_family=match_studio,
            studios=studios,
        )

    return matches_part_of_studio_filter


def create_matches_all_tags_filter(filter_value: Optional[list[str]]):
    def matches_all_tags_filter(scene: Scene, studios: list[Studio], file: SceneFile):
        if filter_value is None:
            return True

        # If there are no tags to filter, it's always a match
        if len(filter_value) == 0:
            return True

        # If the filter value is empty, it's never a match
        for filter_tag_name in filter_value:
            if not filter_tag_name.strip():
                raise ValueError(f"Empty tag name in matches_all_tags filter")

        scene_tag_names = [tag.name for tag in scene.tags]

        for filter_tag_name in filter_value:
            if filter_tag_name.strip() not in scene_tag_names:
                return False

        return True

    return matches_all_tags_filter


def create_matches_any_tags_filter(filter_value: Optional[list[str]]):
    def matches_any_tags_filter(scene: Scene, studios: list[Studio], file: SceneFile):
        if filter_value is None:
            return True

        # If there are no tags to filter, it's always a match
        if len(filter_value) == 0:
            return True

        # If the filter value is empty, it's never a match
        for filter_tag_name in filter_value:
            if not filter_tag_name.strip():
                raise ValueError(f"Empty tag name in matches_all_tags filter")

        scene_tag_names = [tag.name for tag in scene.tags]

        for filter_tag_name in filter_value:
            if filter_tag_name.strip() in scene_tag_names:
                return True

        return False

    return matches_any_tags_filter


def create_matches_organized_value_filter(filter_value: Optional[bool]):
    def matches_organized_value_filter(
        scene: Scene, studios: list[Studio], file: SceneFile
    ):
        if filter_value is None:
            return True

        return scene.organized == filter_value

    return matches_organized_value_filter


def create_matches_scene_with_no_performers_filter(filter_value: Optional[bool]):
    def matches_scene_with_no_performers_filter(
        scene: Scene, studios: list[Studio], file: SceneFile
    ):
        if filter_value is None:
            return True

        scene_has_no_performers = len(scene.performers) == 0

        return scene_has_no_performers == filter_value

    return matches_scene_with_no_performers_filter


def create_matches_src_filter(filter_value: Optional[str]):
    def matches_src_filter(scene: Scene, studios: list[Studio], file: SceneFile):
        if filter_value is None:
            return True

        return Path(file.path).is_relative_to(Path(filter_value))

    return matches_src_filter
