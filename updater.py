# -*- coding: utf-8 -*-
"""
	ReklaminiaiParduotuviųLankstinukai
	Copyright (C) <2014> <Algirdas Butkus>

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
#lst = [('linkparser.py', 0.002, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/linkparser.py'), ('pdf2images.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/pdf2images.py'), ('oldpdfdeleter.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/oldpdfdeleter.py'), ('deadprogram.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/deadprogram.py'), ('BeautifulSoup.py', 3.2, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/BeautifulSoup.py'), ('updater.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/updater.py'), ('gui.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/gui.py'), ('imagedeleter.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/imagedeleter.py')]

version = 0.001

import urllib, os, sys, json, time
from PyQt4 import QtCore
userdir = os.path.expanduser('~')
sys.path.insert(0, userdir + '/.cache/deadprogram/modules')
import pdf2images, oldpdfdeleter, linkparser, deadprogram, BeautifulSoup, imagedeleter, gui

vpdf2images = pdf2images.version
voldpdfdeleter = oldpdfdeleter.version
vlinkparser = linkparser.version
vBeautifulSoup = BeautifulSoup.version
vdeadprogram = deadprogram.version
vimagedeleter = imagedeleter.version
vgui = gui.version

lst = [('pdf2images.py', vpdf2images), ('oldpdfdeleter.py', voldpdfdeleter), ('linkparser.py', vlinkparser), ('BeautifulSoup.py', vBeautifulSoup), ('deadprogram.py', vdeadprogram), ('updater.py', version), ('gui.py', vgui), ('imagedeleter.py', vimagedeleter)]

class Updater(QtCore.QThread):
    foundupdate = QtCore.pyqtSignal(str)
    updated = QtCore.pyqtSignal(str)
       
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()
        
    def run(self):
        time.sleep(2)
        updateinfolink = 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/updateinfo'
        response = urllib.urlopen(updateinfolink)
        info = response.read()
        f = open(userdir + '/.cache/deadprogram/modules/updateinfo', 'w')
        f.write(info)
        f.close()
        f2 = open(userdir + '/.cache/deadprogram/modules/updateinfo', 'r')        
        lst2 = json.load(f2)
        f2.close()
        for item in lst:
            for item2 in lst2:
                if item[1] <  item2[1] and item[0] ==  item2[0]:
                    self.foundupdate.emit('Radau atnaujinimą')
                    url = item2[2]
                    filename = item2[0]
                    response = urllib.urlopen(url)
                    info = response.read()
                    f = open(userdir + '/.cache/deadprogram/modules/' + filename, 'w')
                    f.write(info)
                    f.close()
                    self.updated.emit('Atnaujinau...')
                else:
                    pass
        self.updated.emit('Patikrinau ar nėra programos atnaujinimo')
        return
