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
