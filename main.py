import logging
import logging.handlers
import os
import shutil
from pathlib import Path
import re
from dateutil.parser import parse
import datetime
import filedate

logger = logging.getLogger("root")

SOURCE_PATH = "C:/Notion-export/"
DEST_PATH = "C:/Notion-export-dest/"  # CAUTION: WILL REMOVE EVERYTHING UNDER THIS DIRECTORY
CREATE_YAML = True

FILETYPES_TO_COPY=( # gets copied to DEST_PATH without modifications
    'jpeg',
    'jpg',
    'png',
    'pdf'
)

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

def shutil_ignore_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

def file_copy(s_path, d_path):
    """
    copies the given item to destination path
    
    Parameters:
    item: absolute path to the file
    s_path: SOURCE_PATH
    d_path: DEST_PATH

    Returns:
    """

    pass

def file_touch(d_file):
    """
    creates an empty file at destination path
    
    Parameters:
    d_file: absolute path to the destination file

    Returns:
    """

    dest_dir = d_file.parent()

    if not dest_dir.exists():
        logger.warn('dest dir not found:"{}"'.format(dest_dir))
        exit()
        
        # while not dest_dir.exists():
        #     temp_dir = dest_dir
        #     while not temp_dir.exists():
        #         if(temp_dir.parent.exists()):
        #             logger.debug('creating dest directory: "{}"'.format(temp_dir))
        #             temp_dir.mkdir()
        #         else:
        #             temp_dir = temp_dir.parent

    d_file.touch()
    logger.debug('path to new MD: "{}"'.format(d_file))

    pass

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

def md_cdate_checker(cdate: str, title: str=''):
    """
    parse notion style date format, returns datetime object
    if possible, will use the date specified on the optional_title
    """

    # parse from title first
    original_title = title
    title = title.split(' ')[0]
    try:
        dt = parse(title, yearfirst=True)
        logger.debug('title_date: "{}" -> "{}, {}"'.format(original_title, dt.date(), dt.time()))
    except:
        original_cdate = cdate
        cdate = cdate.split('Created: ')[-1]
        dt = parse(cdate)
        logger.debug('md_cdate: "{}" -> "{}, {}"'.format(original_cdate, dt.date(), dt.time()))

    # alternative date conversion method - strptime()
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


    for item in current_path.iterdir():
        if item.is_dir():
            logger.info('folder: "{}"'.format(item))
            browser(item, s_path, d_path)
        elif item.is_file():
            logger.info('file: "{}"'.format(item))

            # generate source and destination paths
            s_file = ''
            item_path_rel_to_source = item.relative_to(s_path)

            dest_dir = d_path.joinpath(item.relative_to(s_path).parent)
            dest_file = d_path.joinpath(item.relative_to(s_path))  # only for non-MD files, MD files will have to be renamed

            # logger.debug('DEST_DIR: {}'.format(dest_dir))
            # logger.debug('DEST_FILE: {}'.format(dest_file))
            # logger.debug('ITEM: {}'.format(item))
            
            if str(item).endswith('.md'):
                logger.debug('editor: "{}"'.format(item_path_rel_to_source))
                editor(item.absolute(), s_path, d_path)
                # editor2(item.absolute(), d_path)
            else:
                flag_copy = False
                for a in FILETYPES_TO_COPY:
                    if str(item).endswith(a):
                        flag_copy = True
                        break
                
                if flag_copy:  # known extensions
                    logger.info('Copying non-MD file: {}'.format(item))
                    logger.debug('Copying non-MD file to: {}'.format(dest_file))

                    dest_file.parent.mkdir()
                    shutil.copy2(item, dest_file)
                else:
                    logger.debug('Disregarding file: {}'.format(item))

        # exit()  # only iterate once

def editor2(s_file, d_dir):
    """
    parse through item, create updated markdown file in d_path
    
    Parameters:
    s_file: absolute path to the source markdown file
    d_dir: absolute path to the destination directory

    Returns:
    """

    pass

def editor(s_file, s_path, d_path):
    """
    parse through s_file, create updated markdown file in d_path
    
    Parameters:
    s_file: absolute path to the markdown file
    s_path: SOURCE_PATH
    d_path: DEST_PATH

    Returns:
    """
    md_title = ''
    md_creation_date = ''
    md_tags = ''
    
    md_body_str = ''

    if(s_file.exists() == False):
        logger.error('s_file does not exist: "{}"'.format(s_file))
        exit()

    with s_file.open(encoding='UTF8') as f:
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

    md_dt_object = md_cdate_checker(md_creation_date, md_title)
    # md_creation_time = md_cdate_checker(md_creation_date)

    md_tags = md_tags_checker(md_tags)

    # compose a dict variable with parsed data
    parsed_data = {
        'title': md_title,
        'created': md_dt_object.date(),
        'tags': md_tags
    }

    dest_dir = d_path.joinpath(s_file.relative_to(s_path).parent)
    dest_file = d_path.joinpath(s_file.relative_to(s_path)).parent.joinpath(md_title+'.md')

    file_touch(dest_file)

    if CREATE_YAML:
        md_body_str = YAML_front_matter_composer(parsed_data) + '\n' + md_body_str
    
    md_body_bc = md_data_encode(md_body_str)
    dest_file.write_bytes(md_body_bc)

    # change file access/modification time
    # os.utime(dest_file, (md_dt_object.timestamp(), md_dt_object.timestamp()))

    # change file creation/modification/access time
    dest_file_meta = filedate.File(dest_file)
    logger.debug('dest_file: "{}"'.format(dest_file))
    res = dest_file_meta.set(
        created = md_dt_object.strftime("%F"),
        modified = md_dt_object.strftime("%F")
    )
    logger.debug('filedate edit res: "{}"'.format(res))



def main():
    setLogging()

    logger.info('Entry: notion-obsidian-migration-tool')

    if not Path(SOURCE_PATH).exists():
        logger.warn('SOURCE_PATH not found')
        exit()
    
    if Path(DEST_PATH).exists():
        logger.warn('clearing DEST_PATH first...')
        shutil.rmtree(DEST_PATH)
        # rm_path(Path(DEST_PATH))  # clear destination path before proceeding
        # Path(DEST_PATH).rmdir()

    shutil.copytree(SOURCE_PATH, DEST_PATH, ignore=shutil_ignore_files)

    browser(Path(SOURCE_PATH), Path(SOURCE_PATH), Path(DEST_PATH))


if __name__ == '__main__':
    main()
