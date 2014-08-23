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

version = 0.009

def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path
    
import urllib, os, sys, json, time
from PyQt4 import QtCore
userdir = os.path.expanduser('~')

sys.path.insert(0, userdir + SEP('/.cache/deadprogram/modules'))

import pdf2images, oldpdfdeleter, linkparser, deadprogram, BeautifulSoup, imagedeleter, gui, helpfile, pdf2images2

userprogpath = SEP('/.cache/deadprogram/')

vpdf2images = pdf2images.version
voldpdfdeleter = oldpdfdeleter.version
vlinkparser = linkparser.version
vBeautifulSoup = BeautifulSoup.version
vdeadprogram = deadprogram.version
vimagedeleter = imagedeleter.version
vgui = gui.version
vhelpfile = helpfile.version
vpdf2images2 = pdf2images2.version

lst = [('pdf2images.py', vpdf2images), ('oldpdfdeleter.py', voldpdfdeleter), ('linkparser.py', vlinkparser), ('BeautifulSoup.py', vBeautifulSoup), ('deadprogram.py', vdeadprogram), ('updater.py', version), ('gui.py', vgui), ('imagedeleter.py', vimagedeleter), ('helpfile.py', vhelpfile), ('pdf2images2.py', vpdf2images2)]

class Updater(QtCore.QThread):
    info = QtCore.pyqtSignal(str)
       
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()
        
    def run(self):
        self.info.emit('Tikrinu ar nėra programos atnaujinimo')
        updateinfolink = 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/updateinfo'
        response = urllib.urlopen(updateinfolink)
        info = response.read()
        f = open(userdir + userprogpath + SEP('modules/updateinfo'), 'w')
        f.write(info)
        f.close()
        f2 = open(userdir + userprogpath + SEP('modules/updateinfo'), 'r')        
        lst2 = json.load(f2)
        f2.close()
        for item in lst:
            for item2 in lst2:
                print item[0], item2[0], item[1], item2[1]
                if item[1] <  item2[1] and item[0] ==  item2[0]:
                    self.info.emit('Radau atnaujinimą')
                    url = item2[2]
                    filename = item2[0]
                    response = urllib.urlopen(url)
                    info = response.read()
                    f = open(userdir + userprogpath + SEP('modules/') + filename + '.updt', 'w')
                    f.write(info)
                    f.close()
                    self.info.emit('Atnaujinau ' + filename)
                else:
                    pass
        self.info.emit('Baigiau')
        return
