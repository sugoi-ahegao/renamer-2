import datetime
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Optional

import pathvalidate

import components.setup_logging
from components.process_scenes import process_scenes
from components.stash_db import StashDB
from components.stash_graphql import StashGraphQL
from components.stash_logger import get_stash_logger
from models.config import Config, FileNameConfig, PerformersConfig, get_config
from models.scene import Scene, SceneFile, ScenePerformer
from models.studio import Studio

logger = logging.getLogger(__name__)


def optional_chain(root, keys: str):
    result = root
    for k in keys.split("."):
        if isinstance(result, dict):
            result = result.get(k, None)
        else:
            result = getattr(result, k, None)
        if result is None:
            break
    return result


def rename_all_scenes():
    logger.info("Renaming all Scenes")
    config = get_config()
    stash_graphql = StashGraphQL(config.STASH_API_GRAPHQL_URL)

    scenes = stash_graphql.get_all_scenes()
    studios = stash_graphql.get_all_studios()

    process_scenes(scenes, studios)
    logger.info("Finished Renaming all Scenes")


def rename_scenes(scene_ids: list[int]):
    logger.info("Renaming Scenes with IDs: %s", scene_ids)
    config = get_config()
    stash_graphql = StashGraphQL(config.STASH_API_GRAPHQL_URL)

    scenes: list[Scene] = []
    for scene_id in scene_ids:
        scenes.append(stash_graphql.get_scene_with_id(scene_id))

    studios = stash_graphql.get_all_studios()

    process_scenes(scenes, studios)
    logger.info("Finished Renaming Scenes with IDs: %s", scene_ids)


def main():
    # Log to StashApp
    stash_logger = get_stash_logger()
    stash_logger.debug("Starting Renamer 2")
    logger.info("Starting Renamer 2")

    # Get args from StashApp
    stashPluginInput = sys.stdin.read()

    if stashPluginInput.strip() == "":
        rename_all_scenes()
        return

    stashPluginArgs = json.loads(stashPluginInput)

    if (
        optional_chain(stashPluginArgs, "args.hookContext.input.cover_image")
        is not None
    ):
        stashPluginArgs["args"]["hookContext"]["input"][
            "cover_image"
        ] = "--- REDACTED ---"

    if optional_chain(stashPluginArgs, "args.hookContext.input.details") is not None:
        stashPluginArgs["args"]["hookContext"]["input"]["details"] = "--- REDACTED ---"

    logger.debug(f"stashPluginArgs: {stashPluginArgs}")

    if optional_chain(stashPluginArgs, "args.mode") == "all_scenes":
        rename_all_scenes()
        return

    if optional_chain(stashPluginArgs, "args.hookContext.inputFields") is not None:
        inputFields = stashPluginArgs["args"]["hookContext"]["inputFields"]

        if "id" in inputFields:
            scene_id = int(stashPluginArgs["args"]["hookContext"]["input"]["id"])
            rename_scenes([scene_id])
            return
        elif "ids" in inputFields:
            scene_ids = stashPluginArgs["args"]["hookContext"]["input"]["ids"]
            scene_ids = [int(scene_id) for scene_id in scene_ids]
            rename_scenes(scene_ids)
            return
        else:
            raise ValueError("id or ids not in inputFields")

    logger.debug("No Scene Ids found in hookContext, shutting down")
    return


if __name__ == "__main__":
    main()
