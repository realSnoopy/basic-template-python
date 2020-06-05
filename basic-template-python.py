#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Code by SNPY

# prerequisites:
# Python 3.5

import sys
from pathlib import Path
from datetime import datetime

import snpys_dirty_little_helper as s
clear = cls = s.clear_console
press = stop = wait = s.press
exit = kill = s.exit

clear()
s.check_python()
s.check_sdlh('2020-06-05')

### SkriptSettings
# Filter für Dateitypen, weitere Typen falls nötig hinzufügen ('.log', '.txt', '.file',) etc.
# Skript-Modus (für andere Fälle)

settings = {
    'filter' : ('.txt', '.db', ), # filter wird auf klein getrimmt
    # 'mode' : 'test', # test, copy, move 
    # 'recursiv' : True, # True, False, recursiv into subdirs?
}

def printlog(text, timestamp=True, ):
    print(text)
    if timestamp:
        text = '{:.3f}\t{}'.format(datetime.now().timestamp(), text)
    s.write_to_file(path=w.logpath, content=text, )

def startscript():
    print()
    printlog('starting script @ {:.3f} ({} Uhr)'.format(w.starttime.timestamp(), w.starttime.strftime('%H:%M:%S') ))
    printlog('settings:\tfilter:{}\tmode:{}\trecursiv:{}'.format(*w.settings))
    printlog('log-file:\t{}'.format(w.logname))
    printlog('file-count:\t{}'.format(w.fcount))
    printlog('dirs-count:\t{}'.format(w.dcount))

def endscript():
    print()
    w.endtime = datetime.now()
    w.runtime = w.endtime - w.starttime
    printlog('runtime was {}.{:} seconds'.format(w.runtime.seconds, w.runtime.microseconds))
    s.cleanup()

# Skript beginnt hier / script starts here

work = w = s.get_work(**settings) # class (index, counter, dir, outdir, logname, logpath)
startscript()

for file in w.files:

    print()
    w.counter +=  1
    printlog('processing\t{}/{}\t{}'.format(w.counter, w.fcount, file.name), )

# everyone clean up after themselves!
endscript()
