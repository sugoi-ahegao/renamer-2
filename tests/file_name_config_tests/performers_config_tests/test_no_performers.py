import pytest
from pytest_mock import MockerFixture

from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestNoPerformer:
    @pytest.fixture
    def base_scene(self):
        return None

    @pytest.fixture
    def base_config(self):
        return (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{performers}"}])
            .build_dict()
        )

    def test_no_performers_in_scene(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).with_performers([]).build()

        config = (
            ConfigBuilder(base_config)
            .with_performers_config(
                {
                    "NO_PERFORMER_NAME": "Zero Performers",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "Zero Performers"

    def test_limit_0_with_1_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers([{"id": 1, "name": "Nicole Doshi"}])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config(
                {
                    "LIMIT": 0,
                    "NO_PERFORMER_NAME": "Zero Performers",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == f".{scene.files[0].extension}"

    def test_exclude_females_with_1_female_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers([{"id": 1, "name": "Nicole Doshi", "gender": "FEMALE"}])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config(
                {
                    "EXCLUDE_GENDERS": ["FEMALE"],
                    "NO_PERFORMER_NAME": "Zero Performers",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == f".{scene.files[0].extension}"

    def test_exclude_males_with_1_male_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers([{"id": 1, "name": "Nicole Doshi", "gender": "MALE"}])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config(
                {
                    "EXCLUDE_GENDERS": ["MALE"],
                    "NO_PERFORMER_NAME": "Zero Performers",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == f".{scene.files[0].extension}"

    def test_exclude_males_and_females_with_1_male_and_1_female_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers(
                [
                    {"id": 1, "name": "Nicole Doshi", "gender": "MALE"},
                    {"id": 2, "name": "J Mac", "gender": "FEMALE"},
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_performers_config(
                {
                    "EXCLUDE_GENDERS": ["MALE", "FEMALE"],
                    "NO_PERFORMER_NAME": "Zero Performers",
                }
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == f".{scene.files[0].extension}"
