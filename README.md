# notion-obsidian-markdown-converter
a simple python script to further refine markdown files after using [connertennery/Notion-to-Obsidian-Converter](https://github.com/connertennery/Notion-to-Obsidian-Converter)

## What it does (work in progress)
- convert file names to match title
- use created date field inside MD file to edit metadata
- convert notion style tags to obsidian supported hashtags
- create YAML style front matter if needed

## Usage
- update 3 variables in main.py: `SOURCE_PATH`, `DEST_PATH`, `ADD_YAML`
- run the script

## Notes
This script **will remove any files/folders under `SOURCE_DEST`** every time you run it, so proceed with caution.

#### dev note
- https://docs.python.org/3/library/filesys.html
- https://docs.python.org/3/library/pathlib.html#basic-use
- https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#naming-conventions
- https://www.tutorialspoint.com/python/time_strptime.htm

#### features to implement
- advanced filename checking function against windows naming scheme
- edit metadata of created date
    - fiddle with metadata