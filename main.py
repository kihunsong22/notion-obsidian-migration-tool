import logging
import logging.handlers
import os
from pathlib import Path
import re

logger = logging.getLogger("root")

SOURCE_PATH = "C:/Notion-export/"
DEST_PATH = "C:/Notion-export-dest/"  # CAUTION: WILL REMOVE EVERYTHING UNDER THIS DIRECTORY

def setLogging():
    """logging module setup"""

    # formatter = logging.Formatter('[%(levelname)8s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    # formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(funcName)s:%(lineno)s] %(asctime)s.%(msecs)d > %(message)s', '%H:%M:%S')
    # formatter = logging.Formatter('[%(levelname)s|%(funcName)s] %(asctime)s.%(msecs)d > %(message)s', '%H:%M:%S')
    formatter = logging.Formatter('[%(levelname)s|%(funcName)s] > %(message)s')

    # fileMaxByte = 1024 * 1024 * 100 #100MB
    # fileHandler = logging.handlers.RotatingFileHandler(filename='./python.log', maxBytes=fileMaxByte, backupCount=10, encoding='utf-8')
    # RotatingFileHandler only takes 'append' mode
    fileHandler = logging.FileHandler("python.log", mode='w', encoding='utf-8')
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    logger.setLevel(logging.DEBUG)

    # logging.basicConfig(filename='python.log', filemode='w', level=logging.DEBUG)

def rm_path(d_path):
    """
    remove all files/folders inside of d_path
    """

    # d_path = Path(d_path)

    logger.info('rm_path: "{}"'.format(d_path))
    # logger.info('disk_usage of d_path: "{}"'.format(shutil.disk_usage(d_path)))

    for x in d_path.iterdir():
        if x.is_dir():
            rm_path(x.absolute())

            logger.debug('rmdir: "{}"'.format(x.absolute()))
            x.rmdir()
        elif x.is_file():
            x.unlink()
            logger.debug('rm   : "{}"'.format(x.absolute()))

def YAML_front_matter_composer(data: dict):
    """
    returns YAML front matter string
    currently only supports single level dictionary parsing

    Parameters:
    data: dict type

    Returns:
    str containing YAML front matter
    """
    res = '---\n'

    for x in data:
        # if type(data[x]) is dict:
        #     for y in data:
        res += '{}: {}\n'.format(x, data[x])
    
    res += '---'

    logger.info('YAML: \n"{}"'.format(res))

    return res

def browser(s_path, d_path):
    """
    search for appropriate markdown files and call editor() accordingly
    """
    # s_path = Path(SOURCE_PATH)
    # d_path = Path(DEST_PATH)

    for x in s_path.iterdir():
        if x.is_dir():
            logger.info('folder: "{}"'.format(x))
        elif x.is_file():
            logger.info('file: "{}"'.format(x))
            logger.debug('rel_path: "{}"'.format(x.relative_to(SOURCE_PATH)))
            editor(x, s_path, d_path)

        exit()  # only iterate once

def editor(item, s_path, d_path):
    """
    parse through item, create updated markdown file in d_path
    
    Parameters:
    item: absolute path to the markdown file
    s_path: SOURCE_PATH
    d_path: DEST_PATH

    Returns:
    """
    md_title = ''
    md_creation_date = ''
    md_tags = ''

    if(item.exists() == False):
        logger.error('item does not exist: "{}"'.format(item))
        exit()  # die
    
    logger.debug('editor: "{}"'.format(item.name))

    with item.open(encoding='UTF8') as f:
        for lines in f.readlines():
            logger.debug('lines: "{}"'.format(lines[:-1]))  # remove line break from source

            # 1. search for title line
            pattern = re.compile('(# ).+')
            match = pattern.match(lines)
            if not(match is None):
                logger.info('title_match: "{}" chars, "{}"'.format(match.end()-match.start(), match.group()))
                md_title = match.group()

            # 2. search for creation date
            pattern = re.compile('(Created: ).+')
            match = pattern.match(lines)
            if not(match is None):
                logger.info('created_date_match: "{}" chars, "{}"'.format(match.end()-match.start(), match.group()))
                md_creation_date = match.group()

            # 3. search tags
            pattern = re.compile('(Tags: ).+')
            match = pattern.match(lines)
            if not(match is None):
                logger.info('tags_match: "{}" chars, "{}"'.format(match.end()-match.start(), match.group()))
                md_tags = match.group()

    # refine the parsed data
    md_creation_date

    md_tags

    # compose a dict variable with parsed data
    parsed_data = {
        'title': md_title,
        'created': md_creation_date,
        'tags': md_tags
    }
    
    # create an updated MD file with YAML front matter
    logger.info('rel path: "{}"'.format(item.relative_to(s_path)))
    new_item = d_path.joinpath(item.relative_to(s_path))
    new_item.touch()

    YAML_front_matter_composer(d)


def main():
    setLogging()

    logger.info('Entry: notion-obsidian-migration-tool')

    if not Path(SOURCE_PATH).exists():
        logger.warn('SOURCE_PATH not found')
        exit()
    
    if not Path(DEST_PATH).exists():
        logger.warn('DEST_PATH not found, creating one...')
        Path(DEST_PATH).mkdir()        

    rm_path(Path(DEST_PATH))

    browser(Path(SOURCE_PATH), Path(DEST_PATH))


if __name__ == '__main__':
    main()
