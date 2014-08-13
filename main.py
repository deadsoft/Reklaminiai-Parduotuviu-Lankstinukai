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
import os, sys, importlib
import platform, shutil
        
def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path

userprogpath = SEP('/.cache/deadprogram/')
userdir = os.path.expanduser('~')

dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi', 'Aibe' , 'FRESH_MARKET', 'Senukai', 'Moki_Vezi']

if not os.path.exists(userdir + SEP('/.cache')):
    os.mkdir(userdir + '/.cache')
if not os.path.exists(userdir + userprogpath):
    os.mkdir(userdir + userprogpath)
if not os.path.exists(userdir + userprogpath + 'modules'):
    os.mkdir(userdir + userprogpath + 'modules')
if not os.path.exists(userdir + userprogpath + SEP('modules/__init__.py')):
    open(userdir + userprogpath + SEP('modules/__init__.py'), 'a').close()
if not os.path.exists(userdir + userprogpath + 'cache'):
    os.mkdir(userdir + userprogpath + 'cache')
if not os.path.exists(userdir + userprogpath + 'pdfs'):
    os.mkdir(userdir + userprogpath + 'pdfs')
for item in dirs:
    if not os.path.exists(userdir + userprogpath + 'pdfs/' + item):
        os.mkdir(userdir + userprogpath + 'pdfs/' + item)
if platform.system() == "Linux":
    if not os.path.exists(userdir + userprogpath + 'build'):
        shutil.copytree('/usr/share/deadprogram/build', userdir + userprogpath + 'build')
    if not os.path.exists(userdir + userprogpath + 'icons'):
        shutil.copytree('/usr/share/deadprogram/icons', userdir + userprogpath + 'icons')
    if not os.path.exists(userdir + userprogpath + 'web'):
        shutil.copytree('/usr/share/deadprogram/web', userdir + userprogpath + 'web')
    if not os.path.exists(userdir + userprogpath + 'jquery'):
        shutil.copytree('/usr/share/deadprogram/jquery', userdir + userprogpath + 'jquery')    
elif platform.system() == "Windows":
    if not os.path.exists(userdir + userprogpath + 'build'):
        shutil.copytree('C:\\Program Files\\RPL\\build', userdir + userprogpath + 'build')
    if not os.path.exists(userdir + userprogpath + 'icons'):
        shutil.copytree('C:\\Program Files\\RPL\\icons', userdir + userprogpath + 'icons')
    if not os.path.exists(userdir + userprogpath + 'web'):
        shutil.copytree('C:\\Program Files\\RPL\\web', userdir + userprogpath + 'web')
    if not os.path.exists(userdir + userprogpath + 'jquery'):
        shutil.copytree('C:\\Program Files\\RPL\\jquery', userdir + userprogpath + 'jquery')
        
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
        
