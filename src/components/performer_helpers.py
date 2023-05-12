from typing import Optional

from models.scene import PerformerGenderEnum, ScenePerformer
from models.template_variables_config import PerformersConfig


def apply_performers_exclude_genders(
    performers: list[ScenePerformer], excluded_genders: list[PerformerGenderEnum] | None
):
    if not excluded_genders:
        return performers

    return [
        performer
        for performer in performers
        if performer.gender not in excluded_genders
    ]


def apply_performers_order_by(
    performers: list[ScenePerformer], order_by: Optional[str]
):
    if not order_by:
        return sorted(performers, key=lambda performer: performer.dict()["id"])

    return sorted(performers, key=lambda performer: performer.dict()[order_by])


def apply_performers_limit(performers: list[ScenePerformer], limit: Optional[int]):
    if limit == None:
        return performers

    return performers[:limit]
