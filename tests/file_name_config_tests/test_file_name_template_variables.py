import pytest
from pytest_mock import MockerFixture

from models.studio import Studio
from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestFileNameTemplateVariables:
    @pytest.fixture
    def base_scene(self):
        return {
            "id": 1,
            "title": "Scene Title",
            "date": "2023-01-15",
            "rating100": 100,
            "studio": {"id": 1, "name": "Studio A"},
            "code": "ABC-123",
            "organized": False,
            "performers": [
                {
                    "id": 1,
                    "name": "Trinity St. Clair",
                    "gender": "FEMALE",
                    "favorite": False,
                    "stash_ids": [
                        {
                            "endpoint": "http://localhost:9999/graphql",
                            "stash_id": "performer_stash_id_1",
                        }
                    ],
                },
                {
                    "id": 2,
                    "name": "Gia Derza",
                    "gender": "FEMALE",
                    "favorite": False,
                    "stash_ids": [
                        {
                            "endpoint": "http://localhost:9999/graphql",
                            "stash_id": "performer_stash_id_2",
                        }
                    ],
                },
                {
                    "id": 3,
                    "name": "J Mac",
                    "gender": "MALE",
                    "favorite": False,
                    "stash_ids": [
                        {
                            "endpoint": "http://localhost:9999/graphql",
                            "stash_id": "performer_stash_id_3",
                        }
                    ],
                },
            ],
            "tags": [
                {
                    "id": 1,
                    "name": "Tag 1",
                },
                {"id": 2, "name": "Tag 2"},
                {"id": 3, "name": "Tag 3"},
            ],
            "files": [
                {
                    "id": "1",
                    "basename": "file1.mp4",
                    "path": R"C:\Users\Desktop\file1.mp4",
                    "width": "1920",
                    "height": "1080",
                    "video_codec": "h264",
                    "audio_codec": "aac",
                    "frame_rate": 30,
                    "duration": 3030.56,
                    "bit_rate": 6158790,
                    "mod_time": "2022-11-29T23:54:07-07:00",
                    "created_at": "2023-02-22T22:55:02-07:00",
                    "updated_at": "2023-03-07T12:21:01-07:00",
                    "parent_folder_id": "140",
                    "fingerprints": [
                        {"type": "oshash", "value": "file_oshash"},
                        {"type": "phash", "value": "file_phash"},
                    ],
                }
            ],
            "movies": [
                {
                    "movie": {"id": 1, "name": "Movie A", "date": "2022-01-15"},
                    "scene_index": 1,
                }
            ],
            "stash_ids": [
                {
                    "endpoint": "http://localhost:9999/graphql",
                    "stash_id": "scene_stash_id",
                },
            ],
        }

    @pytest.fixture
    def base_config(self):
        return ConfigBuilder().with_max_path_len(None).build_dict()

    def test_template_with_all_template_variables(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "TEMPLATE": "({title}) ({studio}) ({performers}) ({date}) ({resolution}) ({resolution_name}) ({duration}) ({bit_rate_mbps}) ({parent_studio}) ({studio_family}) ({rating}) ({tags}) ({video_codec}) ({audio_codec}) ({movie_scene_number}) ({movie_name}) ({movie_date}) ({scene_stash_id}) ({performers_stash_ids}) ({studio_code}) ({oshash}) ({phash})"
                    }
                ]
            )
            .build()
        )

        scene_studio = scene.studio
        assert scene_studio is not None

        parent_studio = Studio(**{"id": 2, "name": "Parent Studio"})
        scene_studio.parent_studio = parent_studio

        studios = [scene_studio, parent_studio]

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert (
            renames[0]["dst_file_name"]
            == "(Scene Title) (Studio A) (Trinity St. Clair, Gia Derza, J Mac) (2023-01-15) (1080p) (FHD) (00.50.30) (6.16) (Parent Studio) (Parent Studio) (100) (Tag 1, Tag 2, Tag 3) (h264) (aac) (1) (Movie A) (2022-01-15) (scene_stash_id) (performer_stash_id_1, performer_stash_id_2, performer_stash_id_3) (ABC-123) (file_oshash) (file_phash)"
        )

    def test_template_with_formatting(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "TEMPLATE": "[{studio}] {date} {title} -- {performers} ({resolution})"
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert (
            renames[0]["dst_file_name"]
            == "[Studio A] 2023-01-15 Scene Title -- Trinity St. Clair, Gia Derza, J Mac (1080p)"
        )

    def test_template_with_invalid_variable(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates([{"TEMPLATE": "[{studio}] {title} -- {random}"}])
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "[Studio A] Scene Title -- {random}"

    def test_template_with_date_formatting(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates([{"TEMPLATE": "[{studio}] {date:%Y.%m.%d}"}])
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "[Studio A] 2023.01.15"

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates([{"TEMPLATE": "[{studio}] {date:%y.%m.%d}"}])
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "[Studio A] 23.01.15"

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates([{"TEMPLATE": "[{studio}] {date:%b %d, %Y}"}])
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "[Studio A] Jan 15, 2023"

    def test_template_with_multiple_date_formatting(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [{"TEMPLATE": "{date:%Y} [{studio}] {date:%b}-{date:%d}"}]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "2023 [Studio A] Jan-15"

    def test_template_with_duration_formatting(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates([{"TEMPLATE": "[{studio}] {duration:%H.%M}"}])
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "[Studio A] 00.50"

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates([{"TEMPLATE": r"[{studio}] {duration:%X}"}])
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert renames[0]["dst_file_name"] == "[Studio A] 005030"

    def test_template_with_multiple_duration_formatting(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).build()
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [{"TEMPLATE": "{duration:%H} [{studio}] {duration:%M}"}]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1
        assert renames[0]["dst_file_name"] == "00 [Studio A] 50"
