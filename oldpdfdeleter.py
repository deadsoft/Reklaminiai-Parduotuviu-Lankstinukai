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
version = 0.005

import os, time, shutil
from PyQt4 import QtCore

def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path
    
userprogpath = SEP('/.cache/deadprogram/')
userdir = os.path.expanduser('~')

class OldPdfDeleter(QtCore.QThread):
    TxtInfo = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()
    
    def __init__(self, timedays):
        QtCore.QThread.__init__(self)
        self.timedays = timedays
        self.dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi', 'Aibe' , 'FRESH_MARKET', 'Senukai', 'Moki_Vezi']

    def __del__(self):
        self.wait()
        
    def run(self):
        time.sleep(1)
        now = time.time()
        for item in self.dirs:
            dirr = userdir + userprogpath + SEP('pdfs/') + item
            for filename in os.listdir(dirr):
                    if os.path.isfile(os.path.join(dirr, filename)):
                        if os.stat(os.path.join(dirr, filename)).st_mtime < now - self.timedays * 86400:
                            try:
                                os.remove(os.path.join(dirr, filename))
                                shutil.rmtree(dirr + SEP('/dir_') + filename)
                                self.TxtInfo.emit('Ištryniau lankstinuką: ' + filename)
                            except:
                                self.TxtInfo.emit('Nepavyko ištrinti lankstinuko: '  + filename)
        self.finished.emit()
        return	
#                 now = time.time()
#                 t -= 5 * 24 * 60 * 60

