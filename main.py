import logging
import logging.handlers
import os
from pathlib import Path
import re
from dateutil.parser import parse
import datetime

logger = logging.getLogger("root")

SOURCE_PATH = "C:/Notion-export/"
DEST_PATH = "C:/Notion-export-dest/"  # CAUTION: WILL REMOVE EVERYTHING UNDER THIS DIRECTORY
CREATE_YAML = True

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

    logger.debug('rm_path(): "{}"'.format(d_path))
    # logger.info('disk_usage of d_path: "{}"'.format(shutil.disk_usage(d_path)))

    for x in d_path.iterdir():
        if x.is_dir():
            rm_path(x.absolute())

            logger.debug('rmdir: "{}"'.format(x.absolute()))
            x.rmdir()
        elif x.is_file():
            x.unlink()
            logger.debug('rm: "{}"'.format(x.absolute()))

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

    logger.info('YAML: \n{}'.format(res))

    return res

def md_title_checker(title: str):
    """
    remove markdown style hash, enforce windows file naming scheme

    Reference: https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#naming-conventions
    """
    UNSUPPORTED_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    original_title = title

    title = title.split('# ')[-1]
    for c in UNSUPPORTED_CHARS:
        title = title.replace(c, '')

    logger.debug('md_title: "{}" -> "{}"'.format(original_title, title))

    return title

def md_cdate_checker(cdate: str):
    """
    # parse notion style date format, return in YYYY-MM-DD format
    parse notion style date format, returns datetime object
    """

    original_cdate = cdate

    cdate = cdate.split('Created: ')[-1]

    # date conversion method 1 - from dateutil.parser import parse
    dt = parse(cdate)
    logger.debug('md_cdate: "{}" -> "{}, {}"'.format(original_cdate, dt.date(), dt.time()))

    # date conversion method 2 - import datetime
    # cdate = datetime.datetime.strptime(cdate, '%B %d, %Y %I:%M %p').strftime('%Y-%m-%d')

    return dt

def md_tags_checker(tags: str):
    """
    parse notion style tags, return in obsidian style
    """

    original_tags = tags

    tags = tags.split('Tags: ')[-1]  # remove 'Tags: '

    # add hastags
    tag_list = tags.split(', ')
    tags = ''
    for x in tag_list:
        tags += '#{}, '.format(x)

    tags = ', '.join(tags.split(', ')[:-1])  # remove last ', '

    logger.debug('md_tags: "{}" -> "{}"'.format(original_tags, tags))

    return tags

def md_data_encode(content: str):
    """
    encodes the data in UTF-8, converts line endings to LF

    Returns: converted bytecode of input
    """
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    
    content = content.encode('utf-8')

    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    
    return content

def browser(current_path, s_path, d_path):
    """
    search for appropriate markdown files and call editor() accordingly

    Parameters:
    current_path: current path to browse
    s_path: absolute path of SOURCE_INPUT
    d_path: absolute path of DEST_INPUUT
    """
    for x in current_path.iterdir():
        if x.is_dir():
            logger.info('folder: "{}"'.format(x))
            browser(x, s_path, d_path)
        elif x.is_file():
            logger.info('file: "{}"'.format(x))
            editor(x.absolute(), s_path, d_path)

        # exit()  # only iterate once

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
    
    md_body_str = ''

    if(item.exists() == False):
        logger.error('item does not exist: "{}"'.format(item))
        exit()  # die
    
    logger.debug('editor: "{}"'.format(item.relative_to(s_path)))

    with item.open(encoding='UTF8') as f:
        for lines in f.readlines():
            md_body_str += lines
            # logger.debug('lines: "{}"'.format(lines[:-1]))  # remove line break from source

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
    md_title = md_title_checker(md_title)

    md_dt_object = md_cdate_checker(md_creation_date)
    # md_creation_time = md_cdate_checker(md_creation_date)

    md_tags = md_tags_checker(md_tags)

    # compose a dict variable with parsed data
    parsed_data = {
        'title': md_title,
        'created': md_dt_object.date(),
        'tags': md_tags
    }

    dest_dir = d_path.joinpath(item.relative_to(s_path).parent)
    dest_file = d_path.joinpath(item.relative_to(s_path)).parent.joinpath(md_title+'.md')

    if not dest_dir.exists():
        logger.warn('dest dir not found:"{}"'.format(dest_dir))
        
        while not dest_dir.exists():
            temp_dir = dest_dir
            while not temp_dir.exists():
                if(temp_dir.parent.exists()):
                    logger.debug('creating dest directory: "{}"'.format(temp_dir))
                    temp_dir.mkdir()
                else:
                    temp_dir = temp_dir.parent

    dest_file.touch()
    logger.debug('path to new MD: "{}"'.format(dest_file))

    if CREATE_YAML:
        md_body_str = YAML_front_matter_composer(parsed_data) + '\n' + md_body_str
    
    md_body_bc = md_data_encode(md_body_str)
    dest_file.write_bytes(md_body_bc)

    # change creation time metadata
    os.utime(dest_file, times=(md_dt_object.timestamp(), md_dt_object.timestamp()))

def main():
    setLogging()

    logger.info('Entry: notion-obsidian-migration-tool')

    if not Path(SOURCE_PATH).exists():
        logger.warn('SOURCE_PATH not found')
        exit()
    
    if not Path(DEST_PATH).exists():
        logger.warn('DEST_PATH not found, creating directory...')
        Path(DEST_PATH).mkdir()        

    rm_path(Path(DEST_PATH))  # clear destination path before proceeding

    browser(Path(SOURCE_PATH), Path(SOURCE_PATH), Path(DEST_PATH))


if __name__ == '__main__':
    main()
