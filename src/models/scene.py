from __future__ import annotations

import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Extra, validator

from models.studio import Studio


class Scene(BaseModel, validate_assignment=True, extra=Extra.forbid):
    id: str
    title: Optional[str] = ""
    date: Optional[datetime.date] = None
    studio: Optional[Studio] = None
    performers: List[ScenePerformer]
    rating100: Optional[int] = None
    organized: bool
    code: Optional[str] = None
    tags: list[SceneTag]
    files: list[SceneFile]
    movies: list[SceneMovie]
    stash_ids: list[StashId]

    @property
    def rating(self):
        return self.rating100

    @property
    def studio_code(self):
        return self.code

    @property
    def stash_id(self):
        if self.stash_ids:
            return self.stash_ids[0].stash_id
        return None

    @property
    def movie_name(self):
        if self.movies:
            return self.movies[0].movie.name
        return None

    @property
    def movie_date(self):
        if self.movies:
            return self.movies[0].movie.date
        return None

    @property
    def movie_scene_number(self):
        if self.movies:
            return self.movies[0].scene_index
        return None


class ScenePerformer(BaseModel, validate_assignment=True, extra=Extra.forbid):
    id: int
    name: str
    favorite: bool
    gender: Optional[PerformerGenderEnum] = None
    rating100: Optional[int] = None
    stash_ids: List[StashId]

    @validator("gender", pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

    @property
    def rating(self):
        return self.rating100

    @property
    def stash_id(self):
        if self.stash_ids:
            return self.stash_ids[0].stash_id
        return None


class PerformerGenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    TRANSGENDER_MALE = "TRANSGENDER_MALE"
    TRANSGENDER_FEMALE = "TRANSGENDER_FEMALE"
    INTERSEX = "INTERSEX"
    NON_BINARY = "NON_BINARY"
    UNDEFINED = "UNDEFINED"


class SceneTag(BaseModel, validate_assignment=True, extra=Extra.forbid):
    id: int
    name: str


class SceneFile(BaseModel, validate_assignment=True, extra=Extra.forbid):
    id: str
    path: str
    basename: str
    width: int
    height: int
    video_codec: str
    audio_codec: str
    frame_rate: float
    duration: datetime.time
    bit_rate: int
    mod_time: str
    created_at: str
    updated_at: str
    parent_folder_id: int
    fingerprints: List[SceneFileFingerprint] = []

    @property
    def extension(self):
        return self.basename.split(".")[-1]

    @property
    def bit_rate_mbps(self):
        return str(round(self.bit_rate / 1000000, 2))

    @property
    def resolution(self):
        return f"{self.height}p"

    @property
    def resolution_name(self):
        if self.height > self.width:
            return "VERTICAL"

        if self.height >= 4320:
            return "8k"
        elif self.height >= 3384:
            return "6k"
        elif self.height >= 2880:
            return "5k"
        elif self.height >= 2160:
            return "4k"
        elif self.height >= 1440:
            return "2k"
        elif self.height >= 1080:
            return "FHD"
        elif self.height >= 720:
            return "HD"
        elif self.height >= 480:
            return "SD"
        else:
            return f"{self.height}p"

    @property
    def oshash(self):
        for fingerprint in self.fingerprints:
            if fingerprint.type == SceneFileFingerprintTypeEnum.OSHASH:
                return fingerprint.value
        return None

    @property
    def phash(self):
        for fingerprint in self.fingerprints:
            if fingerprint.type == SceneFileFingerprintTypeEnum.PHASH:
                return fingerprint.value
        return None


class SceneFileFingerprint(BaseModel, validate_assignment=True, extra=Extra.forbid):
    type: SceneFileFingerprintTypeEnum
    value: str


class SceneFileFingerprintTypeEnum(str, Enum):
    OSHASH = "oshash"
    PHASH = "phash"


class SceneMovie(BaseModel, validate_assignment=True, extra=Extra.forbid):
    movie: Movie
    scene_index: Optional[int] = None


class Movie(BaseModel, validate_assignment=True, extra=Extra.forbid):
    id: int
    name: str
    date: Optional[datetime.date] = None


class StashId(BaseModel, validate_assignment=True, extra=Extra.forbid):
    endpoint: str
    stash_id: str


StashId.update_forward_refs()
Movie.update_forward_refs()
SceneMovie.update_forward_refs()
SceneFileFingerprint.update_forward_refs()
SceneFile.update_forward_refs()
ScenePerformer.update_forward_refs()
Scene.update_forward_refs()
