#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	ReklaminiaiParduotuviųLankstinukai
	Copyright (C) <2014> <Algirdas Butkus> <butkus.algirdas@gmail.com>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
'''C:\PyInstaller-2.1>c:\python27\python.exe -O pyinstaller.py -w --clean -D -i c:\RPL\icons\image.ico --hidden-import=PyQt4.QtXml -n rpl -y --noupx c:\RPL\main.py'''
'''pyinstaller --clean --hidden-import=PyQt4.QtXml --workpath=/tmp --specpath=/tmp/spec --distpath=/tmp/dist -s --noupx --onefile -n DeadProgram -y  /usr/lib/deadprogram/main.py'''

from PyQt4 import QtGui
import os, sys

def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path

userprogpath = SEP('/.cache/deadprogram/')
userdir = os.path.expanduser('~')
sys.path.insert(0, userdir + userprogpath + 'modules')
import deadprogram

class Start(deadprogram.DeadProgram):
    def __init__(self):
        deadprogram.DeadProgram.__init__(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Start()
    a.show()
    sys.exit(app.exec_())
        
