from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra

from models.scene import PerformerGenderEnum


class TemplateVariablesConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    PERFORMERS_CONFIG: Optional[PerformersConfig] = None
    SCENE_TITLE_CONFIG: Optional[SceneTitleConfig] = None


# The type of the ORDER_BY keys in the PerformersConfig
class PerformerOrderByKeys(str, Enum):
    ID = "id"
    NAME = "name"


class PerformersConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    # The separator to use between performers in the performers list. ie if SEPARATOR is ", " then the list will be "performer1, performer2, performer3"
    SEPARATOR: str = ", "
    # The max number of performers to include in the performers list. ie if LIMIT is 3 and there are 5 performers, then only the first 3 performers will be included in the list
    LIMIT: Optional[int] = None
    # a list of genders to exclude from the performers list
    EXCLUDE_GENDERS: Optional[list[PerformerGenderEnum]] = None
    # Can be "id" or "name"
    ORDER_BY: Optional[PerformerOrderByKeys] = PerformerOrderByKeys.ID
    # Default {performers} value if there are no performers
    # NOTE: This is only used if there are strictly no performers in the scene. If the performers are filtered out using LIMIT or EXCLUDE_GENDERS, then the {performers} value will be empty.
    NO_PERFORMER_NAME: Optional[str] = "No Performers"


class SceneTitleConfig(BaseModel, validate_assignment=True, extra=Extra.forbid):
    REPLACE: Optional[dict[str, str]] = None
    REPLACE_FROM_BEGINNING: Optional[dict[str, str]] = None


SceneTitleConfig.update_forward_refs()
PerformersConfig.update_forward_refs()
TemplateVariablesConfig.update_forward_refs()
