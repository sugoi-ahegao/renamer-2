import pytest
from pytest_mock import MockerFixture

from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestPerformersExcludeGenders:
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

    def test_exclude_male_performers_with_1_male_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config({"EXCLUDE_GENDERS": ["MALE"]})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Gia Derza, Laney Grey"

    def test_exclude_female_performers_with_2_female_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config({"EXCLUDE_GENDERS": ["FEMALE"]})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "J Mac"

    def test_exclude_male_performers_with_2_male_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                    {"id": 5, "name": "Peter Green", "gender": "MALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config({"EXCLUDE_GENDERS": ["MALE"]})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Gia Derza, Laney Grey"

    def test_exclude_male_and_female_performers_with_2_male_and_2_female_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Gia Derza", "gender": "FEMALE"},
                    {"id": 3, "name": "Laney Grey", "gender": "FEMALE"},
                    {"id": 4, "name": "J Mac", "gender": "MALE"},
                    {"id": 5, "name": "Peter Green", "gender": "MALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config({"EXCLUDE_GENDERS": ["MALE", "FEMALE"]})
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == f".{scene.files[0].extension}"
