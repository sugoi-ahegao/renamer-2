import pytest
from pytest_mock import MockerFixture

from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestPerformersSeparator:
    @pytest.fixture
    def base_scene(self):
        return None

    @pytest.fixture
    def base_config(self):
        return (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{performers}"}])
            .with_performers_config(
                {
                    "ORDER_BY": "id",
                }
            )
            .build_dict()
        )

    def test_custom_separator_with_one_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers([{"id": 1, "name": "Performer A"}])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config({"SEPARATOR": " & "})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Performer A"

    def test_custom_separator_with_two_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [{"id": 1, "name": "Performer A"}, {"id": 2, "name": "Performer B"}]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config({"SEPARATOR": " - "})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Performer A - Performer B"

    def test_custom_separator_with_three_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Performer A"},
                    {"id": 2, "name": "Performer B"},
                    {"id": 3, "name": "Performer C"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config({"SEPARATOR": " & "})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert (
            renames[0]["dst_file_name"]
        ) == "Performer A & Performer B & Performer C"
