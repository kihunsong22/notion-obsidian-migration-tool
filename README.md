# notion-obsidian-markdown-converter
a simple python script to further refine markdown files after using [connertennery/Notion-to-Obsidian-Converter](https://github.com/connertennery/Notion-to-Obsidian-Converter)

## Usage
- update 3 variables in main.py: `SOURCE_PATH`, `DEST_PATH`, `ADD_YAML`
- run the script

## Roadmap
- [x] convert file names to match title
    - [ ] advanced filename checks against windows naming scheme
- [x] use created date field inside MD file to edit metadata accordingly
    - [ ] use datetime specified on the title first
- [x] convert notion style tags to obsidian supported hashtags
- [x] option to create YAML style front matter containing title, date, tags

## Notes
This script **will remove any files/folders under `SOURCE_DEST`** every time you run it, so proceed with caution.

#### dev note
- https://docs.python.org/3/library/filesys.html
- https://docs.python.org/3/library/pathlib.html#basic-use
- https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#naming-conventions
- https://www.tutorialspoint.com/python/time_strptime.htm
- https://github.com/othneildrew/Best-README-Template
