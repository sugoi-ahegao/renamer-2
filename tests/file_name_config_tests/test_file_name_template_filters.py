import pytest
from pytest_mock import MockerFixture

from models.studio import Studio
from test_utils.config_builder import ConfigBuilder
from test_utils.helpers import run_renamer_with_mock
from test_utils.scene_builder import SceneBuilder


class TestFileNameTemplateFilters:
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

    def test_filter_matches_studio(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        studio_bangbros = Studio(**{"id": 1, "name": "Bangbros"})

        studios = [studio_bangbros]

        scene = SceneBuilder(base_scene).with_studio(studio_bangbros.dict()).build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [{"matches_studio": "Bangbros", "TEMPLATE": "Scene {id} - {title}"}]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

    def test_filter_matches_studio_negative(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        studio_bangbros = Studio(**{"id": 1, "name": "Bangbros"})
        studio_random = Studio(**{"id": 2, "name": "Random Studio"})

        studios = [studio_bangbros, studio_random]

        scene = SceneBuilder(base_scene).with_studio(studio_bangbros.dict()).build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_studio": studio_random.name,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_filter_matches_all_tags(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_tags(["rough sex", "big ass", "facial"])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_all_tags": ["rough sex"],
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_all_tags": ["rough sex", "big ass"],
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_all_tags": ["rough sex", "big ass", "facial"],
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

    def test_filter_matches_all_tags_negative(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_tags(["rough sex", "big ass", "face fuck"])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_all_tags": ["hentai", "magical girls"],
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_filter_matches_part_of_studio(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        # Setup Studios
        studio_bangbros = Studio(**{"id": 1, "name": "Bangbros"})
        studio_ass_parade = Studio(**{"id": 2, "name": "Ass Parade"})
        studio_random = Studio(**{"id": 3, "name": "Random"})

        studio_ass_parade.parent_studio = studio_bangbros
        studio_random.parent_studio = studio_ass_parade

        studios = [studio_bangbros, studio_ass_parade, studio_random]

        # Setup Config
        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_part_of_studio": studio_bangbros.name,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        # Setup scene with grandparent studio
        scene = SceneBuilder(base_scene).with_studio(studio_bangbros.dict()).build()

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        # Setup scene with parent studio
        scene = SceneBuilder(base_scene).with_studio(studio_ass_parade.dict()).build()

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        # Setup scene with child studio
        scene = SceneBuilder(base_scene).with_studio(studio_random.dict()).build()

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

    def test_filter_matches_part_of_studio_negative(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        studio_deeper = Studio(**{"id": 1, "name": "Deeper"})
        studio_random = Studio(**{"id": 2, "name": "Random"})

        studios = [studio_deeper, studio_random]

        scene = SceneBuilder(base_scene).with_studio(studio_deeper.dict()).build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_studio": studio_random.name,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_filter_matches_organized_value_with_organized_scene(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).organized().build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_organized_value": True,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_organized_value": False,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_filter_matches_organized_value_with_unorganized_scene(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).not_organized().build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_organized_value": True,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_organized_value": False,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

    def test_filter_matches_scene_with_no_performers_with_scene_with_no_performers(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).with_performers([]).build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_scene_with_no_performers": True,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_scene_with_no_performers": False,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_filter_matches_scene_with_no_performers_with_scene_with_1_performer(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = (
            SceneBuilder(base_scene)
            .with_performers([{"id": 1, "name": "Violet Myers"}])
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_scene_with_no_performers": True,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_scene_with_no_performers": False,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

    def test_same_filter_twice_for_one_template_negative(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        scene = SceneBuilder(base_scene).with_tags(["pawg"]).build()

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_all_tags": ["pawg"],
                        # The following filter overrides the above "matches_all_tags": ["pawg"] filter
                        "matches_all_tags": ["deepthroat"],
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        studios = [scene.studio] if scene.studio else []

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

        scene = SceneBuilder(base_scene).with_tags(["deepthroat"]).build()

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        scene = SceneBuilder(base_scene).with_tags(["pawg", "deepthroat"]).build()

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

    def test_multiple_filters_for_one_template(
        self, base_scene: dict, base_config: dict, mocker: MockerFixture
    ):
        studio_adult_time_network = Studio(**{"id": 1, "name": "Adult Time Network"})

        studio_adult_time_originals = Studio(
            **{"id": 2, "name": "Adult Time Originals"}
        )
        studio_girls_under_arrest = Studio(
            **{
                "id": 3,
                "name": "Girls Under Arrest",
            }
        )

        studio_girls_under_arrest.parent_studio = studio_adult_time_originals
        studio_adult_time_originals.parent_studio = studio_adult_time_network

        studios = [
            studio_adult_time_network,
            studio_adult_time_originals,
            studio_girls_under_arrest,
        ]

        scene = (
            SceneBuilder(base_scene)
            .with_studio(studio_girls_under_arrest.dict())
            .with_tags(["Police Officer", "Uniform", "Family Roleplay"])
            .with_performers([{"id": 1, "name": "Violet Myers"}])
            .organized()
            .build()
        )

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_studio": "Girls Under Arrest",
                        "matches_part_of_studio": "Adult Time Network",
                        "matches_all_tags": ["Police Officer", "Uniform"],
                        "matches_scene_with_no_performers": False,
                        "matches_organized_value": True,
                        "TEMPLATE": "Scene {id} - {title}",
                    }
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 1

        # Same scene, but not organized

        new_scene = SceneBuilder(scene.dict()).not_organized().build()

        renames = run_renamer_with_mock(mocker, config, [new_scene], studios)

        assert len(renames) == 0

        # Scene scene, but different studio

        new_scene = (
            SceneBuilder(scene.dict())
            .with_studio(studio_adult_time_originals.dict())
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, [new_scene], studios)

        assert len(renames) == 0

        # Same scene, but with no performers

        new_scene = SceneBuilder(scene.dict()).with_performers([]).build()

        renames = run_renamer_with_mock(mocker, config, [new_scene], studios)

        assert len(renames) == 0

        # Same scene, but with different tags

        new_scene = SceneBuilder(scene.dict()).with_tags(["Police Officer"]).build()

        renames = run_renamer_with_mock(mocker, config, [new_scene], studios)

        assert len(renames) == 0

        # Run the original test again but change the parent studio
        studio_girls_under_arrest.parent_studio = None

        renames = run_renamer_with_mock(mocker, config, [scene], studios)

        assert len(renames) == 0

    def test_mixed_filters_for_multiple_templates(
        self, base_config: dict, base_scene: dict, mocker: MockerFixture
    ):
        studio_adult_time_network = Studio(**{"id": 1, "name": "Adult Time Network"})

        studio_adult_time_originals = Studio(
            **{"id": 2, "name": "Adult Time Originals"}
        )
        studio_girls_under_arrest = Studio(
            **{
                "id": 3,
                "name": "Girls Under Arrest",
            }
        )

        studio_girls_under_arrest.parent_studio = studio_adult_time_originals
        studio_adult_time_originals.parent_studio = studio_adult_time_network

        studios = [
            studio_adult_time_network,
            studio_adult_time_originals,
            studio_girls_under_arrest,
        ]

        scenes = [
            (
                SceneBuilder(base_scene)
                .organized()
                .with_studio(studio_girls_under_arrest.dict())
                .build()
            ),
            (
                SceneBuilder(base_scene)
                .organized()
                .with_studio(studio_girls_under_arrest.dict())
                .with_tags(["Police Officer", "Uniform"])
                .build()
            ),
            (SceneBuilder(base_scene).not_organized().build()),
        ]

        config = (
            ConfigBuilder(base_config)
            .with_file_name_templates(
                [
                    {
                        "matches_organized_value": True,
                        "matches_all_tags": ["Uniform"],
                        "TEMPLATE": "Scene {id} - {title} (Uniform)",
                    },
                    {
                        "matches_organized_value": True,
                        "matches_studio": "Girls Under Arrest",
                        "TEMPLATE": "[Girls Under Arrest] Scene {id} - {title} (organized)",
                    },
                    {
                        "TEMPLATE": "Scene {id} - {title}",
                    },
                ]
            )
            .build()
        )

        renames = run_renamer_with_mock(mocker, config, scenes, studios)

        assert len(renames) == 3
