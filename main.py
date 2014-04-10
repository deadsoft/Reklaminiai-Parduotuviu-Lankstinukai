#!/usr/bin/env python
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

'''pyinstaller --clean --hidden-import=PyQt4.QtXml --workpath=/tmp --specpath=/tmp/spec --distpath=/tmp/dist -s --noupx --onefile -n DeadProgram -y  /usr/lib/deadprogram/main.py'''

import sys, os
from PyQt4 import QtGui, QtCore
userdir = os.path.expanduser('~')
sys.path.insert(0, userdir + '/.cache/deadprogram/modules')
from deadprogram import Ui_MainWindow

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
#        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
 #       self.setAutoFillBackground(True)

if __name__ == "__main__":
#    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
#    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    app = QtGui.QApplication(sys.argv)
#    app.setDesktopSettingsAware(True)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
