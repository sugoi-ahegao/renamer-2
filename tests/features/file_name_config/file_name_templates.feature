Feature: File Name Config

Background:
  Given scene:
    {
      "id": 1,
      "title": "My Scene Title",
      "date": "2023-01-15",
      "studio": {
        "id": 1,
        "name": "My Studio Name"
      },
      "performers": [
        {
          "id": 1,
          "name": "Gina Valentina"
        },
        {
          "id": 2,
          "name": "Melissa Moore"
        },
        {
          "id": 3,
          "name": "Bryan Gozzling"
        }
      ],
      "files": [
        {
          "id": "1",
          "path": "C:\\User\\Desktop\\Test Scene.mp4",
          "basename": "Test Scene.mp4",
          "height": 1080,
          "width": 1920,
          "video_codec": "h264",
          "audio_codec": "aac",
          "frame_rate": 30,
          "duration": 3030.56,
          "bit_rate": 6158790
        }
      ]
    }
  Given config:
    {
      "ENABLE_DRYRUN": true,
      "FILE_NAME_CONFIG": {
        "TEMPLATE": "",
        "PERFORMERS_CONFIG": {
          "SEPARATOR": ", ",
          "ORDER_BY": "id"
        }
      },
      "FILE_PATH_CONFIG": {
        "TEMPLATE": "C:\\User\\Desktop\\STASH"
      }
    }

Scenario: File Name Template With Just Title
  Given config has file name template: "{title}"
  When renamer is activated
  Then rename dst file name is: "My Scene Title"

Scenario: More Complex File Name Template
  Given config has file name template: "{title} ({date}) -- {studio}"
  When renamer is activated
  Then rename dst file name is: "My Scene Title (2023-01-15) -- My Studio Name"

Scenario: File Name Template with Template Variables Right Next To Each Other
  Given config has file name template: "{title}{date}{studio}"
  When renamer is activated
  Then rename dst file name is: "My Scene Title2023-01-15My Studio Name"

Scenario: File Name Template With Resolution
  Given config has file name template: "{title} ({resolution})"
  When renamer is activated
  Then rename dst file name is: "My Scene Title (1080p)"

Scenario: File Name Template With Resolution Name
  Given config has file name template: "{title} ({resolution_name})"
  When renamer is activated
  Then rename dst file name is: "My Scene Title (FHD)"

Scenario: Repeated Title in File Name Template
  Given config has file name template: "({title}) {title}"
  When renamer is activated
  Then rename dst file name is: "(My Scene Title) My Scene Title"


# --- DATE FORMAT ---

Scenario: File Name Template With Date and Title
  Given config has file name template: "{date}.{title}"
  When renamer is activated
  Then rename dst file name is: "2023-01-15.My Scene Title"

Scenario: File Name Template With Dots in Date
  Given config has file name template: "{date:%Y.%m.%d}.{title}"
  When renamer is activated
  Then rename dst file name is: "2023.01.15.My Scene Title"

# NOTE: Slashes are not allowed in Windows file names
Scenario: File Name Template With Slashes in Date
  Given config has file name template: "{date:%Y/%m/%d} - {title}"
  When renamer is activated
  # The rename dst directory is 2023/01 and the file name is 15 - My Scene Title
  Then rename dst file name is: "15 - My Scene Title"

Scenario: File Name Template With Separated Values of  Date
  Given config has file name template: "{date:%m} {date:%Y} {date:%d} - {title}"
  When renamer is activated
  Then rename dst file name is: "01 2023 15 - My Scene Title"

Scenario: File Name Template With Month Name in Date
  Given config has file name template: "{date:%B} {date:%d}, {date:%Y} - {title}"
  When renamer is activated
  Then rename dst file name is: "January 15, 2023 - My Scene Title"


Scenario: File Name Template With Month Name and Spaces in Date
  Given config has file name template: "{date:%B %Y} - {title}"
  When renamer is activated
  Then rename dst file name is: "January 2023 - My Scene Title"
