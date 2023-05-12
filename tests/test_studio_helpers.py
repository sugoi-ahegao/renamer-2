from components.studio_helpers import (
    contains_studio,
    get_parent_studio,
    get_studio_family,
    get_studio_hierarchy,
)
from models.studio import Studio


class TestParentStudioAndStudioFamily:
    def test_with_1_studio(self) -> None:
        studio = Studio(id="1", name="Studio 1", parent_studio=None)
        studios = [studio]

        curr_studio = studio

        assert get_parent_studio(curr_studio, studios) is curr_studio

        assert get_studio_family(curr_studio, studios) is curr_studio

    def test_with_parent_and_child_studios(self) -> None:
        parent_studio = Studio(id="1", name="Studio 1", parent_studio=None)
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)

        studios = [parent_studio, child_studio]

        curr_studio = child_studio

        assert get_parent_studio(curr_studio, studios) == parent_studio
        assert get_studio_family(curr_studio, studios) == parent_studio

    def test_with_grandparent_and_parent_and_child_studios(self) -> None:
        grandparent_studio = Studio(id="3", name="Studio 1", parent_studio=None)

        parent_studio = Studio(
            id="1", name="Studio 1", parent_studio=grandparent_studio
        )
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)

        studios = [parent_studio, grandparent_studio, child_studio]

        curr_studio = child_studio

        assert get_parent_studio(curr_studio, studios) == parent_studio
        assert get_studio_family(curr_studio, studios) == grandparent_studio

    def test_studios_with_cycles(self) -> None:
        grandparent_studio = Studio(id="3", name="Studio 1", parent_studio=None)

        parent_studio = Studio(
            id="1", name="Studio 1", parent_studio=grandparent_studio
        )

        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)

        grandparent_studio.parent_studio = child_studio

        studios = [parent_studio, grandparent_studio, child_studio]

        curr_studio = child_studio

        parent_studio_result = get_parent_studio(curr_studio, studios)
        studio_family_result = get_studio_family(curr_studio, studios)

        assert parent_studio_result is not None
        assert parent_studio_result.id == parent_studio.id

        assert studio_family_result is not None
        assert studio_family_result.id == grandparent_studio.id

    def test_studios_with_cycles_2(self) -> None:
        great_grandparent_studio = Studio(id="4", name="Studio 4", parent_studio=None)
        grandparent_studio = Studio(
            id="3", name="Studio 3", parent_studio=great_grandparent_studio
        )
        parent_studio = Studio(
            id="1", name="Studio 1", parent_studio=grandparent_studio
        )
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)
        great_grandparent_studio.parent_studio = child_studio

        studios = [
            parent_studio,
            grandparent_studio,
            child_studio,
            great_grandparent_studio,
        ]

        curr_studio = child_studio

        parent_studio_result = get_parent_studio(curr_studio, studios)
        studio_family_result = get_studio_family(curr_studio, studios)

        assert parent_studio_result is not None
        assert parent_studio_result.id == parent_studio.id

        assert studio_family_result is not None
        assert studio_family_result.id == great_grandparent_studio.id


class TestContainsStudio:
    def test_studio_contains_itself(self) -> None:
        studio = Studio(id="1", name="Studio 1", parent_studio=None)

        studios = [studio]

        child_studio = studio
        parent_studio = studio

        assert contains_studio(
            studio=child_studio,
            target_studio_family=parent_studio,
            studios=studios,
        )

    def test_contains_studio_with_basic_child_and_parent_studios(self) -> None:
        parent_studio = Studio(id="1", name="Studio 1", parent_studio=None)
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)

        studios = [parent_studio, child_studio]

        assert contains_studio(
            studio=child_studio,
            target_studio_family=parent_studio,
            studios=studios,
        )

    def test_contains_studio_with_3_studios(self) -> None:
        grandparent_studio = Studio(id="3", name="Studio 1", parent_studio=None)
        parent_studio = Studio(
            id="1", name="Studio 1", parent_studio=grandparent_studio
        )
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)

        studios = [parent_studio, grandparent_studio, child_studio]

        assert contains_studio(
            studio=child_studio,
            target_studio_family=parent_studio,
            studios=studios,
        )

        assert contains_studio(
            studio=child_studio,
            target_studio_family=grandparent_studio,
            studios=studios,
        )

    def test_contains_studio_with_cycles(self) -> None:
        grandparent_studio = Studio(id="3", name="Studio 3", parent_studio=None)
        parent_studio = Studio(
            id="1", name="Studio 1", parent_studio=grandparent_studio
        )
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)
        grandparent_studio.parent_studio = child_studio

        studios = [parent_studio, grandparent_studio, child_studio]

        assert contains_studio(
            studio=child_studio,
            target_studio_family=parent_studio,
            studios=studios,
        )

        assert contains_studio(
            studio=child_studio,
            target_studio_family=grandparent_studio,
            studios=studios,
        )

    def test_not_contains_studio_2_studios(self) -> None:
        not_really_parent_studio = Studio(id="1", name="Studio 1", parent_studio=None)
        child_studio = Studio(id="2", name="Studio 2", parent_studio=None)

        studios = [not_really_parent_studio, child_studio]

        assert not contains_studio(
            studio=child_studio,
            target_studio_family=not_really_parent_studio,
            studios=studios,
        )

    def test_not_contains_studio_5_studios(self) -> None:
        disjointed_studio_1 = Studio(id="4", name="Studio 4", parent_studio=None)
        disjointed_studio_2 = Studio(
            id="5", name="Studio 5", parent_studio=disjointed_studio_1
        )
        grandparent_studio = Studio(id="3", name="Studio 3", parent_studio=None)
        parent_studio = Studio(
            id="1", name="Studio 1", parent_studio=grandparent_studio
        )
        child_studio = Studio(id="2", name="Studio 2", parent_studio=parent_studio)

        studios = [
            parent_studio,
            child_studio,
            grandparent_studio,
            disjointed_studio_1,
            disjointed_studio_2,
        ]

        assert not contains_studio(
            studio=child_studio,
            target_studio_family=disjointed_studio_1,
            studios=studios,
        )


class TestStudioHierarchy:
    def test_studio_hierarchy_base_case(self) -> None:
        studio = Studio(id="1", name="Studio 1", parent_studio=None)

        studios = [studio]

        studio_hierarchy = get_studio_hierarchy(studio, studios)

        assert studio_hierarchy is not None
        assert studio_hierarchy == [studio]

    def test_studio_hierarchy_with_parent_and_child(self) -> None:
        parent_studio = Studio(id="1", name="Parent Studio")
        child_studio = Studio(id="2", name="Child Studio", parent_studio=parent_studio)

        studios = [child_studio, parent_studio]

        studio_hierarchy = get_studio_hierarchy(child_studio, studios)

        assert studio_hierarchy is not None
        assert studio_hierarchy == [parent_studio, child_studio]

        studio_hierarchy = get_studio_hierarchy(parent_studio, studios)

        assert studio_hierarchy is not None
        assert studio_hierarchy == [parent_studio]

    def test_studio_hierarchy_with_grandparent_parent_and_child(self) -> None:
        studio_grandparent = Studio(id="1", name="GrandParent Studio")
        studio_parent = Studio(id="2", name="Parent Studio")
        studio_child = Studio(id="3", name="Child Studio")

        studio_child.parent_studio = studio_parent
        studio_parent.parent_studio = studio_grandparent

        studios = [studio_child, studio_parent, studio_grandparent]

        studio_hierarchy = get_studio_hierarchy(studio_child, studios)

        assert studio_hierarchy is not None
        assert studio_hierarchy == [studio_grandparent, studio_parent, studio_child]

        studio_hierarchy = get_studio_hierarchy(studio_parent, studios)

        assert studio_hierarchy is not None
        assert studio_hierarchy == [studio_grandparent, studio_parent]

        studio_hierarchy = get_studio_hierarchy(studio_grandparent, studios)

        assert studio_hierarchy is not None
        assert studio_hierarchy == [studio_grandparent]
