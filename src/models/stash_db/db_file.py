class DBFile:
    def __init__(
        self,
        id: int,
        basename: str,
        zip_file_id: int,
        parent_folder_id: int,
        mod_time: str,
    ):
        self.id = id
        self.basename = basename
        self.zip_file_id = zip_file_id
        self.parent_folder_id = parent_folder_id
        self.mod_time = mod_time

    @staticmethod
    def from_db_row(row: tuple):
        return DBFile(
            id=row[0],
            basename=row[1],
            zip_file_id=row[2],
            parent_folder_id=row[3],
            mod_time=row[5],
        )

    def __str__(self):
        return f"DBFile(id={self.id}, basename={self.basename}, zip_file_id={self.zip_file_id}, parent_folder_id={self.parent_folder_id}, mod_time={self.mod_time})"
