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
#lst = [('linkparser.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/linkparser.py'), ('pdf2images.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/pdf2images.py'), ('oldpdfdeleter.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/oldpdfdeleter.py'), ('deadprogram.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/deadprogram.py'), ('BeautifulSoup.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/BeautifulSoup.py'), ('updater.py', 0.001, 'https://github.com/deadsoft/Reklaminiai-Parduotuviu-Lankstinukai/raw/master/updater.py')]

version = 0.001

import urllib, os, sys, json
from PyQt4 import QtCore
userdir = os.path.expanduser('~')
sys.path.insert(0, userdir + '/.cache/deadprogram/modules')
import pdf2images, oldpdfdeleter, linkparser, deadprogram
from BeautifulSoup import __version__

vpdf2images = pdf2images.version
voldpdfdeleter = oldpdfdeleter.version
vlinkparser = linkparser.version
vBeautifulSoup = __version__
vdeadprogram = deadprogram.version
vversion = version

lst = [('pdf2images.py', vpdf2images), ('oldpdfdeleter.py', voldpdfdeleter), ('linkparser.py', vlinkparser), ('BeautifulSoup.py', vBeautifulSoup), ('deadprogram.py', vdeadprogram), ('version', version)]

class Updater(QtCore.QThread):
    foundupdate = QtCore.pyqtSignal(str)
    updated = QtCore.pyqtSignal(str)
       
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
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
                if item[1] <  item2[1]:
                    self.foundupdate.emit('Radau atnaujinimą: ' + item2[0])
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

    def __del__(self):
        self.wait()
