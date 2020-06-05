#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Code by SNPY

# prerequisites:
# Python 3.5

# History
version = '2020-06-05' # new basic release, expect data in #-INPUT-#, recursiv as default

import os
import sys
import sqlite3
from platform import python_version
from datetime import datetime
from pathlib import Path
from shutil import rmtree, move, copy2
from codecs import BOM_UTF8, BOM_UTF16, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

class get_work(object):

    def __init__(self, mode='test', filter=None, recursiv=True, ):

        self.index = 0
        self.counter = 0
        self.starttime = datetime.now()
        self.dir = Path.cwd()
        self.outdir = Path(self.dir) / '#-OUT-#'
        self.inputdir = Path(self.dir) / '#-INPUT-#'
        self.logname = '{}-log.log'.format(self.index)
        self.logpath = Path(self.outdir) / self.logname
        self.mode = mode
        self.recursiv = recursiv
        self.endtime = None
        
        while True:
            if self.logpath.exists():
                self.index += 1
                self.logname = '{}-log.log'.format(self.index)
                self.logpath = Path(self.outdir) / self.logname
            else:
                break

        if filter!=None:
            ffilter = tuple([entry.lower() for entry in filter]) # sicherheitshalber
        else:
            ffilter = filter
        
        self.filter = ffilter
        self.files, self.dirs = get_files_filter(self.inputdir, self.filter, self.recursiv)
        self.fcount = len(self.files)
        self.dcount = len(self.dirs)
        self.settings = self.filter, self.mode, self.recursiv

# self explaining
def clear_console():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')
###

# press ENTER to continue / exit
def press():
    print()
    input('press ENTER to continue or CTRL+C to cancel script...')
###

# everyone clean up after themselves!
def cleanup():
    print()
    print('clean up my own mess...')
    try:
        rmtree(Path.cwd() / '__pycache__')
    except:
        pass
###

# clean exit
def exit():
    cleanup()
    sys.exit(0)
###

# benötigt Python 3.6 für vollständige pathlib Path Kompatibilität (Betriebssystem unabhängig)
# requires Python 3.6 for full pathlib path compatibility (OS independent)
# added workaround for Python 3.5
def check_python():
    try:
        assert(python_version() >= '3.5') # workaround for Python 3.5 in get_files_filter() -> Python LTS Version
        print('Python {} found -> GOOD'.format(python_version()))
    except AssertionError:
        print('Python {} found -> BAD.'.format(python_version()))
        print('This script requires at least Python 3.5. Please update or use "python3" to invoke. -> EXIT')
        exit()
###

# check matching SDLH
def check_sdlh(check):
    if version != check:
        print('SDLH match failed -> BAD\nScript:\t{}\nSDLH:\t{}'.format(check, version))
        print('Expect undefined behavior!')
        press()
    else:
        print('SDLH match passed -> GOOD')
###

#
def get_size(file):
    return Path(file).stat().st_size
###

# added exception for Python 3.5, where os.scandir cant use pathlib.Path-objects, added in Python 3.6
def get_files_filter(directory, filter=None, recursiv=False):
    
    files_list = []
    dirs_list = []

    try:
        assert(python_version() >= '3.6')
    except AssertionError:
        directory = str(directory)

    try:
        for entry in os.scandir(directory):
            if entry.is_dir(follow_symlinks=False) and recursiv == True and entry.name == '#-OUT-#':
                continue
            elif entry.is_dir(follow_symlinks=False) and recursiv == True:
                files_temp = get_files_filter(entry, filter, recursiv)
                [files_list.append(Path(file)) for file in files_temp]
            elif filter == None and entry.is_file() and not entry.name.lower().endswith('.py') and not entry.name.lower().endswith('.pyc'):
                files_list.append(Path(entry))
            elif filter != None and entry.is_file() and entry.name.lower().endswith(filter):
                files_list.append(Path(entry))
            else:
                pass
    except:
        pass
    return files_list, dirs_list
###

BOMS = (
    (BOM_UTF8, 'UTF-8-SIG'),
    (BOM_UTF32_BE, 'UTF-32-BE'),
    (BOM_UTF32_LE, 'UTF-32-LE'),
    (BOM_UTF16_BE, 'UTF-16-BE'),
    (BOM_UTF16_LE, 'UTF-16-LE'),
)

def check_bom(data):
    return [encoding for bom, encoding in BOMS if data.startswith(bom)]

def get_content(file, type, ):

    file_content = []
    error_msg = []

    with open(file, mode='rb') as file_object:
        encoding = check_bom(file_object.readline())
        encoding = ''.join(encoding)

    # mit erkannter Codierung auslesen, bei Fehler auf UTF-8 ausweichen, todo delete iso related stuff
    if encoding != '':
        try:
            with open(file, mode='r', encoding=encoding, errors='strict') as file_object:
                if type == 'read':
                    file_content = file_object.read()
                elif type == 'lines':
                    file_content = file_object.readlines()
        except Exception as error:
            print(error, file)
            error_msg.append(error)
            encoding = ''

    if encoding == '':
            try:
                with open(file, mode='r', encoding='utf-8', errors='strict') as file_object:
                    if type == 'read':
                        file_content = file_object.read()
                    elif type == 'lines':
                        file_content = file_object.readlines()
            except Exception as error:
                print(error, file)
                error_msg.append(error)
                try:
                    with open(file, mode='r', encoding='iso8859-15', errors='strict') as file_object:
                        if type == 'read':
                            file_content = file_object.read()
                        elif type == 'lines':
                            file_content = file_object.readlines()
                except Exception as error:
                    print(error, file)
                    error_msg.append(error)

    file_data = {
        'content' : file_content,
        'error' : error_msg,
    }
    return file_data

def write_to_file(path, content, ):

    path = Path(path) # pathlib path object
    # create required folders if needed
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, mode='a', encoding='UTF-8', errors='strict') as output:

        if isinstance(content, (str)):
            content = content + '\n'
            output.writelines(content)
        else:
            content = [str(entry) + '\n' for entry in content]
            output.writelines(content)

def query_db(database, sql):
    database = str(database)
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    if connection:
        connection.close()
    return result