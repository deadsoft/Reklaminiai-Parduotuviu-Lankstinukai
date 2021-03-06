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

from PyQt4 import QtGui
import os, sys, importlib
        
def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path

userprogpath = SEP('/.cache/deadprogram/')
userdir = os.path.expanduser('~')
if not os.path.exists(userdir + SEP('/.cache')):
    os.mkdir(userdir + '/.cache')
if not os.path.exists(userdir + userprogpath):
    os.mkdir(userdir + userprogpath)
if not os.path.exists(userdir + userprogpath + 'modules'):
    os.mkdir(userdir + userprogpath + 'modules')
if not os.path.exists(userdir + userprogpath + SEP('modules/__init__.py')):
    open(userdir + userprogpath + SEP('modules/__init__.py'), 'a').close()
            
files = os.listdir(userdir + userprogpath + SEP('modules/'))
for f in files:
    if f.endswith('.updt'):
        try:
            os.rename(userdir + userprogpath + SEP('modules/') + f, userdir + userprogpath + SEP('modules/') + f.replace(".updt", ""))
        except:
            os.remove(userdir + userprogpath + SEP('modules/') + f.replace(".updt", ""))
            os.rename(userdir + userprogpath + SEP('modules/') + f, userdir + userprogpath + SEP('modules/') + f.replace(".updt", ""))

sys.path.insert(0, userdir + SEP('/.cache/deadprogram/modules'))
import deadprogram



class Start(deadprogram.DeadProgram):
    def __init__(self):
        deadprogram.DeadProgram.__init__(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Start()
    a.show()
    sys.exit(app.exec_())
        
