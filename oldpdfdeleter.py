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
version = 0.001

import os, time, shutil
from PyQt4 import QtCore

userdir = os.path.expanduser('~')

class OldPdfDeleter(QtCore.QThread):
    TxtInfo = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()
    
    def __init__(self, timedays):
        QtCore.QThread.__init__(self)
        self.timedays = timedays
        self.dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi']

    def __del__(self):
        self.wait()
        
    def run(self):
        time.sleep(1)
        now = time.time()
        for item in self.dirs:
            dirr = userdir + '/.cache/deadprogram/pdfs' + '/' + item
            for filename in os.listdir(dirr):
                try:
                    if os.stat(os.path.join(dirr, filename)).st_mtime < now - self.timedays * 86400:
                        if os.path.isfile(os.path.join(dirr, filename)):
                            try:
                                os.remove(os.path.join(dirr, filename))
                                shutil.rmtree(dirr + '/dir_' + filename)
                                self.TxtInfo.emit('Istryniau lankstinuka: ' + filename)
                            except:
                                pass
                except:
                    pass
        self.finished.emit()
        return	
#                 now = time.time()
#                 t -= 5 * 24 * 60 * 60

