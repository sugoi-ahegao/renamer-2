from pathlib import Path
from models.scene import SceneFile


class SceneFileBuilder:
    def __init__(self, id: str):
        self.scene_file_dict = {
            "id": id,
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

    def with_file_path(self, file_path_str: str):
        file_path = Path(file_path_str)

        self.scene_file_dict["path"] = str(file_path)
        self.scene_file_dict["basename"] = file_path.name

        return self

    def build_dict(self):
        return self.scene_file_dict

    def build(self):
        return SceneFile(**self.scene_file_dict)
