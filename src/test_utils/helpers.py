from pathlib import Path

from pytest_mock import MockerFixture

from components.process_scenes import process_scenes
from models.config import Config
from models.scene import Scene
from models.studio import Studio


def run_renamer_with_mock(
    mocker: MockerFixture,
    config: Config,
    scenes: list[Scene],
    studios: list[Studio],
):
    mocker.patch("components.process_scenes.get_config", return_value=config)

    rename_mock = mocker.patch("components.process_scenes.rename")

    process_scenes(scenes, studios)

    renames = []
    for call in rename_mock.call_args_list:
        args, kwargs = call
        src, dst = args

        renames.append(
            {
                "src": src,
                "src_file_name": Path(src).stem,
                "dst": dst,
                "dst_file_name": Path(dst).stem,
            }
        )

    return renames
