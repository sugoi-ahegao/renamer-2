import datetime
import logging
import sqlite3
from pathlib import Path

import components.setup_logging
from models.scene import Scene, SceneFile
from models.stash_db.db_file import DBFile
from models.stash_db.db_folder import DBFolder

logger = logging.getLogger(__name__)


def get_curr_time():
    return datetime.datetime.now().astimezone().isoformat("T", "seconds")


class StashDB:
    def __init__(self, sqlite_path: str, dryrun_enabled: bool = True):
        self.dryrun_enabled = dryrun_enabled

        if self.dryrun_enabled:
            return

        self._connect(sqlite_path)

    def _connect(self, sqlite_path: str):
        if self.dryrun_enabled:
            raise ValueError("Cannot connect to database when dryrun is enabled")

        try:
            self.conn = sqlite3.connect(sqlite_path)
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            raise ConnectionError(
                f"Error connecting to database. Path: {sqlite_path}, {e}"
            )

    def rename(self, file: SceneFile, new_file_path: str):
        if self.dryrun_enabled:
            logger.debug(
                f"[DRYRUN] [STASH-DB] Renaming file: '{file.path}' --> '{new_file_path}'"
            )
            return

        logger.debug(f"[STASH-DB] Renaming file: '{file.path}' --> '{new_file_path}'")

        # new file folder is the parent folder of the new file path
        parent_folder_path = str(Path(new_file_path).resolve().parent)

        parent_folder_id = self._get_or_create_db_folder(parent_folder_path).id

        new_file_basename = Path(new_file_path).name

        self._update_db_file_path(file, new_file_basename, parent_folder_id)

    def _get_or_create_db_folder(self, folder_path: str):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")

        # use resolve to get the absolute path (in case the path is relative)
        folder_path = str(Path(folder_path).resolve())

        if (
            parent_db_folder := self._find_db_folder_with_path(folder_path)
        ) is not None:
            logger.debug(
                f"[STASH-DB] Found file's folder: (folder_id={parent_db_folder.id}) '{parent_db_folder.path}'"
            )
            return parent_db_folder

        # At this point, since the folder does not exist in stash db, we need to create the folder in the database

        # Find the parent folder of the folder we will create in the database
        curr_folder_path = str(Path(folder_path))
        while True:
            curr_parent_folder_path = str(Path(curr_folder_path).parent)

            if curr_parent_folder_path == curr_folder_path:
                logger.error(
                    f"Could not find parent folder in stash db for '{folder_path}'"
                )
                raise ValueError(
                    f"You need to setup a library with the new location ({folder_path}) and scan at least 1 file"
                )

            parent_db_folder = self._find_db_folder_with_path(curr_parent_folder_path)

            if parent_db_folder is not None:
                logger.debug(
                    f"[STASH-DB] Found parent folder of file's folder: (parent_folder_id={parent_db_folder.id}) '{parent_db_folder.path}'"
                )
                break

            curr_folder_path = curr_parent_folder_path

        # now we have the parent folder in the database -> db_folder, so we can create the new folder in the database
        return self._insert_db_folder(folder_path, parent_db_folder.id)

    def _find_db_folder_with_path(self, path: str):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")
        result = self.cursor.execute("SELECT * FROM folders WHERE path = ?", (path,))
        row = result.fetchone()

        if row is None:
            return None

        return DBFolder.from_db_row(row)

    def _find_db_folder_with_id(self, id: int):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")
        result = self.cursor.execute("SELECT * FROM folders WHERE id = ?", (id,))
        row = result.fetchone()

        if row is None:
            return None

        return DBFolder.from_db_row(row)

    def _find_db_file_with_id(self, file_id: int):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")

        result = self.cursor.execute("SELECT * FROM files WHERE id = ?", (file_id,))
        row = result.fetchone()

        if row is None:
            return None

        return DBFile.from_db_row(row)

    def _get_new_db_folder_id(self):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")

        result = self.cursor.execute("SELECT MAX(id) FROM folders")
        max_id = result.fetchone()[0]

        return max_id + 1

    def _insert_db_folder(self, path: str, parent_folder_id: int):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")

        logger.debug(f"[Stash-DB] Creating folder: '{path}'")

        result = self.cursor.execute(
            "INSERT INTO folders (path, parent_folder_id, mod_time, created_at, updated_at, zip_file_id) VALUES (?, ?, ?, ?, ?, ?)",
            (
                path,
                parent_folder_id,
                get_curr_time(),
                get_curr_time(),
                get_curr_time(),
                None,
            ),
        )

        self.conn.commit()

        assert result.lastrowid is not None

        logger.debug(
            f"[Stash-DB] Created folder: (folder_id={result.lastrowid}) (parent_folder_id={parent_folder_id}) '{path}'"
        )

        inserted_folder = self._find_db_folder_with_id(result.lastrowid)

        assert inserted_folder is not None

        return inserted_folder

    def _update_db_file_path(
        self, file: SceneFile, new_file_basename: str, parent_folder_id: int
    ):
        if self.dryrun_enabled:
            raise ValueError("Cannot perform database operation when dryrun is enabled")

        logger.debug(
            f"[Stash-DB] Updating stash db file: (file_id={file.id}) (curr_parent_folder_id={file.parent_folder_id}) '{file.basename}' --> (new_parent_folder_id={parent_folder_id}) '{new_file_basename}'"
        )
        self.cursor.execute(
            "UPDATE files SET basename = ?, parent_folder_id = ?, mod_time = ? WHERE id = ?",
            (new_file_basename, parent_folder_id, get_curr_time(), file.id),
        )

        self.conn.commit()

        logger.debug(f"[Stash-DB] File updated")
