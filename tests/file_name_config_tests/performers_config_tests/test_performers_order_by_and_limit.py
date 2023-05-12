import pytest
from pytest_mock import MockerFixture

from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestPerformersOrderByAndLimit:
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

    def test_performers_order_by_id_limit_2_with_3_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 3, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 1, "name": "Laney Grey", "gender": "FEMALE"},
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
                    "LIMIT": 2,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Laney Grey, Gia Derza"

    def test_performers_order_by_name_limit_2_with_3_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 3, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 1, "name": "Laney Grey", "gender": "FEMALE"},
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
                    "LIMIT": 2,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Gia Derza, Laney Grey"
