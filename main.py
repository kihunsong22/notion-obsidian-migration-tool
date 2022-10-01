import logging
import logging.handlers
import os
from pathlib import Path

logger = logging.getLogger("root")

SOURCE_DIR = "C:/Notion-export/"
DEST_DIR = "C:/Notion-export-dest/"

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

def browser():
    s_dir = Path(SOURCE_DIR)
    d_dir = Path(DEST_DIR)

    for x in s_dir.iterdir():
        if x.is_dir():
            logger.info('folder: "{}"'.format(x))
        elif x.is_file():
            logger.info('file: "{}"'.format(x))
            editor(x, d_dir)

        exit()  # only iterate once

def editor(item, dest_path):
    if(item.exists() == False):
        logger.info('item does not exist: "{}"'.format(item))
        exit()  # die
    
    logger.debug('editor: "{}"'.format(item.name))

    with item.open(encoding='UTF8') as f:
        for lines in f.readlines():
            logger.debug('lines: "{}"'.format(lines[:-1]))  # remove line break from source
        # logger.debug(f.readline())
    

def main():
    setLogging()

    logger.info('Entry: notion-obsidian-migration-tool')

    browser()


if __name__ == '__main__':
    main()


