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

import os, time, shutil
from PyQt4 import QtCore


userdir = os.path.expanduser('~')
version = 0.001

class OldPdfDeleter(QtCore.QThread):
    TxtInfo = QtCore.pyqtSignal(str)
    
    def __init__(self, timedays):
        QtCore.QThread.__init__(self)
        self.timedays = timedays
        self.dirs = ['Iki', 'Jysk', 'Maxima', 'Norfa', 'Rimi']
        
    def run(self):
			now = time.time()
			self.TxtInfo.emit('Trinu senus lankstinukus')
			for item in self.dirs:
				dirr = userdir + '/.cache/deadprogram/pdfs' + '/' + item
				for filename in os.listdir(dirr):
					try:
						if os.stat(os.path.join(dirr, filename)).st_mtime < now - self.timedays * 86400:
							if os.path.isfile(os.path.join(dirr, filename)):
								try:
									os.remove(os.path.join(dirr, filename))
									shutil.rmtree(dirr + '/dir_' + filename)
									self.TxtInfo.emit('Ištryniau: ' + filename)
								except:
									pass
					except:
						pass
			self.TxtInfo.emit('Baigiau trinti lankstinukus')
			return	
#			     now = time.time()
#                 t -= 5 * 24 * 60 * 60
			
    def __del__(self):
        self.wait()
