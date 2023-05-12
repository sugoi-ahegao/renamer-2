from typing import Optional

from models.studio import Studio


def find_studio_with_id(studio_id: str, studios: list[Studio]) -> Optional[Studio]:
    for studio in studios:
        if studio.id == studio_id:
            return studio

    return None


def find_studio_with_name(studio_name: str, studios: list[Studio]) -> Optional[Studio]:
    for studio in studios:
        if studio.name.lower() == studio_name.lower():
            return studio

    return None


def get_parent_studio(studio: Studio, studios: list[Studio]) -> Studio:
    # Get the studio from the list of studios, to ensure we have the full object
    curr_studio = find_studio_with_id(studio.id, studios)

    # The studio that the caller sent should always be found in the studio list
    if curr_studio is None:
        raise ValueError(f"Studio {studio.id} not found in studios list")

    # If the studio has a parent, return the parent, otherwise, return itself
    if not curr_studio.parent_studio:
        return curr_studio

    parent_studio = find_studio_with_id(curr_studio.parent_studio.id, studios)

    if not parent_studio:
        raise ValueError(
            f"Studio {curr_studio.parent_studio.id} not found in studios list"
        )

    return parent_studio


def get_studio_family(studio: Studio, studios: list[Studio]) -> Studio:
    curr_studio = find_studio_with_id(studio.id, studios)

    if curr_studio is None:
        raise ValueError(f"Studio {studio.id} not found in studios list")

    # if you pass a string into a set ie. set("string"), it will create a set of characters ie. {'s', 't', 'r', 'i', 'n', 'g'}
    # so we need to put the string in an array and then create a set from the array
    explored_studio_ids = set([curr_studio.id])

    while True:
        parent_studio = get_parent_studio(curr_studio, studios)

        if parent_studio.id in explored_studio_ids:
            return curr_studio

        explored_studio_ids.add(parent_studio.id)
        curr_studio = parent_studio


def contains_studio(
    studio: Studio, target_studio_family: Studio, studios: list[Studio]
) -> bool:
    curr_studio = find_studio_with_id(studio.id, studios)

    if curr_studio is None:
        raise ValueError(f"Studio '{studio.id}' not found in studios list")

    studio_family = find_studio_with_id(target_studio_family.id, studios)

    if studio_family is None:
        raise ValueError(
            f"Studio '{target_studio_family.id}' not found in studios list"
        )

    # child studio is the same as the target studio family
    if curr_studio.id == studio_family.id:
        return True

    # if you pass a string into a set ie. set("string"), it will create a set of characters ie. {'s', 't', 'r', 'i', 'n', 'g'}
    # so we need to put the string in an array and then create a set from the array
    explored_studio_ids = set([curr_studio.id])

    while True:
        curr_studio = get_parent_studio(curr_studio, studios)

        if curr_studio.id == studio_family.id:
            return True

        if curr_studio.id in explored_studio_ids:
            return False

        explored_studio_ids.add(curr_studio.id)


def get_studio_hierarchy(studio: Studio, studios: list[Studio]) -> list[Studio]:
    curr_studio = find_studio_with_id(studio.id, studios)

    if curr_studio is None:
        raise ValueError(f"Studio '{studio.id}' not found in studios list")

    studio_hierarchy = [curr_studio]

    # if you pass a string into a set ie. set("string"), it will create a set of characters ie. {'s', 't', 'r', 'i', 'n', 'g'}
    # so we need to put the string in an array and then create a set from the array
    explored_studio_ids = set([curr_studio.id])

    while True:
        parent_studio = get_parent_studio(curr_studio, studios)

        if parent_studio.id in explored_studio_ids:
            break

        studio_hierarchy.append(parent_studio)
        explored_studio_ids.add(parent_studio.id)

        curr_studio = parent_studio

    studio_hierarchy.reverse()
    return studio_hierarchy
