import datetime
import json
import logging
import os
import re
from pathlib import Path
from typing import Optional

import pathvalidate

from components.fill_template import fill_template_file_dir, fill_template_file_name
from components.find_matching_template import find_matching_template
from components.stash_db import StashDB
from components.stash_logger import StashLogger, get_stash_logger
from models.config import Config, FileNameConfig, PerformersConfig, get_config
from models.scene import Scene, SceneFile, ScenePerformer
from models.studio import Studio

logger = logging.getLogger(__name__)
stash_logger = get_stash_logger()

OS_PATH_SEPARATOR = os.path.sep


def process_scenes(scenes: list[Scene], studios: list[Studio]):
    """
    Renames files based on the scene, studio and config information
    """

    config = get_config()

    stash_db = StashDB(config.STASH_SQLITE_DATABASE_PATH, config.DRYRUN_ENABLED)

    stash_logger.progress(0)

    for idx, scene in enumerate(scenes):
        stash_logger.progress((idx + 1) / len(scenes))

        logger.info(f"--- Processing scene: (scene_id={scene.id}) {scene.title} ---")
        stash_logger.info(
            f"Change Processing scene: (scene_id={scene.id}) {scene.title}"
        )

        # Filter scenes without files
        if not scene.files:
            logger.info(f"[Skipping Scene] No files found for scene")
            stash_logger.info("[Skipping Scene] No files found for scene")
            continue

        for file in scene.files:
            logger.info("Processing src file: '%s'", file.path)
            stash_logger.info(
                f"Processing src file: '{file.path}'",
            )

            # Filter scenes without a matching file name template
            logger.debug("File Name Template - Searching for match...")
            file_name_template = find_matching_template(
                scene=scene,
                studios=studios,
                file=file,
                template_configs=config.FILE_NAME_CONFIG.FILE_NAME_TEMPLATES,
            )

            if file_name_template:
                logger.debug(
                    "File Name Template Found: '%s'",
                    file_name_template,
                )
            else:
                logger.info(f"[Skipping File] File Name Template Not Found")
                stash_logger.info(f"[Skipping File] File Name Template Not Found")
                continue

            # Filter scenes without a matching file dir template
            logger.debug("File Dir Template - Searching for match...")
            file_dir_template = find_matching_template(
                scene=scene,
                studios=studios,
                file=file,
                template_configs=config.FILE_DIR_CONFIG.FILE_DIR_TEMPLATES,
            )

            if file_dir_template:
                logger.debug("File Dir Template Found: '%s'", file_dir_template)
            else:
                logger.info(f"[Skipping File] File Dir Template Not Found")
                stash_logger.info(f"[Skipping File] File Dir Template Not Found")
                continue

            try:
                new_file_path = create_new_file_path(
                    scene, studios, file, config, file_name_template, file_dir_template
                )
            except FileExistsError as error:
                logger.info("[Skipping File] No changes to file path (in Stash DB)")
                stash_logger.info(
                    "[Skipping File] No changes to file path (in Stash DB)"
                )
                continue
            except FilePathTooLongError as error:
                logger.error(
                    "[Skipping File] New file path generated from templates is too long and could not be shortened: %s",
                    error.path,
                )
                stash_logger.error(
                    f"[Skipping File] New file path generated from templates is too long and could not be shortened: {error.path}",
                )
                continue

            try:
                rename(file.path, new_file_path)
            except Exception as error:
                logger.error("Failed to rename file: %s", file.path, exc_info=True)
                stash_logger.error(f'Failed to rename file: "{file.path}"')
                continue

            if not config.DRYRUN_ENABLED:
                try:
                    stash_db.rename(file, new_file_path)
                except Exception as error:
                    logger.error(
                        "Failed to rename file in stash database: %s",
                        file.path,
                        exc_info=True,
                    )
                    stash_logger.error(
                        f'Failed to rename file in stash database: "{file.path}"'
                    )

                    logger.warn("Rolling back file rename")
                    stash_logger.warn("Rolling back file rename")
                    rename(new_file_path, file.path)


class FilePathTooLongError(Exception):
    "Raised when the file path is too long to be saved on the OS"

    def __init__(self, path: str, message: str = "File path too long"):
        self.message = message
        self.path = path

        super().__init__(self.message)


def create_new_file_path(
    scene: Scene,
    studios: list[Studio],
    file: SceneFile,
    config: Config,
    file_name_template: str,
    file_dir_template: str,
):
    template_var_removal_order_iter = iter(
        config.PATH_CONFIG.TEMPLATE_VARIABLE_REMOVAL_ORDER
    )

    while True:
        # Part 1: Fill templates

        file_name = fill_template_file_name(
            template=file_name_template,
            scene=scene,
            studios=studios,
            file=file,
            template_variables_config=config.TEMPLATE_VARIABLES_CONFIG,
        )

        file_dir = fill_template_file_dir(
            template=file_dir_template,
            scene=scene,
            studios=studios,
            file=file,
            template_variables_config=config.TEMPLATE_VARIABLES_CONFIG,
        )

        new_file_path = str(
            (Path(file_dir) / Path(f"{file_name}.{file.extension}")).resolve()
        )

        logger.debug("Generated new file path: '%s'", new_file_path)

        # Part 2:
        # a) Check if the file's current path is the same as the new path
        #   i) If it is raise an error, as there are no changes to the file path
        #   ii) otherwise, go to b)
        # b) Check if there is already a file at the new path.
        #   i) If there is, add a duplicate suffix to the file name and go back to a)
        #   ii) otherwise, now we have a unique file path - our new file path!

        if Path(file.path) == Path(new_file_path):
            raise FileExistsError(f"No changes to file path: {file.path}")

        generate_file_path_with_suffix = append_duplicate_suffix_generator(
            new_file_path, config.PATH_CONFIG.DUPLICATE_SUFFIX_TEMPLATE
        )

        while file_exists(new_file_path):
            logger.debug(
                "A file already exists at generated path, adding duplicate suffix..."
            )

            new_file_path = next(generate_file_path_with_suffix)

            logger.debug("Generated new file path: '%s'", new_file_path)

            if Path(file.path) == Path(new_file_path):
                raise FileExistsError(f"No changes to file path: {file.path}")

        # Part 3:
        # a) Check if the new file path is too long
        #   i) If it is, remove template variables from the file name and file dir templates and go back to Part 1

        if not validate_file_path_length(
            new_file_path, config.PATH_CONFIG.MAX_PATH_LENGTH
        ):
            # Get a list of template vars to remove eg. ["{performers}", "{title}"]
            # TODO: Raise an error if there are no more template vars to remove
            logger.debug("File path too long %s", new_file_path)
            try:
                template_var_to_remove = next(template_var_removal_order_iter)

            except StopIteration:
                raise FilePathTooLongError(new_file_path)

            logger.debug(
                "Removing file name template variable '%s'",
                template_var_to_remove,
            )

            file_name_template = file_name_template.replace(template_var_to_remove, "")

            logger.debug("New file name template: '%s'", file_name_template)

            # go back to Part 1
            continue

        logger.debug("Final new file path: '%s'", new_file_path)
        return new_file_path


def append_duplicate_suffix_generator(file_path: str, duplicate_suffix_template: str):
    path = Path(file_path)
    i = 1

    while True:
        suffix = re.sub(r"{num}", str(i), duplicate_suffix_template)
        yield str(path.with_stem(f"{path.stem}{suffix}"))
        i += 1


def template_vars_to_remove_generator(template_vars_removal_order: list[str]):
    for i in range(1, len(template_vars_removal_order)):
        yield (template_vars_removal_order[:i])


def rename(src: str, dst: str):
    if get_config().DRYRUN_ENABLED:
        logger.info("[DRYRUN] [RENAME] '%s' --> '%s'", src, dst)
        stash_logger.info(f'[DRYRUN] [RENAME] "{src}" --> "{dst}"')
        return

    logger.info("[RENAME] '%s' --> '%s'", src, dst)
    stash_logger.info(f'[RENAME] "{src}" --> "{dst}"')
    try:
        if not file_exists(src):
            raise FileNotFoundError

        if file_exists(dst):
            raise FileExistsError

        os.renames(src, dst)
    except FileExistsError:
        logger.error("Destination already exists.")
        raise
    except FileNotFoundError:
        logger.error("Source or destination does not exist.")
        raise
    except IsADirectoryError:
        # Unix Error
        logger.error("Source is a file but destination is a directory.")
        raise
    except NotADirectoryError:
        # Unix Error
        logger.error("Source is a directory but destination is a file.")
        raise
    except PermissionError:
        logger.error("Operation not permitted.")
        raise
    except OSError as error:
        logger.error("OS Error: %s", exc_info=error)
        raise


def file_exists(path: str) -> bool:
    return os.path.isfile(path)


# for title basically
# def cleanup_text(text: str):
#     text = re.sub(r"\(\W*\)|\[\W*\]|{[^a-zA-Z0-9]*}", "", text)
#     text = re.sub(r"[{}]", "", text)
#     text = remove_consecutive_nonword(text)
#     return text.strip(" -_.")

# def capitalizeWords(s: str):
#     # thanks to BCFC_1982 for it
#     return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).capitalize(), s)


def sanitize_file_path(path: str, max_path_len: Optional[int] = None):
    # # Remove illegal character for Windows

    # Trying to remove non standard character
    # if MODULE_UNIDECODE and UNICODE_USE:
    #     new_filename = unidecode.unidecode(new_filename, errors="preserve")
    # else:
    #     # Using typewriter for Apostrophe
    #     new_filename = re.sub("[’‘”“]+", "'", new_filename)

    if max_path_len is None:
        return re.sub(r'[<>:"|?*]', "", path)
    return str(pathvalidate.sanitize_filepath(path, platform="auto", max_len=1000))


def validate_file_path_length(path: str, max_path_len: Optional[int] = None):
    if max_path_len is None:
        return True

    return len(path) <= max_path_len


def create_studio_hierarchy_list(
    studio_id: Optional[str] = None, studios: list[Studio] = []
) -> list[str]:
    def get_studio_with_id(id: str):
        for studio in studios:
            if studio.id == id:
                return studio
        raise ValueError(f"Studio with id {id} not found")

    if not studio_id or not studios:
        return []

    curr_studio = get_studio_with_id(studio_id)

    hierarchy_of_ids = []
    while True:
        hierarchy_of_ids.append(curr_studio.id)

        if curr_studio.parent_studio is None:
            break

        # to prevent infinite loop if there is a circular reference ie Studio A -> Studio B -> Studio A
        if curr_studio.parent_studio.id in hierarchy_of_ids:
            break

        curr_studio = get_studio_with_id(curr_studio.parent_studio.id)

    return list(
        reversed([get_studio_with_id(studio_id).name for studio_id in hierarchy_of_ids])
    )


# validate_file_exists_mock
