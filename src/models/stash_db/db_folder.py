from typing import Optional


class DBFolder:
    def __init__(
        self,
        id: int,
        path: str,
        parent_folder_id: int,
        mod_time: str,
        created_at: str,
        updated_at: str,
        zip_file_id: Optional[int],
    ):
        self.id = id
        self.path = path
        self.parent_folder_id = parent_folder_id
        self.mod_time = mod_time
        self.created_at = created_at
        self.updated_at = updated_at
        self.zip_file_id = zip_file_id

    @staticmethod
    def from_db_row(row: tuple):
        return DBFolder(
            id=row[0],
            path=row[1],
            parent_folder_id=row[2],
            mod_time=row[3],
            created_at=row[4],
            updated_at=row[5],
            zip_file_id=row[6],
        )

    def __str__(self):
        return f"DBFolder(id={self.id}, path={self.path}, parent_folder_id={self.parent_folder_id}, mod_time={self.mod_time}, created_at={self.created_at}, updated_at={self.updated_at}, zip_file_id={self.zip_file_id})"
