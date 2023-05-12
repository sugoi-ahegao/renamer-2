import pytest
from pytest_mock import MockerFixture

from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestPerformersLimit:
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
                    "SEPARATOR": ", ",
                    "ORDER_BY": "id",
                }
            )
            .build_dict()
        )

    def test_performers_limit_3_with_1_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [{"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"}]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 3,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair"

    def test_performers_limit_3_with_2_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 3,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza"

    def test_performers_limit_3_with_3_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 3,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza, Laney Grey"

    def test_performers_limit_3_with_4_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 3,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza, Laney Grey"

    def test_performers_limit_3_with_5_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                    {"id": 5, "name": "Nicole Doshi", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 3,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza, Laney Grey"

    def test_performers_limit_2_with_4_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 2,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza"

    def test_performers_limit_4_with_3_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 4,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Trinity St. Clair, Gia Derza, Laney Grey"

    def test_performers_limit_0_with_3_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Trinity St. Clair", "gender": "FEMALE"},
                    {"id": 2, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .update_performers_config(
                {
                    "LIMIT": 0,
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == f".{scene.files[0].extension}"
