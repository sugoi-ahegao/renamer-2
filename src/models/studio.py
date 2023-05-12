from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Extra


class Studio(BaseModel, validate_assignment=True, extra=Extra.forbid):
    id: str
    name: str
    parent_studio: Optional[Studio] = None
