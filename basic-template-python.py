#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Code by SNPY

# prerequisites:
# Python 3.5

import sys
from pathlib import Path
from datetime import datetime
# add #-DLH-# to path for import
sys.path.append(str(Path(sys.path[0]) / '#-DLH-#'))

import snpys_dirty_little_helper as s
clear = cls = s.clear_console
press = stop = wait = s.press

clear()
s.check_python()

### SkriptSettings
# Filter für Dateitypen, weitere Typen falls nötig hinzufügen ('.log', '.txt', '.file',) etc.
# Skript-Modus (für andere Fälle)

settings = {
    'filter' : ('.txt', '.db', ), # filter wird auf klein getrimmt
    'mode' : 'test', # test, copy, move 
    'rekursiv' : False, # True, False, recursiv into subdirs?
}

def exit():
    sys.exit(0)

def printlog(text, logname=None, printer=None):
    print(text)
    s.write_to_file(path=w.logpath, content=text, )

def endscript():
    w.endtime = datetime.now()
    w.runtime = w.endtime - w.starttime
    printlog('Skript benötigte {} Sekunden'.format(str(w.runtime.seconds) + '.' + str(w.runtime.microseconds)))
    s.cleanup()

# Skript beginnt hier / script starts here

work = w = s.get_work(**settings) # Klasse, (counter, starttime, timestring, logtime, dir, outdir, logname, logpath, )
printlog('Starte Skript um {} Uhr'.format(w.starttime.strftime('%H:%M:%S')))
print()

# everyone clean up after themselves!
endscript()
