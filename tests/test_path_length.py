import os

import pytest
from pytest_mock import MockerFixture

from models.studio import Studio
from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder
from test_utils.scene_file_builder import SceneFileBuilder


class TestPathLength:
    def test_path_length(self, mocker: MockerFixture):
        scene = (
            SceneBuilder()
            .with_files(
                [
                    SceneFileBuilder(id="1")
                    .with_file_path(R"C:\User\Desktop\My File.mp4")
                    .build_dict()
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "0123456789"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(240)
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert len(renames[0]["dst"]) == 36

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "0123456789"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(37)
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert len(renames[0]["dst"]) == 36
        assert (renames[0]["dst"]) == R"C:\User\Desktop\STASH\0123456789.mp4"

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "0123456789"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(36)
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert len(renames[0]["dst"]) == 36

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "0123456789"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(35)
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "0123456789"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(30)
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_path_length_with_long_path(self, mocker: MockerFixture):
        scene = (
            SceneBuilder()
            .with_files(
                [
                    SceneFileBuilder(id="1")
                    .with_file_path(R"C:\User\Desktop\My File.mp4")
                    .build_dict(),
                ]
            )
            .build()
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates(
                [
                    {
                        "TEMPLATE": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                    }
                ]
            )
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(None)
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert len(renames[0]["dst"]) == 500
        assert (
            renames[0]["dst"]
            == R"C:\User\Desktop\STASH\AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.mp4"
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "File"}])
            .with_file_dir_templates(
                [
                    {
                        "TEMPLATE": R"C:\User\Desktop\STASH\AAAAA\BBBBB\CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
                    }
                ]
            )
            .with_max_path_len(None)
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert len(renames[0]["dst"]) == 500
        assert (
            renames[0]["dst"]
            == R"C:\User\Desktop\STASH\AAAAA\BBBBB\CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\File.mp4"
        )

    def test_template_variable_removal_order(self, mocker: MockerFixture):
        abuse_me_studio = Studio(**{"id": "1", "name": "AbuseMe"})

        studios = [abuse_me_studio]

        scene = (
            SceneBuilder()
            .with_studio(abuse_me_studio.dict())
            .with_title("Rough Sex Dream")
            .with_files(
                [SceneFileBuilder(id="1").with_file_path(R"C:\File.mp4").build_dict()]
            )
            .build()
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{studio} {title}"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH\{studio}"}])
            .with_max_path_len(None)
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert (
            renames[0]["dst"]
            == R"C:\User\Desktop\STASH\AbuseMe\AbuseMe Rough Sex Dream.mp4"
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{studio} {title}"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH\{studio}"}])
            .with_max_path_len(50)
            .with_template_variable_removal_order(["{studio}"])
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == R"C:\User\Desktop\STASH\AbuseMe\Rough Sex Dream.mp4"

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{studio} {title}"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH\{studio}"}])
            .with_max_path_len(40)
            .with_template_variable_removal_order(["{studio}", "{title}"])
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == R"C:\User\Desktop\STASH\AbuseMe\.mp4"

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": "{studio} - {title}"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH\{studio}"}])
            .with_max_path_len(40)
            .with_template_variable_removal_order(["{studio}", "{title}"])
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == R"C:\User\Desktop\STASH\AbuseMe\-.mp4"

    def test_path_with_long_title(self, mocker: MockerFixture):
        scene_title = "Pee Between Girls, Alicia Trece & Moona Snake , 2on2, BBC, ATOGM, DAP, Big Gapes, Pee Drink, Squirt, Creampie Swallow GIO2040"

        scene = (
            SceneBuilder()
            .with_files(
                [
                    SceneFileBuilder(id="1")
                    .with_file_path(R"C:\User\Desktop\My File.mp4")
                    .build_dict(),
                ]
            )
            .with_title(scene_title)
            .build()
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": R"{title} {title}"}])
            .with_file_dir_templates([{"TEMPLATE": R"C:\User\Desktop\STASH"}])
            .with_max_path_len(240)
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_config_template_path_with_trailing_slash(self, mocker: MockerFixture):
        scene_title = "Scene Title"
        config_template_path = R"C:\User\Desktop\STASH"

        scene = (
            SceneBuilder()
            .with_files(
                [
                    SceneFileBuilder(id="1")
                    .with_file_path(R"C:\User\Desktop\My File.mp4")
                    .build_dict(),
                ]
            )
            .with_title(scene_title)
            .build()
        )

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": R"{title}"}])
            .with_file_dir_templates([{"TEMPLATE": config_template_path}])
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst"] == R"C:\User\Desktop\STASH\Scene Title.mp4"

        config_template_path = R"C:\User\Desktop\STASH\ "

        config = (
            ConfigBuilder()
            .with_file_name_templates([{"TEMPLATE": R"{title}"}])
            .with_file_dir_templates([{"TEMPLATE": config_template_path}])
            .build()
        )

        assert len(renames) == 1
        assert renames[0]["dst"] == R"C:\User\Desktop\STASH\Scene Title.mp4"
