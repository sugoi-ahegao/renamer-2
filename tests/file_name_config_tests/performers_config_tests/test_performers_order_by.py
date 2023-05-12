import pytest
from pytest_mock import MockerFixture

from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestPerformersOrderBy:
    @pytest.fixture
    def base_scene(self):
        return None

    @pytest.fixture
    def base_config(self):
        return (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{performers}"}])
            .with_performers_config({"SEPARATOR": ", "})
            .build_dict()
        )

    def test_performers_order_by_id(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "ORDER_BY": "id",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza, Laney Grey"

    def test_performers_order_by_name(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "ORDER_BY": "name",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Gia Derza, Laney Grey, Trinity St. Clair"

    def test_performers_order_by_id_and_ensure_id_is_not_string(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 10, "name": "Ariella Ferrera", "gender": "FEMALE"},
                    {"id": 2, "name": "Ava Addams", "gender": "FEMALE"},
                    {"id": 20, "name": "Ariella Ferrera", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "ORDER_BY": "id",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert (
            renames[0]["dst_file_name"]
            == "Trinity St. Clair, Ava Addams, Ariella Ferrera, Ariella Ferrera"
        )
