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

import os, shutil
from PyQt4 import QtCore

userdir = os.path.expanduser('~')

class ImageDeleter(QtCore.QThread):
    finished = QtCore.pyqtSignal(str)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi']

    def __del__(self):
        self.wait()
        
    def run(self):
        for item in self.dirs:
            dirr = userdir + '/.cache/deadprogram/pdfs' + '/' + item
            for filename in os.listdir(dirr):
                if os.path.exists(os.path.join(dirr + '/dir_' + filename)):
                    shutil.rmtree(dirr + '/dir_' + filename)
        self.finished.emit('Ištryniau paveikslėlius')