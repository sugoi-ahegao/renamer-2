import logging

import pydantic
import requests

import components.setup_logging
from models.config import get_config
from models.scene import Scene
from models.studio import Studio

logger = logging.getLogger(__name__)


class StashGraphQL:
    def __init__(self, graphql_url: str):
        self.graphql_url = graphql_url
        self.test_connection()

    def test_connection(self):
        try:
            version = self.get_stash_version()
            logger.info("Connected to Stash GraphQL API (version: %s)", version)
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Stash GraphQL API", exc_info=True)

    def get_stash_version(self):
        query = """
            query StashVersion {
                version {
                    version
                }
            }
        """
        response = self._send_request(query)
        return response["version"]["version"]

    def get_configuration(self):
        query = """
            query Configuration {
                configuration {
                    general {
                        databasePath
                    }
                }
            }
        """

        response = self._send_request(query)
        return response

    def get_all_studios(self):
        query = """
            query GetAllStudios($filter: FindFilterType) {
                findStudios(filter: $filter) {
                    count
                    studios {
                        id
                        name
                        parent_studio {
                            id
                            name
                        }
                    }
                }
            }
        """

        variables = {
            "filter": {
                "direction": "DESC",
                "page": 1,
                "per_page": -1,  # Get all
                "sort": "updated_at",
            }
        }

        response = self._send_request(query, variables)

        studios = []
        for studio_dict in response["findStudios"]["studios"]:
            studios.append(Studio(**studio_dict))

        return studios

    def get_all_scenes(self):
        query = (
            """
          query GetAllScenes($filter:FindFilterType) {
                findScenes(filter: $filter) {
                    count
                    scenes {
                        ...Scene_Data
                    }
                }
            }
        """
            + SCENE_DATA_FRAGMENT
        )

        variables = {
            "filter": {
                "direction": "DESC",
                "page": 1,
                "per_page": -1,  # per_page: -1 -> means Get all
                "sort": "updated_at",
            }
        }

        response = self._send_request(query, variables)

        scenes = []
        for scene_dict in response["findScenes"]["scenes"]:
            try:
                scenes.append(Scene(**scene_dict))
            except pydantic.error_wrappers.ValidationError as e:
                logger.error("Error parsing scene: %s", scene_dict, exc_info=True)

        logger.info("Found %s scenes", len(scenes))
        return scenes

    def get_scene_with_id(self, scene_id: int):
        query = (
            """
            query FindScene($id: ID!, $checksum: String) {
                findScene(id: $id, checksum: $checksum) {
                    ...Scene_Data
                }
                
            }
            """
            + SCENE_DATA_FRAGMENT
        )

        variables = {"id": scene_id}

        response = self._send_request(query, variables)
        return Scene(**response["findScene"])

    def _send_request(self, query, variables=None):
        body = {"query": query, "variables": variables}

        response = requests.post(self.graphql_url, json=body)
        return response.json().get("data")


SCENE_DATA_FRAGMENT = """
fragment Scene_Data on Scene {
    id
    title
    date
    rating100
    stash_ids {
        endpoint
        stash_id
    }
    organized
    files {
        id
        path
        video_codec
        audio_codec
        width
        height
        frame_rate
        duration
        bit_rate
        basename
        mod_time
        created_at
        updated_at
        parent_folder_id
        fingerprints {
            type
            value
        }
    }
    studio {
        id
        name
        parent_studio {
            id
            name
        }
    }
    tags {
        id
        name
    }
    performers {
        id
        name
        gender
        favorite
        rating100
        stash_ids {
            endpoint
            stash_id
        }
    }
    movies {
        movie {
            id
            name
            date
        }
        scene_index
    }
}
"""
