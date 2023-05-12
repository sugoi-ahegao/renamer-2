from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Extra

from models.template_variables_config import (
    PerformersConfig,
    SceneTitleConfig,
    TemplateVariablesConfig,
)
from user_config import user_config


class Config(BaseModel, validate_assignment=True, extra=Extra.forbid):
    DRYRUN_ENABLED: bool = True
    STASH_API_GRAPHQL_URL: str
    STASH_SQLITE_DATABASE_PATH: str

    FILE_NAME_CONFIG: FileNameConfig
    FILE_DIR_CONFIG: FileDirConfig
    TEMPLATE_VARIABLES_CONFIG: TemplateVariablesConfig
    PATH_CONFIG: PathConfig


class FileNameConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    FILE_NAME_TEMPLATES: list[FileNameTemplateConfig] = []


class FileNameTemplateConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    matches_studio: Optional[str] = None
    matches_part_of_studio: Optional[str] = None
    matches_all_tags: Optional[list[str]] = None
    matches_any_tags: Optional[list[str]] = None
    matches_organized_value: Optional[bool] = None
    matches_scene_with_no_performers: Optional[bool] = None

    TEMPLATE: str


class FileDirConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    FILE_DIR_TEMPLATES: list[FileDirTemplateConfig] = []


class FileDirTemplateConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    matches_src: Optional[str] = None
    matches_studio: Optional[str] = None
    matches_part_of_studio: Optional[str] = None
    matches_all_tags: Optional[list[str]] = None
    matches_any_tags: Optional[list[str]] = None
    matches_organized_value: Optional[bool] = None
    matches_scene_with_no_performers: Optional[bool] = None

    TEMPLATE: str


class PathConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    MAX_PATH_LENGTH: Optional[int] = None
    DUPLICATE_SUFFIX_TEMPLATE: str = " ({num})"
    TEMPLATE_VARIABLE_REMOVAL_ORDER: list[str] = []


FileNameTemplateConfig.update_forward_refs()
FileNameConfig.update_forward_refs()

FileDirTemplateConfig.update_forward_refs()
FileDirConfig.update_forward_refs()

PathConfig.update_forward_refs()
Config.update_forward_refs()


def get_config():
    config = Config(**user_config)
    return config
