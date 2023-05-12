from unittest.mock import call
import pytest
from pytest_mock import MockerFixture
from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock

from test_utils.scene_builder import SceneBuilder
from models.scene import Studio
from test_utils.scene_file_builder import SceneFileBuilder


def create_file_exists_mock_validator(
    mocker: MockerFixture,
    expected_file_exists_calls: list[str],
):
    side_effect = [True for _ in range(len(expected_file_exists_calls) - 1)]
    side_effect.append(False)

    file_exists_mock = mocker.patch(
        "components.process_scenes.file_exists",
        side_effect=side_effect,
    )

    def file_exists_mock_validator():
        expected_call_args_list = [call(path) for path in expected_file_exists_calls]
        return file_exists_mock.call_args_list == expected_call_args_list

    return file_exists_mock_validator


class TestDuplicateFilePaths:
    @pytest.fixture
    def studio_bangbros(self):
        return Studio(**{"id": 1, "name": "Bangbros"})

    @pytest.fixture
    def base_scene(self, studio_bangbros: Studio):
        return (
            SceneBuilder()
            .with_studio(studio_bangbros.dict())
            .with_title("A Bangbros Scene")
            .with_files(
                [
                    SceneFileBuilder(id="1")
                    .with_file_path(R"C:\A Random File.mp4")
                    .build_dict()
                ]
            )
            .build_dict()
        )

    @pytest.fixture
    def base_config(self):
        return (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{title}"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH\{studio}"}])
            .build_dict()
        )

    # test when there is already a file with the same path as new file path

    def test_file_path_exists_base_case(
        self,
        base_scene: dict,
        base_config: dict,
        studio_bangbros: Studio,
        mocker: MockerFixture,
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_duplicate_suffix_template("_({num})")
            .build()
        )
        studios = [studio_bangbros]

        expected_rename_dst = R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene.mp4"
        expected_file_exists_calls = [
            expected_rename_dst,
        ]

        validate_file_exists_mock = create_file_exists_mock_validator(
            mocker,
            expected_file_exists_calls=expected_file_exists_calls,
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == expected_rename_dst

        assert validate_file_exists_mock()

    def test_file_path_exists_once(
        self,
        base_scene: dict,
        base_config: dict,
        studio_bangbros: Studio,
        mocker: MockerFixture,
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_duplicate_suffix_template("__({num})")
            .build()
        )
        studios = [studio_bangbros]

        expected_rename_dst = (
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene__(1).mp4"
        )
        expected_file_exists_calls = [
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene.mp4",
            expected_rename_dst,
        ]

        validate_file_exists_mock = create_file_exists_mock_validator(
            mocker,
            expected_file_exists_calls=expected_file_exists_calls,
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == expected_rename_dst

        assert validate_file_exists_mock()

    def test_file_path_exists_twice(
        self,
        base_scene: dict,
        base_config: dict,
        studio_bangbros: Studio,
        mocker: MockerFixture,
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_duplicate_suffix_template("__({num})")
            .build()
        )
        studios = [studio_bangbros]

        expected_rename_dst = (
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene__(2).mp4"
        )
        expected_file_exists_calls = [
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene__(1).mp4",
            expected_rename_dst,
        ]

        validate_file_exists_mock = create_file_exists_mock_validator(
            mocker,
            expected_file_exists_calls=expected_file_exists_calls,
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == expected_rename_dst

        assert validate_file_exists_mock()

    def test_file_path_exists_thrice(
        self,
        base_scene: dict,
        base_config: dict,
        studio_bangbros: Studio,
        mocker: MockerFixture,
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config).with_duplicate_suffix_template("({num})").build()
        )
        studios = [studio_bangbros]

        expected_rename_dst = R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene(3).mp4"
        expected_file_exists_calls = [
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene(1).mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene(2).mp4",
            expected_rename_dst,
        ]

        validate_file_exists_mock = create_file_exists_mock_validator(
            mocker,
            expected_file_exists_calls=expected_file_exists_calls,
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == expected_rename_dst

        assert validate_file_exists_mock()

    def test_file_path_exists_many_times(
        self,
        base_scene: dict,
        base_config: dict,
        studio_bangbros: Studio,
        mocker: MockerFixture,
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config).with_duplicate_suffix_template(" {num}").build()
        )
        studios = [studio_bangbros]

        expected_rename_dst = R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 14.mp4"
        expected_file_exists_calls = [
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 1.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 2.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 3.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 4.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 5.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 6.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 7.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 8.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 9.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 10.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 11.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 12.mp4",
            R"C:\User\Desktop\STASH\Bangbros\A Bangbros Scene 13.mp4",
            expected_rename_dst,
        ]

        validate_file_exists_mock = create_file_exists_mock_validator(
            mocker,
            expected_file_exists_calls=expected_file_exists_calls,
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == expected_rename_dst

        assert validate_file_exists_mock()
