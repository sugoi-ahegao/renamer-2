# --- *** TEMPLATE VARIABLES: *** ---
# Available for use in BOTH FILE NAME TEMPLATES and FILE DIR TEMPLATES

# - {title} - The title of the scene
#   - eg. "Filling Both Her Holes"

# - {studio} - The name of the studio of the scene, can be configured in the "STUDIOS_CONFIG" section
#   - eg. "Brazzers"

# - {parent_studio} - The name of the parent studio of the scene if it has one or {studio} if it does not, can be configured in the "STUDIOS_CONFIG" section
#   - eg. "Adult Time"

# - {studio_family} - The name of the top level studio of the scene if it has one or {studio} if it does not, can be configured in the "STUDIOS_CONFIG" section
#   - eg. "Bangbros"

# - {performers} - The performers in the scene, can be configured in the "PERFORMERS_CONFIG" section
#   - eg. "Abella Danger, Keisha Grey, Luna Star"

# - {date} - The date of the scene (default format is "%Y-%m-%d")
#   - {date:<date_format>} - The date of the scene with the specified date format (uses the same format as the python datetime.strftime() method)
#       - %Y - Year with century as a decimal number (2013, 2019, etc)
#       - %y - Year without century as a zero-padded decimal number (00, 01, ..., 99)
#       - %m - Month as a zero-padded decimal number (01, 02, ..., 12)
#       - %d - Day of the month as a zero-padded decimal (01, 02, ..., 31)
#       - %B - Full month name (January, February, ...)
#       - %b - Abbreviated month name (Jan, Feb, ..., Dec)
#       - many more... search "python strftime format" for more info
#   - eg. "{date}" -> "2021-01-15"
#   - eg. "{date:%Y.%m.%d}" -> "2021.01.15"
#   - eg. "{date:%B} {date:%d}, {date: %Y}" -> "January 15, 2021"

# - {resolution} - The resolution of the scene
#   - value: (video height)p -> "480p", "720p", "1080p", "1440p", "2160p", "2880p" etc
#   - eg. "480p"
#   - eg. "1080p"

# - {resolution_name} - The resolution of the scene
#   - values: (map height of video file to a name) - "SD", "HD", "FHD", "2k", "4k", "5k" etc
#   - eg. "SD" (video height >= 480)
#   - eg. "HD" (video height >= 720)
#   - eg. "FHD" (video height >= 1080)
#   - eg. "2k" (video height >= 1440)
#   - eg. "4k" (video height >= 2160)
#   - eg. "5k" (video height >= 2880)
#   - eg. "6k" (video height >= 3384)
#   - eg. "8k" (video height >= 4320)

# - {duration} - The duration of the scene (default format is "%H.%M.%S")
#   - {duration:<duration_format>} - The duration of the scene with the specified duration format (uses the same format as the python datetime.strftime() method)
#       - %H - Hour (24-hour clock) as a zero-padded decimal number (00, 01, ..., 23)
#       - %M - Minute as a zero-padded decimal number (00, 01, ..., 59)
#       - %S - Second as a zero-padded decimal number (00, 01, ..., 59)
#       - many more... search "python strftime format" for more info
#   - eg. "{duration:%H.%M.%S}" -> "01.15.30"

# - {bit_rate_mbps} - The bit rate of the scene in megabits per second
#   - eg. "6.16"

# - {rating} - The rating of the scene
#   - NOTE: This is the new "rating100" field of the scene
#   - possible values: "0", ..., "50", ..., "80", ..., "100"
#   - eg. "50"
#   - eg. "80"

# - {tags} - The tags of the scene, can be configured in the "TAGS_CONFIG" section
#   - eg. "Rough Sex, Bondage, Anal"

# - {video_codec} - The video codec of the video file
#   - eg. "h264"
#   - eg. "h265"

# - {audio_codec} - The audio codec of the video file
#   - eg. "aac"
#   - eg. "ac3"

# - {movie_scene_number} - The scene number of the scene in the movie (eg. 1, 2, 3, etc)
#   - eg. "1"

# - {movie_name} - The name of the movie of the scene
#   - eg. "Teens Like It Rough 2"

# - {movie_date} - The date of the movie of the scene (default format is "%Y-%m-%d")
#   - {movie_date:<date_format>} - The date of the movie of the scene with the specified date format (uses the same format as the python datetime.strftime() method)
#   - <date_format> is the same as the date format for the {date} variable
#   - eg. "{movie_date}" -> "2021-01-15"

# - {scene_stash_id} - The **first** value of the "stash ids" field of the scene
#   - eg. "064fc24e-7c6a-4757-8968-9972bd7060bc"

# - {oshash} - The oshash of the video file
#   - eg. "fdccbe33e1ce4a82"

# - {phash} - The phash of the video file
#   - eg. "c5176ad76b613560"

# - {performers_stash_ids} - The **first** value of the "stash ids" field of each performer in the scene
#   - eg. "c0386a4e-f58f-42d4-9676-c51276ad0cbc, a5c1f628-6c26-45ce-bbf0-79b37e955022"

# - {studio_code} - The studio code of the scene
#   - eg. "8659021"
#   - eg. "STARS-416"
#   - eg. "BB18053"

# -- Only available for use in the FILE DIR TEMPLATE --

# - {studio_hierarchy} - The studio hierarchy of the scene
#   - eg. Grand Parent Studio Name/Parent Studio Name/Studio Name

# - {src} - The src dir of the scene
#   - eg. r"C:\Users\Me\Downloads\Scene Name"

# --- NOTE: {studio} vs {parent_studio} vs {studio_family} Examples ---
# -----------------------------------------------------------------
# Studio D               <- {studio_family}
# └── Studio C
#     └── Studio B       <- {parent_studio}
#         └── Studio A   <- {studio}
# -----------------------------------------------------------------
# Studio C               <- {studio_family}
# └─ Studio B            <- {parent_studio}
#    └─ Studio A         <- {studio}
# -----------------------------------------------------------------
# Studio B               <- {parent_studio}, {studio_family}
# └─ Studio A            <- {studio}
# -----------------------------------------------------------------
# Studio A               <- {studio}, {parent_studio}, {studio_family}
# -----------------------------------------------------------------

# --- *** FILTER VARIABLES: *** ---
# Available for use in BOTH The FILE NAME TEMPLATE FILTERS and FILE DIR TEMPLATE FILTERS
# - matches_studio: <filter_value> - Matches all scenes that have a studio with the name <filter_value>. NOTE: Case sensitive
#   - eg. "Brazzers"
#   - eg. "Bangbros"
#
# - matches_part_of_studio: <filter_value> - Matches scenes whose studio is a part of <filter_value>. NOTE: Case sensitive
#   - eg. "Bangbros" - If the scene's studio is "Bangbros", it will match
#   - eg. "Brazzers" - If the scene's studio is "Big Wet Butts" and is a child of "Brazzers", it will match
#   - eg. "Adult Time (Network)" - If the scene's studio is "Modern-Day Sins" and is a child of "Adult Time Originals" which is a child of "Adult Time (Network)", it will match
#
# - matches_all_tags: <filter_value> - Matches all scenes that have ALL of the tags in <filter_value>. NOTE: Case sensitive
#   - eg. ["Rough Sex", "Bondage"]
#   - eg. ["Gangbang"]
#
# - matches_any_tags: <filter_value> - Matches all scenes that have ANY of the tags in <filter_value>. NOTE: Case sensitive
#   - eg. ["Teen", "MILF"]
#
# - matches_organized_value: <filter_value> - For differentiating between organized and unorganized scenes
#   - possible values: True, False
#   - If <filter_value> is True, This filter will matches all scenes that are organized
#   - If <filter_value> is False, This filter will match all scenes that are NOT organized
#
# - matches_scene_with_no_performers: <filter_value> - For differentiating between scenes that have no performers and scene that have at least one
#   - possible values: True, False
#   - If <filter_value> is True, This filter will match all scenes that have NO performers
#   - If <filter_value> is False, This filter will match all scenes that have at least one performer

# -- Only available for use in the FILE DIR TEMPLATE FILTERS --

# - matches_src: <filter_value> - Matches all scene files that are in the src dir <filter_value> including nested directories
#   - eg. "C:\Users\Me\New Scenes" -> Matches "C:\Users\Me\New Scenes\Scene 1.mp4" and also matches "C:\Users\Me\New Scenes\Nested Dir\Scene 2.mp4"

config = {
    "ENABLE_HOOK": True,  # If set to True, this script will run after a scene is created or updated
    "DRYRUN_ENABLED": True,  # If set to True, it will NOT move or rename any files, it will only print the actions that would be performed
    "LOGGING_CONFIG": {
        "LOG_FILE": "C:\\User\\Desktop\\STASH\\stash_organize.log",  # If set to None, it will not log to a file
        "LOG_LEVEL": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        "OVERRIDE_LOG_FILE": True,  # If set to True, it will override the log file if it already exists, if set to False, it will append to the log file
    },
    "FILE_NAME_CONFIG": {
        "FILE_NAME_TEMPLATES": [
            # Templates for the NAME of the file
            # NOTE: The order of the templates is important, the first template that matches the scene will be used
            ## {
            ##   "{filter}": {filter value} <- optional, if you do not have a filter, it will match all scenes
            ##   "TEMPLATE": {template for file name of filtered files} <- REQUIRED, the template for the file name
            ## }
            # Examples:
            # {
            #     # fmt: off
            #     "matches_studio": "Bang Bus",                       # Make sure the studio "Bang Bus"
            #     "matches_part_of_studio": "Bangbros",               # Make sure the scene is part of the studio "Bangbros"
            #     "matches_all_tags": [ "Doggy Style", "Amateur", ],  # Make sure the scene has both "Doggy Style" and "Amateur" tags
            #     "matches_any_tags": [ "Small Ass", "Small Tits", ], # Make sure the scene has a "Small Ass" tag or a "Small Tits" tag or both tags
            #     "matches_organized_value": True,                    # Make sure scene is organized
            #     "matches_scene_with_no_performers": False,          # Make sure scene has at least one performer
            #     # The filters above match this scene from stashdb: https://stashdb.org/scenes/22499e1d-ee9a-4cab-ac77-3f2140c9cfc0
            #     # Assuming the scene is organized in your stash and the video file is 1080p...
            #     # Also assuming that the Studio Config, Title Config, Performers Configs are the default...
            #     # The following template would resolve to "[Bang Bus] 2021-03-03 Valentines Date on the Bus -- Angel Aurora, Peter Green (1080p)"
            #     "TEMPLATE": "[{studio}] {date} {title} -- {performers} ({resolution})",
            #     # fmt: on
            # },
            # {
            #     "matches_organized_value": False,  # Match scenes that are NOT organized
            #     "TEMPLATE": "[{studio}] {date} {title} -- {performers} ({resolution})",  # Now rename them to using the same template as above
            # },
            {
                # DEFAULT TEMPLATE - This will match all scenes since there are no filters (eg. matches_studio, matches_all_tags, etc)
                # Make sure to put this default template at the end of the list, otherwise it will match all scenes
                # if you do not want to have a default template, remove this item or comment it out
                # if you do not have a default template, and the scene does not match any of the other templates filters, the file will NOT be moved
                # Recommend: At least using the "matches_organized_value: False" filter to make sure only unorganized scenes are moved
                "TEMPLATE": "{date} {title} -- {performers} ({resolution})",
            },
        ],
        "POST_FILE_NAME_TEMPLATE_CONFIG": {
            # configuration of the file name after the template has been applied
            # ORDER in which the following operations are performed: REPLACE, REPLACE_WHITESPACE, TRANSFORM, DUPLICATE_SUFFIX
            "REPLACE": {
                # NOTE: case sensitive
                "#": "",  # removes all the '#' characters
            },
            "REPLACE_WHITESPACE": " ",  # replace all the whitespace with a value, e.g. " " or "_" or "-" or "."
            "TRANSFORM": None,  # Transforms the file name. possible values: "lowercase", "titlecase" (Capitalizes each letter after a whitespace)
        },
    },
    "FILE_DIR_CONFIG": {
        "FILE_DIR_TEMPLATES": [
            # Templates for the destination DIR (aka folder) of the file
            # Works the exact same as the FILE_NAME_CONFIG, except the TEMPLATE is the destination DIR...
            # ...And you can use more filters (eg. matches_src) and template variables (eg. {src}, {studio_hierarchy})
            # NOTE: The order of the templates is important, the first template that matches the scene will be used
            {
                # fmt: off
                "matches_src": "C:\\User\\Desktop\\New Scenes",  # matches all scenes in C:\User\Desktop including subdirectories eg. C:\User\Desktop\New Scenes\Nested Folder\video.mp4 will also be matched
                
                # The following filters work the same as the filters in the FILE_NAME_CONFIG
                "matches_studio": "Bang Bus",                       # Match the studio "Bang Bus"
                "matches_part_of_studio": "Bangbros",               # Match the scene is part of the studio "Bangbros"
                "matches_all_tags": [ "Doggy Style", "Amateur", ],  # Make sure the scene has both "Doggy Style" and "Amateur" tags
                "matches_any_tags": [ "Small Ass", "Small Tits", ], # Make sure the scene has a "Small Ass" tag or a "Small Tits" tag or both tags
                "matches_organized_value": True,                    # Make sure scene is organized
                "matches_scene_with_no_performers": False,          # Make sure scene has at least one performer
                
                # Any scene that matches the above filters will be moved to "C:\User\Desktop\STASH"
                "TEMPLATE": "C:\\User\\Desktop\\STASH",
                # fmt: on
            },
            # {
            # NOTE: you cannot use the same filter twice in one
            # Example:
            # "matches_all_tags": ["Pawg"],
            # "matches_all_tags": ["Deepthroat"] # This filter will override the previous "matches_all_tags": ["Pawg"] filter
            # }
            {
                # DEFAULT TEMPLATE - This will match any scene since there are no filters eg. marches_src, matches_studio, etc.
                # Works the same as FILE_NAME_CONFIG
                # if you do not want to have a default template, remove this item or comment it out
                # if you do not have a default template, and the scene does not match any of the other templates, the file will NOT be moved
                "TEMPLATE": "C:\\User\\Desktop\\STASH\\{studio_hierarchy}",
            },
        ],
        "POST_DIR_TEMPLATE_CONFIG": {
            # configuration of the file dir path after the template has been applied
            # If set to True, it will prevent duplicate nested directories from being created
            # ie if the processed template is "C:\Studio A\Studio A\video.mp4", then it will be changed to "C:\Studio A\video.mp4"
            "PREVENT_CONSECUTIVE_NESTED_DIRS": True,
        },
    },
    "TEMPLATE_VARIABLES_CONFIG": {
        "PERFORMERS_CONFIG": {
            # Configuration of the {performers} variable in the file name
            # ORDER in which the following operations are performed: NO_PERFORMER_NAME, ORDER_BY, EXCLUDE_GENDERS, LIMIT, SEPARATOR
            # The max number of performers to include in the performers list. ie if LIMIT is 3 and there are 5 performers, then only the first 3 performers will be included in the list
            "LIMIT": 3,
            # The separator to use between performers in the performers list. ie if SEPARATOR is ", " then the list will be "performer1, performer2, performer3"
            "SEPARATOR": ", ",
            # A list of genders to exclude from the performers list. possible values: "MALE", "FEMALE", "TRANSGENDER_MALE", "TRANSGENDER_FEMALE", "INTERSEX", "NON_BINARY", "UNDEFINED"
            "EXCLUDE_GENDERS": [],
            # Order in which the performers are listed in the performers list. possible values: "name", "id"
            "ORDER_BY": "id",
            # If set to True, then if the LIMIT is exceeded, then the {performers} value will be empty
            # ie if LIMIT is 3 and there are 5 performers (after filtering genders), then the {performers} value will be empty (even if NO_PERFORMER_NAME is set)
            "REMOVE_ALL_PERFORMERS_IF_LIMIT_EXCEEDED": False,
            # Default {performers} value if there are no performers
            # NOTE: This is only used if there are strictly no performers in the scene. If the performers are filtered out using LIMIT or EXCLUDE_GENDERS, then the {performers} value will be empty.
            "NO_PERFORMER_NAME": "No Performers",
        },
        "TITLE_CONFIG": {
            # configuration of the {title} variable in the file name
            # ORDER in which the following operations are performed: REPLACE, REPLACE_FROM_BEGINNING
            "REPLACE": {
                # NOTE: Case sensitive
                "'": "",  # remove apostrophes, e.g. "My Stepsister's a Slut" -> "My Stepsisters a Slut"
            },
            "REPLACE_FROM_BEGINNING": {
                # NOTE: Case insensitive
                "The": "",  # remove 'The' from the beginning, e.g. "The Gangbang of The Office Boss" -> "Gangbang of The Office Boss"
                "A": "",
                "An": "",
            },
        },
        "STUDIO_CONFIG": {
            # configuration of the {studio}, {parent_studio}, {studio_family}, and {studio_hierarchy} variables in the file name
            "SQUEEZE_STUDIO_NAME": False  # If set to True, it will remove spacing between the studio name and capitalize
        },
        "TAGS_CONFIG": {
            # configuration of the {tags} variable
            # NOTE: Tags are compared strictly and case sensitive, "pantyhose" != "Pantyhose" and "panty hose" != "pantyhose"
            "SEPARATOR": " ",  # separator between tags
            "USE": "WHITELIST",  # "WHITELIST" or "BLACKLIST" or "NONE" to keep all tags (NOTE: "NONE" is not recommended as it may make the path too long)
            "WHITELIST": [],  # if set to a non-empty list, only tags in this list will be included in the file name
            "BLACKLIST": [],  # if set to a non-empty list, tags in this list will be excluded from the file name
        },
    },
    "ASSOCIATED_FILES": [
        # List of file extensions that are associated with the video file
        # if a file is found with the same name as the video file, in the same folder but with one of these extensions, it will move it to the same folder as the video file and given the same (new) name as the video file
        "srt",
        "vtt",
        "funscript",
    ],
    "POST_PROCESSING": {
        "DELETE_EMPTY_FOLDERS": True,  # If set to True, it will delete empty folders after the files have been moved
    },
    "PATH_CONFIG": {
        "MAX_PATH_LENGTH": 240,  # If the resulting path is longer than this value, it will be skipped and the file will not be moved. If set to None, it will not be checked.
        # NOTE: the duplicate suffix operation is performed only if the file already exists
        # NOTE: the {num} variable is replaced with the number of the duplicate and is incremented until the file does not exist
        # NOTE: the {num} variable is only available in the DUPLICATE_SUFFIX
        "DUPLICATE_SUFFIX_TEMPLATE": " ({num})",  # suffix to add to the file name if the file already exists
        "TEMPLATE_VARIABLE_REMOVAL_ORDER": [
            # If the resulting path is longer than the MAX_PATH_LENGTH, the following fields are removed one at a time in order from the FILE_NAME Template (not FILE_DIR Template) until the path is short enough
            "{video_codec}",
            "{audio_codec}",
            "{tags}",
            "{rating}",
            "{resolution}",
            "{resolution_name}",
            "{parent_studio}",
            "{studio}",
            "{performers}",
        ],
    },
}
