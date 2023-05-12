# Welcome to Renamer-2

## What is Renamer-2?

Renamer-2 is built to improve upon [renamerOnUpdate](https://github.com/stashapp/CommunityScripts/tree/main/plugins/renamerOnUpdate) by adding a more powerful, intuitive way to configure renaming rules. It is also built to be more performant than renamerOnUpdate.

## How do I use Renamer-2?

1. Install dependencies by running `pip install -r requirements.txt` (NOTE: TODO)
2. Add the entire `renamer-2` folder to your Stash `plugins` folder
3. Restart Stash or click the `reload plugins` button on your Stash to load the plugin
4. Add your own config by modifying [user_config.py](./src/user_config.py)
   1. Make sure you set `ENABLE_DRYRUN` to `True` to test your config before running it for real
   2. See the [user config demo](./src/user_config_demo.py) for examples of how to configure your own rules

## Features Planned for Future Releases

- [ ] Add support for configuring logging
- [ ] Add support to configure the `ENABLE_RENAME_ON_UPDATE` flag from the Stash UI
- [ ] Add support to configure the `ENABLE_DRYRUN` flag from the Stash UI
- [ ] Add support for `FILE_NAME_CONFIG/POST_FILE_NAME_TEMPLATE_CONFIG` configuration
- [ ] Add support for `FILE_DIR_CONFIG/POST_FILE_DIR_TEMPLATE_CONFIG` configuration
- [ ] Add support for `TEMPLATE_VARIABLES_CONFIG/TITLE_CONFIG` configuration
- [ ] Add support for `TEMPLATE_VARIABLES_CONFIG/STUDIO_CONFIG` configuration
- [ ] Add support for `TEMPLATE_VARIABLES_CONFIG/TAGS_CONFIG` configuration
- [ ] Add support for `ASSOCIATED_FILES` - to be able to rename associated files
