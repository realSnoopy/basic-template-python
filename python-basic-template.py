#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Flat is better than nested.

# Python 3.5 and up
# getestet Python 3.6.5

VERSION = 'ALPHA'

def clear_console():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')

def exit(error_msg=None):
    if error_msg:
        print('\n[ERROR]\n{}\n[EXIT]'.format(error_msg))
    sys.exit(0)

try:
    import os
    import sys
    import unicodedata
    import logging
    from pathlib import Path
    from platform import python_version
    from codecs import BOM_UTF8, BOM_UTF16, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE
except Exception as error:
    exit(error)

def check_python():
    try:
        assert(python_version() >= '3.5')
    except AssertionError:
        error = 'This script requires at least Python 3.5. Please update or use "python3" to invoke.\n'
        error += 'Python {} found.'.format(python_version())
        exit(error)

def get_files(path, ):
    file_list = []
    try:
        assert(python_version() >= '3.6')
    except AssertionError:
        directory = str(directory)

    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            tmp_files = get_files(entry, )
            [file_list.append(Path(file)) for file in tmp_files]
        if entry.is_file():
            file_list.append(Path(entry))
    
    return file_list

def get_files_filter(files, file_filter, ):
    file_list_filter = []
    for file in files:
            if file.name in file_filter or file.suffix.lower() in [filter.lower() for filter in file_filter]:
                file_list_filter.append(Path(file))
    return file_list_filter

def make_dir(path):
    path = Path(path)
    if not path.exists():
            path.mkdir(parents=True)

def get_size(file):
        return (Path(file).stat().st_size)

def size_to_human(filesize, base='KB'):

    if base == 'KB':
        return '{:.2f} KB'.format(filesize/1024)

    elif base == 'MB':
        return '{:.2f} MB'.format(filesize/(1024*1024))

class GetWork:

    def __init__(self, path, file_filter=None):
        
        self._path = path
        self._file_filter = file_filter
        self._root = Path.cwd()

        self._outpath = Path(self._root) / '#-OUT-#'
        make_dir(self._outpath)

        if not self._path:
            logging.info('Input-Path not found')
            exit()
        
        self._files = get_files(self._path, )

        if self._file_filter:
            self._files_filtered = get_files_filter(self._files, self._file_filter)
        else:
            self._files_filtered = self._files

    @property
    def files(self):
        return self._files
    @property
    def files_filtered(self):
        return self._files_filtered
    @property
    def outpath(self):
        return self._outpath

BOMS = (
    (BOM_UTF8, 'UTF-8-SIG'),
    (BOM_UTF32_BE, 'UTF-32-BE'),
    (BOM_UTF32_LE, 'UTF-32-LE'),
    (BOM_UTF16_BE, 'UTF-16-BE'),
    (BOM_UTF16_LE, 'UTF-16-LE'),
)

def check_bom(data):
    return [encoding for bom, encoding in BOMS if data.startswith(bom)]

def get_content(file, read, ):

    def read_file(file, encoding, read, mode='r'):
        with open(file=file, encoding=encoding, mode=mode, errors='strict') as file_object:
                    if read == 'read':
                        file_content = file_object.read()
                    elif read == 'lines':
                        file_content = file_object.readlines()
        return file_content

    error_msg = ''

    with open(file, mode='rb') as file_object:
        encoding = check_bom(file_object.readline())
        encoding = ''.join(encoding)
    
    if encoding != '':
        logging.info('encoding\t{}'.format(encoding))
    else:
        logging.info('encoding\tNo BOM found')

    # mit erkannter BOM-Codierung auslesen, ohne Codierung auf UTF-8 ausweichen
    if encoding != '':
        try:
            file_content = read_file(file=file, encoding=encoding, read=read, )
        except Exception as error:
            logging.debug('{}'.format(error))
            encoding = ''

    if encoding == '':
        try:
            file_content = read_file(file=file, encoding='UTF-8', read=read)
        except Exception as error:
            logging.debug('{}'.format(error))
            exit('Krasser Fehler')
    return file_content

def write_to_file(path, content, mode='w'):

    path = Path(path) # pathlib path object
    # create required folders if needed
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, mode=mode, encoding='UTF-8', errors='strict') as output:

        if isinstance(content, (str)):
            content = content + '\n'
            output.writelines(content)
        else:
            content = [str(entry) + '\n' for entry in content]
            output.writelines(content)

### Logging-Stuff
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

def create_basic_logger(file_handler):

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(file_handler)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch_formatter = logging.Formatter(fmt='{levelname}\t{message}', style='{', )
    fh_formatter = logging.Formatter(fmt='{asctime}\t{levelname}\t{message}', style='{', datefmt='%H:%M:%S')
    ch.setFormatter(ch_formatter)
    fh.setFormatter(fh_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

#######
# Ich bin das Alpha und das Omega, der Erste und der Letzte, der Anfang und das Ende.
#######

clear_console()
check_python()

settings = {
    'path' : Path.cwd() ,
    'file_filter' : ('.txt', ) ,
}
root = GetWork(**settings)

# create basic logger
logging = create_basic_logger(file_handler = Path(root.outpath) / 'debug.log')

if __name__ == '__main__':
    
    for file in root.files:
        pass
    for file in root.files_filtered:
        pass
        # basic infos for files
        logging.info('filename\t{}'.format(file.name))
        logging.info('filesize\t{}'.format(size_to_human(get_size(file), base='KB')))

        file_content = get_content(file, read='lines')


