Feature: Basic Feature

Scenario: Basic Scenario
    Given scene:
        {
          "id": "1",
          "title": "Test Scene",
          "date": "2021-01-01",
          "studio": {
            "id": "1",
            "name": "Test Studio"
          },
          "performers": [
            {
              "id": "1",
              "name": "Test Performer 1"
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
    And config:
        {
          "ENABLE_DRYRUN": true,
          "FILE_NAME_CONFIG": [
            {
              "TEMPLATE": "[{studio}] {date} {title} -- {performers} ({resolution})"
            }
          ],
          "FILE_PATH_CONFIG": [
            {
              "TEMPLATE": "C:\\User\\Desktop\\STASH"
            }
          ]
        }
    When renamer is activated
    Then rename is called with:
      {
        "src": "C:\\User\\Desktop\\Test Scene.mp4",
        "dst": "C:\\User\\Desktop\\STASH\\[Test Studio] 2021-01-01 Test Scene -- Test Performer 1 (1080p).mp4"
      }

Scenario: Multiple Files, Multiple Performers, Different File Name Template
    Given scene:
        {
          "id": "1",
          "title": "Test Scene",
          "date": "2021-01-15",
          "studio": {
            "id": "1",
            "name": "Test Studio"
          },
          "performers": [
            {
              "id": "1",
              "name": "Performer A",
              "gender": "FEMALE"
            },
            {
              "id": "2",
              "name": "Performer B",
              "gender": "MALE"
            }
          ],
          "files": [
            {
              "id": "1",
              "path": "C:\\User\\Desktop\\Test Scene 1.mp4",
              "basename": "Test Scene 1.mp4",
              "height": 1440,
              "width": 2560,
              "video_codec": "h264",
              "audio_codec": "aac",
              "frame_rate": 30,
              "duration": 3030.56,
              "bit_rate": 6158790
            },
            {
              "id": "1",
              "path": "C:\\User\\Desktop\\Test Scene 2.mp4",
              "basename": "Test Scene 2.mp4",
              "height": 2160,
              "width": 2840,
              "video_codec": "h264",
              "audio_codec": "aac",
              "frame_rate": 30,
              "duration": 3030.56,
              "bit_rate": 6158790
            }
          ]
        }
    And config:
        {
          "ENABLE_DRYRUN": true,
          "FILE_NAME_CONFIG": [
            {
              "TEMPLATE": "[{studio}] {date:%Y.%m.%d} {title} -- {performers} ({resolution_name})"
            }
          ],
          "FILE_PATH_CONFIG": [
            {
              "TEMPLATE": "C:\\User\\Desktop\\STASH"
            }
          ]
        }
    When renamer is activated
    Then rename is called multiple times with:
      [
        {
          "src": "C:\\User\\Desktop\\Test Scene 1.mp4",
          "dst": "C:\\User\\Desktop\\STASH\\[Test Studio] 2021.01.15 Test Scene -- Performer A, Performer B (2k).mp4"
        },
        {
          "src": "C:\\User\\Desktop\\Test Scene 2.mp4",
          "dst": "C:\\User\\Desktop\\STASH\\[Test Studio] 2021.01.15 Test Scene -- Performer A, Performer B (4k).mp4"
        }
      ]
      