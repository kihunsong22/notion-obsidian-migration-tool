# notion-obsidian-markdown-converter
a simple python script to further refine markdown files after using [connertennery/Notion-to-Obsidian-Converter](https://github.com/connertennery/Notion-to-Obsidian-Converter)

## Usage
- update 3 variables in main.py: `SOURCE_PATH`, `DEST_PATH`, `ADD_YAML`
- run the script

## Roadmap
- [x] better title for each markdown file
    - [x] use title field inside MD file if possible
    - [x] substitute/remove unsupported characters by Windows and ObsidianMD
    - [ ] advanced filename checks against Windows naming scheme
- [x] use created date field inside MD file to edit metadata if possible
- [x] convert notion style tags to YAML style hashtags
- [x] option to create YAML style front matter containing title, date, tags
- [ ] fix images and attachments path inside each markdown document

## Notes/Warning
This script **will remove any files/folders under `SOURCE_DEST`** every time you run it, so proceed with caution.

#### dev note
- https://docs.python.org/3/library/filesys.html
- https://docs.python.org/3/library/pathlib.html#basic-use
- https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#naming-conventions
- https://www.tutorialspoint.com/python/time_strptime.htm
- https://github.com/othneildrew/Best-README-Template
