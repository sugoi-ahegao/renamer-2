from typing import Optional

from models.config import Config


class ConfigBuilder:
    def __init__(self, config_dict: Optional[dict] = None):
        if config_dict is None:
            config_dict = {}

        default_config_dict = {
            "DRYRUN_ENABLED": True,
            "STASH_API_GRAPHQL_URL": "https://stash.example.com/graphql",
            "STASH_SQLITE_DATABASE_PATH": R"C:\Users\user\AppData\Roaming\Stash\stash.db",
            "FILE_NAME_CONFIG": {
                "FILE_NAME_TEMPLATES": [
                    {
                        "TEMPLATE": "[{studio}] {date} {title} -- {performers} ({resolution})"
                    }
                ]
            },
            "FILE_DIR_CONFIG": {
                "FILE_DIR_TEMPLATES": [
                    {
                        "TEMPLATE": R"C:\User\Desktop\STASH",
                    }
                ]
            },
            "TEMPLATE_VARIABLES_CONFIG": {},
            "PATH_CONFIG": {"MAX_PATH_LENGTH": 240},
        }

        self.config_dict = {**default_config_dict, **config_dict}

    def with_file_name_templates(self, file_name_templates: list[dict]):
        self.config_dict["FILE_NAME_CONFIG"][
            "FILE_NAME_TEMPLATES"
        ] = file_name_templates

        return self

    def with_file_dir_templates(self, file_name_templates: list[dict]):
        self.config_dict["FILE_DIR_CONFIG"]["FILE_DIR_TEMPLATES"] = file_name_templates

        return self

    def with_performers_config(self, performers_config: dict):
        self.config_dict["TEMPLATE_VARIABLES_CONFIG"][
            "PERFORMERS_CONFIG"
        ] = performers_config

        return self

    def update_performers_config(self, performers_config: dict):
        self.config_dict["TEMPLATE_VARIABLES_CONFIG"]["PERFORMERS_CONFIG"].update(
            performers_config
        )

        return self

    def with_max_path_len(self, max_path_len: Optional[int]):
        self.config_dict["PATH_CONFIG"]["MAX_PATH_LENGTH"] = max_path_len

        return self

    def with_duplicate_suffix_template(self, duplicate_suffix_template: str):
        self.config_dict["PATH_CONFIG"][
            "DUPLICATE_SUFFIX_TEMPLATE"
        ] = duplicate_suffix_template

        return self

    def with_template_variable_removal_order(
        self, template_variable_removal_order: list[str]
    ):
        self.config_dict["PATH_CONFIG"][
            "TEMPLATE_VARIABLE_REMOVAL_ORDER"
        ] = template_variable_removal_order

        return self

    def build(self):
        return Config(**self.config_dict)

    def build_dict(self):
        return self.config_dict
