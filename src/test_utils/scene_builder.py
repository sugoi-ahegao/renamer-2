from typing import Optional

from models.scene import Scene
from models.studio import Studio


class SceneBuilder:
    def __init__(self, scene_dict: Optional[dict] = None):
        if scene_dict is None:
            scene_dict = {}

        default_scene_dict = {
            "id": 1,
            "title": "Scene Title",
            "organized": False,
            "date": "2021-01-01",
            "studio": {"id": 1, "name": "Studio A"},
            "performers": [],
            "tags": [],
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
                }
            ],
            "movies": [],
            "stash_ids": [],
        }

        self.scene_dict = {**default_scene_dict, **scene_dict}

    def with_performers(self, performers: list[dict]):
        default_performer_dict = {"favorite": False, "stash_ids": []}

        self.scene_dict["performers"] = [
            {**default_performer_dict, **performer} for performer in performers
        ]

        return self

    def with_studio(self, studio: dict | None):
        self.scene_dict["studio"] = studio
        return self

    def with_title(self, title: str):
        self.scene_dict["title"] = title
        return self

    def with_files(self, files: list[dict]):
        self.scene_dict["files"] = files

        return self

    def with_tags(self, tag_names: list[str]):
        self.scene_dict["tags"] = [
            {"name": tag_name, "id": id} for id, tag_name in enumerate(tag_names, 1)
        ]

        return self

    def organized(self):
        self.scene_dict["organized"] = True

        return self

    def not_organized(self):
        self.scene_dict["organized"] = False

        return self

    def build_dict(self):
        return self.scene_dict

    def build(self):
        return Scene(**self.scene_dict)
