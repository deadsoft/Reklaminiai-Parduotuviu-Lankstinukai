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

import urllib, sys, os, json, shutil, time
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork, Qt
userdir = os.path.expanduser('~')
sys.path.insert(0, userdir + '/.cache/deadprogram/modules')
import pdf2images, oldpdfdeleter, linkparser, updater

dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi']
if not os.path.exists(userdir + '/.cache/'):
    os.mkdir(userdir + '/.cache/')
if not os.path.exists(userdir + '/.cache/deadprogram/'):
    os.mkdir(userdir + '/.cache/deadprogram/')
if not os.path.exists(userdir + '/.cache/deadprogram/modules/'):
    os.mkdir(userdir + '/.cache/deadprogram/modules')
if not os.path.exists(userdir + '/.cache/deadprogram/modules/__init__.py'):
    open(userdir + '/.cache/deadprogram/modules/__init__.py', 'a').close()
if not os.path.exists(userdir + '/.cache/deadprogram/cache'):
    os.mkdir(userdir + '/.cache/deadprogram/cache')
if not os.path.exists(userdir + '/.cache/deadprogram/' + '/pdfs'):
    os.mkdir(userdir + '/.cache/deadprogram/' + '/pdfs')
for item in dirs:
    if not os.path.exists(userdir + '/.cache/deadprogram/' + '/pdfs/' + item):
        os.mkdir(userdir + '/.cache/deadprogram/' + '/pdfs/' + item)
if not os.path.exists(userdir + '/.cache/deadprogram/' + 'build'):
    shutil.copytree('/usr/share/deadprogram/build', userdir + '/.cache/deadprogram/' + 'build')
if not os.path.exists(userdir + '/.cache/deadprogram/' + 'icons'):
    shutil.copytree('/usr/share/deadprogram/icons', userdir + '/.cache/deadprogram/' + 'icons')
if not os.path.exists(userdir + '/.cache/deadprogram/' + 'web'):
    shutil.copytree('/usr/share/deadprogram/web', userdir + '/.cache/deadprogram/' + 'web')
        
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(853, 626)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans"))
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/image.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setBaseSize(QtCore.QSize(0, 0))
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.pdftab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pdftab.sizePolicy().hasHeightForWidth())
        self.pdftab.setSizePolicy(sizePolicy)
        self.pdftab.setObjectName(_fromUtf8("pdftab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.pdftab)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.comboBox_2 = QtGui.QComboBox(self.pdftab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QtCore.QSize(100, 27))
        self.comboBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        self.comboBox_2.setFont(font)
        self.comboBox_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.comboBox_2)
        self.comboBox_3 = QtGui.QComboBox(self.pdftab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setMinimumSize(QtCore.QSize(100, 27))
        self.comboBox_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.comboBox_3)
        self.comboBox_4 = QtGui.QComboBox(self.pdftab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setMinimumSize(QtCore.QSize(100, 27))
        self.comboBox_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.comboBox_4)
        self.comboBox_6 = QtGui.QComboBox(self.pdftab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_6.sizePolicy().hasHeightForWidth())
        self.comboBox_6.setSizePolicy(sizePolicy)
        self.comboBox_6.setMinimumSize(QtCore.QSize(100, 27))
        self.comboBox_6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox_6.setObjectName(_fromUtf8("comboBox_6"))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.comboBox_6)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.line_2 = QtGui.QFrame(self.pdftab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_4.addWidget(self.line_2)
        self.webView_2 = QtWebKit.QWebView(self.pdftab)
        self.webView_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.webView_2.setAutoFillBackground(False)
        self.webView_2.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView_2.setObjectName(_fromUtf8("webView_2"))
        self.verticalLayout_4.addWidget(self.webView_2)
        self.tabWidget.addTab(self.pdftab, _fromUtf8(""))
        self.Internettab = QtGui.QWidget()
        self.Internettab.setObjectName(_fromUtf8("Internettab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.Internettab)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Intbuttonmaxima = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Intbuttonmaxima.sizePolicy().hasHeightForWidth())
        self.Intbuttonmaxima.setSizePolicy(sizePolicy)
        self.Intbuttonmaxima.setMinimumSize(QtCore.QSize(100, 0))
        self.Intbuttonmaxima.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Intbuttonmaxima.setAcceptDrops(True)
        self.Intbuttonmaxima.setCheckable(True)
        self.Intbuttonmaxima.setChecked(False)
        self.Intbuttonmaxima.setFlat(False)
        self.Intbuttonmaxima.setObjectName(_fromUtf8("Intbuttonmaxima"))
        self.horizontalLayout_2.addWidget(self.Intbuttonmaxima)
        self.Intbuttonnorfa = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Intbuttonnorfa.sizePolicy().hasHeightForWidth())
        self.Intbuttonnorfa.setSizePolicy(sizePolicy)
        self.Intbuttonnorfa.setMinimumSize(QtCore.QSize(100, 0))
        self.Intbuttonnorfa.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Intbuttonnorfa.setCheckable(True)
        self.Intbuttonnorfa.setFlat(False)
        self.Intbuttonnorfa.setObjectName(_fromUtf8("Intbuttonnorfa"))
        self.horizontalLayout_2.addWidget(self.Intbuttonnorfa)
        self.Intbuttoniki = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Intbuttoniki.sizePolicy().hasHeightForWidth())
        self.Intbuttoniki.setSizePolicy(sizePolicy)
        self.Intbuttoniki.setMinimumSize(QtCore.QSize(100, 0))
        self.Intbuttoniki.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Intbuttoniki.setCheckable(True)
        self.Intbuttoniki.setFlat(False)
        self.Intbuttoniki.setObjectName(_fromUtf8("Intbuttoniki"))
        self.horizontalLayout_2.addWidget(self.Intbuttoniki)
        self.Intbuttonrimi = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Intbuttonrimi.sizePolicy().hasHeightForWidth())
        self.Intbuttonrimi.setSizePolicy(sizePolicy)
        self.Intbuttonrimi.setMinimumSize(QtCore.QSize(100, 0))
        self.Intbuttonrimi.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Intbuttonrimi.setCheckable(True)
        self.Intbuttonrimi.setFlat(False)
        self.Intbuttonrimi.setObjectName(_fromUtf8("Intbuttonrimi"))
        self.horizontalLayout_2.addWidget(self.Intbuttonrimi)
        self.comboBox = QtGui.QComboBox(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.comboBox.setFont(font)
        self.comboBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.setAcceptDrops(True)
        self.comboBox.setEditable(False)
        self.comboBox.setMaxVisibleItems(20)
        self.comboBox.setFrame(False)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout_2.addWidget(self.comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_9 = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_9.setAcceptDrops(True)
        self.pushButton_9.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/user-trash.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_9.setIcon(icon1)
        self.pushButton_9.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_9.setAutoRepeat(False)
        self.pushButton_9.setFlat(True)
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.horizontalLayout_2.addWidget(self.pushButton_9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.pushButton_5 = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMouseTracking(False)
        self.pushButton_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_5.setAutoFillBackground(False)
        self.pushButton_5.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/go-previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_5.setIcon(icon2)
        self.pushButton_5.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_5.setShortcut(_fromUtf8(""))
        self.pushButton_5.setAutoExclusive(False)
        self.pushButton_5.setAutoDefault(False)
        self.pushButton_5.setDefault(False)
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_4.addWidget(self.pushButton_5)
        self.pushButton_4 = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMouseTracking(False)
        self.pushButton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_4.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/go-next.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_4.setCheckable(False)
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_4.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMouseTracking(False)
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_3.setIcon(icon4)
        self.pushButton_3.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.pushButton = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMouseTracking(False)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/view-refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton.setIcon(icon5)
        self.pushButton.setIconSize(QtCore.QSize(24, 24))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.pushButton_22 = QtGui.QPushButton(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_22.sizePolicy().hasHeightForWidth())
        self.pushButton_22.setSizePolicy(sizePolicy)
        self.pushButton_22.setMouseTracking(False)
        self.pushButton_22.setFocusPolicy(QtCore.Qt.NoFocus)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/go-home.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_22.setIcon(icon6)
        self.pushButton_22.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_22.setFlat(True)
        self.pushButton_22.setObjectName(_fromUtf8("pushButton_22"))
        self.horizontalLayout_4.addWidget(self.pushButton_22)
        self.lineEdit = QtGui.QLineEdit(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(360, 0))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.lineEdit.setFont(font)
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit.setDragEnabled(True)
        self.lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.pushButton_2 = QtGui.QPushButton(self.Internettab)
        self.pushButton_2.setMouseTracking(True)
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8("../../../usr/share/deadprogram/icons/go-jump.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_2.setIcon(icon7)
        self.pushButton_2.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.progressBar_2 = QtGui.QProgressBar(self.Internettab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_2.sizePolicy().hasHeightForWidth())
        self.progressBar_2.setSizePolicy(sizePolicy)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.horizontalLayout_4.addWidget(self.progressBar_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.line_3 = QtGui.QFrame(self.Internettab)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_3.addWidget(self.line_3)
        self.webView = QtWebKit.QWebView(self.Internettab)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.webView.setFont(font)
        self.webView.setMouseTracking(False)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout_3.addWidget(self.webView)
        self.tabWidget.addTab(self.Internettab, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setContentsMargins(-1, 0, 0, -1)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.line_4 = QtGui.QFrame(self.tab)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout_11.addWidget(self.line_4)
        self.label_3 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_11.addWidget(self.label_3)
        self.checkboxmaxima = QtGui.QCheckBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkboxmaxima.sizePolicy().hasHeightForWidth())
        self.checkboxmaxima.setSizePolicy(sizePolicy)
        self.checkboxmaxima.setMinimumSize(QtCore.QSize(0, 0))
        self.checkboxmaxima.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkboxmaxima.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkboxmaxima.setAutoFillBackground(False)
        self.checkboxmaxima.setChecked(False)
        self.checkboxmaxima.setTristate(False)
        self.checkboxmaxima.setObjectName(_fromUtf8("checkboxmaxima"))
        self.verticalLayout_11.addWidget(self.checkboxmaxima)
        self.checkBoxnorfa = QtGui.QCheckBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxnorfa.sizePolicy().hasHeightForWidth())
        self.checkBoxnorfa.setSizePolicy(sizePolicy)
        self.checkBoxnorfa.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBoxnorfa.setChecked(False)
        self.checkBoxnorfa.setObjectName(_fromUtf8("checkBoxnorfa"))
        self.verticalLayout_11.addWidget(self.checkBoxnorfa)
        self.checkBoxiki = QtGui.QCheckBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxiki.sizePolicy().hasHeightForWidth())
        self.checkBoxiki.setSizePolicy(sizePolicy)
        self.checkBoxiki.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBoxiki.setChecked(False)
        self.checkBoxiki.setObjectName(_fromUtf8("checkBoxiki"))
        self.verticalLayout_11.addWidget(self.checkBoxiki)
        self.checkBoxrimi = QtGui.QCheckBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxrimi.sizePolicy().hasHeightForWidth())
        self.checkBoxrimi.setSizePolicy(sizePolicy)
        self.checkBoxrimi.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBoxrimi.setObjectName(_fromUtf8("checkBoxrimi"))
        self.verticalLayout_11.addWidget(self.checkBoxrimi)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.pushButtondownloadpdf = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtondownloadpdf.sizePolicy().hasHeightForWidth())
        self.pushButtondownloadpdf.setSizePolicy(sizePolicy)
        self.pushButtondownloadpdf.setMinimumSize(QtCore.QSize(85, 0))
        self.pushButtondownloadpdf.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtondownloadpdf.setObjectName(_fromUtf8("pushButtondownloadpdf"))
        self.horizontalLayout_8.addWidget(self.pushButtondownloadpdf)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout_11.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBox_4 = QtGui.QCheckBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_4.sizePolicy().hasHeightForWidth())
        self.checkBox_4.setSizePolicy(sizePolicy)
        self.checkBox_4.setBaseSize(QtCore.QSize(0, 0))
        self.checkBox_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.horizontalLayout_6.addWidget(self.checkBox_4)
        self.spinBox_3 = QtGui.QSpinBox(self.tab)
        self.spinBox_3.setMaximum(30)
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.horizontalLayout_6.addWidget(self.spinBox_3)
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_11.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkBox_3 = QtGui.QCheckBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_3.sizePolicy().hasHeightForWidth())
        self.checkBox_3.setSizePolicy(sizePolicy)
        self.checkBox_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.horizontalLayout_3.addWidget(self.checkBox_3)
        self.spinBox = QtGui.QSpinBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(365)
        self.spinBox.setSingleStep(5)
        self.spinBox.setProperty("value", 180)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_3.addWidget(self.spinBox)
        self.label_2 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.pushButton_8 = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.horizontalLayout_3.addWidget(self.pushButton_8)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_11.addLayout(self.horizontalLayout_3)
        self.line = QtGui.QFrame(self.tab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_11.addWidget(self.line)
        self.verticalLayout.addLayout(self.verticalLayout_11)
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.checkBox_2 = QtGui.QCheckBox(self.tab)
        self.checkBox_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox_2.setChecked(False)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.horizontalLayout_7.addWidget(self.checkBox_2)
        self.spinBox_2 = QtGui.QSpinBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(30)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.horizontalLayout_7.addWidget(self.spinBox_2)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_7.addWidget(self.label_4)
        self.pushButton_7 = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.horizontalLayout_7.addWidget(self.pushButton_7)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.line_6 = QtGui.QFrame(self.tab)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.verticalLayout.addWidget(self.line_6)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.pushButtoncanceldownloadpdf = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtoncanceldownloadpdf.sizePolicy().hasHeightForWidth())
        self.pushButtoncanceldownloadpdf.setSizePolicy(sizePolicy)
        self.pushButtoncanceldownloadpdf.setMinimumSize(QtCore.QSize(85, 0))
        self.pushButtoncanceldownloadpdf.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtoncanceldownloadpdf.setObjectName(_fromUtf8("pushButtoncanceldownloadpdf"))
        self.horizontalLayout_12.addWidget(self.pushButtoncanceldownloadpdf)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plainTextEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.plainTextEdit.setAcceptDrops(False)
        self.plainTextEdit.setAutoFillBackground(True)
        self.plainTextEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.plainTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setUndoRedoEnabled(True)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.progressBar = QtGui.QProgressBar(self.tab)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.checkBox = QtGui.QCheckBox(self.tab_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout_5.addWidget(self.checkBox)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem9)
        self.pushButton_6 = QtGui.QPushButton(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_6.setDefault(False)
        self.pushButton_6.setFlat(False)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.verticalLayout_5.addWidget(self.pushButton_6)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Reklaminiai Parduotuvių Lankstinukai", None))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Maxima", None))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Norfa", None))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "Iki", None))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "Rimi", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pdftab), _translate("MainWindow", "Lankstinukai", None))
        self.Intbuttonmaxima.setText(_translate("MainWindow", "Maxima", None))
        self.Intbuttonnorfa.setText(_translate("MainWindow", "Norfa", None))
        self.Intbuttoniki.setText(_translate("MainWindow", "Iki", None))
        self.Intbuttonrimi.setText(_translate("MainWindow", "Rimi", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Internettab), _translate("MainWindow", "Internetas", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600;\">Lankstinukų atnaujinimas</span><br/></p></body></html>", None))
        self.checkboxmaxima.setText(_translate("MainWindow", "Maxima", None))
        self.checkBoxnorfa.setText(_translate("MainWindow", "Norfa", None))
        self.checkBoxiki.setText(_translate("MainWindow", "Iki", None))
        self.checkBoxrimi.setText(_translate("MainWindow", "Rimi", None))
        self.pushButtondownloadpdf.setText(_translate("MainWindow", "Tikrinti ir atsiųsti dabar", None))
        self.checkBox_4.setText(_translate("MainWindow", "Automatiškai tikrinti ar yra naujų lankstinukų kas  ", None))
        self.label_5.setText(_translate("MainWindow", "  dienų  ", None))
        self.checkBox_3.setText(_translate("MainWindow", "Automatiškai trinti senus lankstinukus po  ", None))
        self.label_2.setText(_translate("MainWindow", "  dienų    ", None))
        self.pushButton_8.setText(_translate("MainWindow", "Trinti dabar", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600;\">Programos atnaujinimas</span><br/></p></body></html>", None))
        self.checkBox_2.setText(_translate("MainWindow", "Automatiškai tikrinti įjungiant programą kas  ", None))
        self.label_4.setText(_translate("MainWindow", "  dienų  ", None))
        self.pushButton_7.setText(_translate("MainWindow", "Tikrinti ir atsiųsti dabar", None))
        self.pushButtoncanceldownloadpdf.setText(_translate("MainWindow", "Perkrauti programą", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Naujinimas", None))
        self.checkBox.setText(_translate("MainWindow", "Naudoti pdf.js", None))
        self.pushButton_6.setText(_translate("MainWindow", "Perkrauti programą", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Nustatymai", None))

        
        self.downloadlist = []
        self.threads = []
        self.loadpdfjs = False
        self.downloading = False
        self.checkforpdfupdates = False
        self.deletingoldpdfs = False
        self.downlopdedpdfs = False
        self.combohighlighted = int
        self.lastprogramupdatechecktime = 1
        self.lastpdfupdatechecktime = 1
        
        self.comboBox.highlighted.connect(self.comboboxlasthighlighted)
        self.Intbuttonmaxima.pressed.connect(lambda: self.loadurl(self.Intbuttonmaxima))
        self.Intbuttonnorfa.clicked.connect(lambda: self.loadurl(self.Intbuttonnorfa))
        self.Intbuttoniki.clicked.connect(lambda: self.loadurl(self.Intbuttoniki))
        self.Intbuttonrimi.clicked.connect(lambda: self.loadurl(self.Intbuttonrimi))
        self.pushButtoncanceldownloadpdf.clicked.connect(self.restart)
        self.pushButton_22.clicked.connect(lambda: self.webView.load(QtCore.QUrl("about:blank")))
        self.pushButton.clicked.connect(self.webView.reload)
        self.pushButton_3.clicked.connect(self.webView.stop)
        self.pushButton_4.clicked.connect(self.webView.forward)
        self.pushButton_5.clicked.connect(self.webView.back)
        self.pushButton_2.clicked.connect(self.loadurlfromlineedit)
        self.pushButton_6.clicked.connect(self.restart)
        self.pushButton_7.clicked.connect(self.checkforprogramupdates)
        self.pushButton_8.clicked.connect(self.deleteoldpdfs)
        self.pushButton_8.clicked.connect(self.stupidworkaround)
        self.webView.loadStarted.connect(self.updatelineedit)
        self.webView.loadFinished.connect(self.updatelineedit)
        self.webView.urlChanged.connect(self.updatelineedit)
        self.lineEdit.returnPressed.connect(self.loadurlfromlineedit)
        self.webView.loadProgress.connect(self.pageloadprogress)
        self.pushButtondownloadpdf.clicked.connect(self.updatepdfs)
        self.comboBox.activated.connect(self.loadsite)
        self.comboBox_2.activated.connect(lambda: self.loadpdf(self.comboBox_2))
        self.comboBox_3.activated.connect(lambda: self.loadpdf(self.comboBox_3))
        self.comboBox_4.activated.connect(lambda: self.loadpdf(self.comboBox_4))
        self.comboBox_6.activated.connect(lambda: self.loadpdf(self.comboBox_6))
        self.combolist = [('Maxima', self.comboBox_2), ('Rimi', self.comboBox_6), ('Iki', self.comboBox_4), ('Norfa', self.comboBox_3)]
        self.checkboxlist = [self.checkboxmaxima, self.checkBoxrimi, self.checkBoxiki, self.checkBoxnorfa]
        self.pushbuttonlist = [self.Intbuttonmaxima, self.Intbuttonnorfa, self.Intbuttoniki, self.Intbuttonrimi]
        
        self.lineEdit.insert('about:blank')
        self.lineEdit.setDragEnabled(True)
        self.lineEdit.installEventFilter(self)
        self.comboBox.installEventFilter(self)
        self.comboBox.setAcceptDrops(True)
        self.pushButton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_9.installEventFilter(self)
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBoxview = self.comboBox.view()
        self.comboBoxview.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        
        settings = self.webView.settings()
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        settings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.JavaEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.DnsPrefetchEnabled, True)
        settings.setLocalStoragePath(userdir  + '/.cache/deadprogram/cache')
        settings.setMaximumPagesInCache(20)
        settings.setOfflineStoragePath(userdir  + '/.cache/deadprogram/cache')
#        settings.userStyleSheetUrl(QtCore.QUrl(curentdir  + '/css'))
        
        settings_2 = self.webView_2.settings()
        settings_2.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavaEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.DnsPrefetchEnabled, True)
        settings_2.setLocalStoragePath(userdir  + '/.cache/deadprogram/cache')
        settings_2.setMaximumPagesInCache(20)
        settings_2.setOfflineStoragePath(userdir  + '/.cache/deadprogram/cache')
#        settings_2.userStyleSheetUrl(QtCore.QUrl(curentdir  + '/css'))
        
        self.readSettings()
        self.addbrowserbookmarks()
        self.loadpdfcomboboxes()
        
#       if not self.loadpdfjs and self.downlopdedpdfs
        if not self.loadpdfjs:
            self.downlopdedpdfs = True            
            self.createhtmlfrompdf()
            
        if self.loadpdfjs:
            self.webView_2.load(QtCore.QUrl('file://' + userdir + '/.cache/deadprogram/web/viewer.html?pdfurl=pdftoload.pdf'))
        else:
            self.webView_2.load(QtCore.QUrl('about:blank'))        
        
        self.downloader = QtWebKit.QWebView()
        self.downloader.page().setForwardUnsupportedContent(True)
        self.downloader.page().unsupportedContent.connect(self.downloadstart)
        self.downloadmanager = QtNetwork.QNetworkAccessManager()
        self.downloadmanager.finished.connect(self.downloadfinished)

    def loadpdfcomboboxes(self):
        for item in self.combolist:
            shop = item[0]
#            pdfsinshopsdir = os.listdir(userdir + '/.cache/deadprogram/pdfs/' + shop + '/')
            pdfsinshopsdir = sorted(os.listdir(userdir + '/.cache/deadprogram/pdfs/' + shop + '/'), key=lambda p: os.path.getctime(os.path.join(userdir + '/.cache/deadprogram/pdfs/' + shop + '/', p)))
            pdfss = []
            for pdf in pdfsinshopsdir:
                if not pdf.startswith('dir_'):
                    pdfss.append(pdf)
            item[1].clear()
            item[1].addItem(shop)
            item[1].addItems(pdfss)

    def createhtmlfrompdf(self):
        b = pdf2images.imagesFromPdf()
        self.threads.append(b)
        self.threads[len(self.threads)-1].FinishedExtractingImages.connect(self.addtxt)
        self.threads[len(self.threads)-1].reloadcomboboxes.connect(self.loadpdfcomboboxes)
        self.threads[len(self.threads)-1].reloadcomboboxes.connect(self.downlopdedpdfsfalse)
        b.start()
        

    def downlopdedpdfsfalse(self):
        self.downlopdedpdfs = False
        
    def loadurlfromlineedit(self):
        url = str(self.lineEdit.displayText())
        if url.startswith('http://'):
            self.webView.load(QtCore.QUrl(url))
        elif url.startswith('www.'):
            self.webView.load(QtCore.QUrl('http://' + url))
        elif url.startswith('/'):
            self.webView.load(QtCore.QUrl('file://' + url))
        else:
            self.webView.load(QtCore.QUrl('http://www.' + url))
        
    def comboboxlasthighlighted(self, num):
        self.combohighlighted = num
        
    def eventFilter(self, source, event):        
        #help(QtCore.QEvent)
        #print event.type(), event, source
        if (event.type() == 60 and source is self.comboBox):
            event.accept()				
        if (event.type() == 63 and source is self.comboBox):
            if event.mimeData().hasFormat('text/plain'):
                event.accept()
                source.addItem(event.mimeData().text())
        if (event.type() == 60 and source is self.pushButton_9):
            if not event.mimeData().hasFormat('text/plain'):
                event.accept()
        if (event.type() == 63 and source is self.pushButton_9):
            if not event.mimeData().hasFormat('text/plain'):
                event.accept()
                self.comboBox.removeItem(self.combohighlighted)
        if (event.type() == 60 and source is self.lineEdit):
            event.ignore()

        return QtGui.QWidget.eventFilter(self, source, event)
        
    def pageloadprogress(self, n):
        self.progressBar_2.setProperty("value", n) 
        
    def loadsite(self):
        for item in self.pushbuttonlist:
            item.setChecked(False)
        self.webView.load(QtCore.QUrl(self.comboBox.currentText()))

    def savebrowserbookmarks(self):
        lst = []
        for n in range(self.comboBox.count()):
            lst.append(('Site title', str(self.comboBox.itemText(n))))
        f = open(userdir + '/.cache/deadprogram/browserbookmarks.txt', 'w')
        json.dump(lst, f,  indent=4)
        f.close()


    def addbrowserbookmarks(self):
        try:
            f = open(userdir + '/.cache/deadprogram/browserbookmarks.txt', 'r')
            lst = json.load(f)
            for tpl in lst:
                self.comboBox.addItem(tpl[1])
        except:
                pass

    def infobox(self, text):
        box = QtGui.QMessageBox()
        box.setText(unicode(text, "utf-8"))
#        box.setAutoFillBackground(True)
#        box.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#        box.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#        box.setBackgroundRole(QtGui.QPalette.Base)
#        box.setFocusPolicy(QtCore.Qt.StrongFocus)
#        box.setWindowOpacity(0.5)
        box.exec_()
        
    def closeEvent(self, event):
        if self.downlopdedpdfs:
            event.ignore()
            self.infobox('Apdirbu lankstinukus ir išsijungt kolkas negaliu       \nTiesiog palauk kažkiek...')
        else:
            self.writeSettings()
            event.accept()
            

    def readSettings(self):
        settings = QtCore.QSettings("deadprogram", "lankstukai")
        self.resize(settings.value("winsize").toSize())
        self.move(settings.value("winpos").toPoint())
        for item in self.checkboxlist:
             if settings.value(item.text()).toBool():
                item.setChecked(True)
        self.tabWidget.setCurrentIndex(settings.value("activetab").toInt()[0])
        if settings.value("pdfjs").toBool():
            self.checkBox.setChecked(True)
            self.loadpdfjs = True
        if settings.value("pdfupdateindays").toInt()[1]:
            self.lastprogramupdatechecktime = settings.value("pdfupdateindays").toInt()[0]
        if settings.value("lastprogramupdatechecktime").toInt()[1]:
            self.lastprogramupdatechecktime = settings.value("lastprogramupdatechecktime").toInt()[0]
        if settings.value("checkprogramforupdates").toBool():
            self.checkBox_2.setChecked(True)
            if self.lastprogramupdatechecktime <= int(time.strftime("%Y%m%d")) - settings.value("programupdateindays").toInt()[0]:
                self.checkforprogramupdates()
                self.lastprogramupdatechecktime = int(time.strftime("%Y%m%d"))
        if settings.value("programupdateindays").toInt()[1]:
            self.spinBox_2.setValue(settings.value("programupdateindays").toInt()[0])
        if settings.value("pdfupdateindays").toInt()[1]:
            self.spinBox_3.setValue(settings.value("pdfupdateindays").toInt()[0])
        if settings.value("lastpdfupdatechecktime").toInt()[1]:
            self.lastpdfupdatechecktime = settings.value("lastpdfupdatechecktime").toInt()[0]
        if settings.value("autoupdatepdfs").toBool():
            self.checkBox_4.setChecked(True)
            if self.lastpdfupdatechecktime <= int(time.strftime("%Y%m%d")) - settings.value("pdfupdateindays").toInt()[0]:
                self.updatepdfs()
                self.lastpdfupdatechecktime = int(time.strftime("%Y%m%d"))
        if settings.value("autodelpdfs").toBool():
            self.checkBox_3.setChecked(True)
            self.deleteoldpdfs()
        if settings.value("autodelpdfstime").toInt()[1]:
            self.spinBox.setValue(settings.value("autodelpdfstime").toInt()[0])
        
        
    def writeSettings(self):
        settings = QtCore.QSettings("deadprogram", "lankstukai")
        settings.setValue("winsize", self.size())
        settings.setValue("winpos", self.pos())
        for item in self.checkboxlist:
            settings.setValue(item.text(), item.isChecked())
        settings.setValue("activetab", self.tabWidget.currentIndex())
        settings.setValue("pdfjs", self.checkBox.isChecked())
        settings.setValue("autoupdatepdfs", self.checkBox_4.isChecked())
        settings.setValue("checkprogramforupdates", self.checkBox_2.isChecked())
        settings.setValue("lastprogramupdatechecktime", self.lastprogramupdatechecktime)
        settings.setValue("pdfupdateindays", self.spinBox_3.value())
        settings.setValue("programupdateindays", self.spinBox_2.value())
        settings.setValue("lastpdfupdatechecktime", self.lastpdfupdatechecktime)
        settings.setValue("downlopdedpdfs", self.downlopdedpdfs)
        settings.setValue("autodelpdfs", self.checkBox_3.isChecked())
        settings.setValue("autodelpdfstime", self.spinBox.value())
        self.savebrowserbookmarks()        
        
    def deleteoldpdfs(self):
        a = oldpdfdeleter.OldPdfDeleter(self.spinBox.value())
        self.threads.append(a)
        self.threads[len(self.threads)-1].TxtInfo.connect(self.addtxt)
        a.start()

    def stupidworkaround(self):
        self.plainTextEdit.appendPlainText(unicode('Jei yra trinu senus lankstinukus', "utf-8"))
            
    def checkforprogramupdates(self):
        self.plainTextEdit.appendPlainText(unicode('Tikrinu ar nėra programos atnaujinimo', "utf-8"))
        b = updater.Updater()
        self.threads.append(b)
        self.threads[len(self.threads)-1].foundupdate.connect(self.addtxt)
        self.threads[len(self.threads)-1].updated.connect(self.addtxt)
        b.start()
 
    def loadpdf(self, combobox):
        index = combobox.currentIndex()
        if index != 0:
            if self.loadpdfjs:
                pdf = userdir + '/.cache/deadprogram/pdfs/' + combobox.itemText(0) + '/' + combobox.itemText(index)
                if os.path.exists(userdir + '/.cache/deadprogram/web/pdftoload.pdf'):
                    os.remove(userdir + '/.cache/deadprogram/web/pdftoload.pdf')
                os.link(pdf, userdir + '/.cache/deadprogram/web/pdftoload.pdf')
                self.webView_2.load(QtCore.QUrl('file://' + userdir + '/.cache/deadprogram/web/viewer.html?pdfurl=pdftoload.pdf'))
                for item in self.combolist:
                    shop = item[0]
                    if shop != str(combobox.itemText(combobox.currentIndex())):
                        item[1].setCurrentIndex(0)
            else:
                html = 'file://' + userdir + '/.cache/deadprogram/pdfs/' + combobox.itemText(0) + '/dir_' + combobox.itemText(index) + '/index.html'
                self.webView_2.load(QtCore.QUrl(html))
                for item in self.combolist:
                    shop = item[0]
                    if shop != combobox.itemText(combobox.currentIndex()):
                        item[1].setCurrentIndex(0)
                
    def updatepdfs(self):
        if not self.checkforpdfupdates:
            self.checkforpdfupdates = True
            queue_list = []
            for item in self.checkboxlist:
                if item.isChecked():
                    queue_list.append(str(item.text()))
            lnk = linkparser.LinkParser(queue_list)
            self.threads.append(lnk)
            self.threads[len(self.threads)-1].addtext.connect(self.addtxt)
            self.threads[len(self.threads)-1].url.connect(self.addurltodwnlist)
            self.threads[len(self.threads)-1].finishedurlparsing.connect(self.downloadpdfs)
            lnk.start()
        
    def addurltodwnlist(self, shop, url):
        self.downloadlist.append((str(shop), str(url)))

    def addtxt(self, txt):
        self.plainTextEdit.appendPlainText(unicode(txt, "utf-8"))

    def updatelineedit(self):
        self.lineEdit.clear()
        self.lineEdit.insert(self.webView.url().toString())

    def loadurl(self, button):
        urllist = ([('Maxima', 'http://www.maxima.lt/akcijos/akcijos-ir-nuolaidos/'), 
        ('Rimi', 'http://www.rimi.lt/rimi-pasiulymai'), 
        ('Norfa', 'http://www.norfa.lt/lt/akcijos/vykdomos_akcijos/'), 
        ('Iki', 'http://iki.lt/lt.php/akcijos/pasiulymai')])
        
        for item in urllist:
            if item[0] == button.text():
               self.webView.load(QtCore.QUrl(item[1]))
        for item in self.pushbuttonlist:
            if item.text() != button.text():
                item.setChecked(False)
                
    def restart(self):
        self.writeSettings()
        python = sys.executable
        os.execl(python, python, * sys.argv)
        return
                
    def downloadpdfs(self):
        if not self.downloading:
            self.downloading = True
            for shop, url in self.downloadlist:
                self.downloadlist.remove((shop, url))
                self.shop = str(shop)
                self.url = str(url)
                if not os.path.exists(userdir + '/.cache/deadprogram/pdfs/' + self.shop + '/' + os.path.basename(self.url).split('?utm_source')[0]):
                    self.downloader.load(QtCore.QUrl(self.url))
                    break

    def downloadstart(self, reply):
        self.request = reply.request()
        self.request.setUrl(reply.url())
        self.reply = self.downloadmanager.get(self.request)
        self.reply.downloadProgress.connect(self.dloadprogr)
        self.plainTextEdit.appendPlainText(unicode('Atsiunčiu lankstinuką: ' + os.path.basename(str(self.reply.url().path())), "utf-8"))
        

    def dloadprogr(self, fromb, tob):
        self.progressBar.setProperty("value", int(float(fromb) / float(tob) * 100))      

    def downloadfinished(self, dl):
        self.plainTextEdit.appendPlainText(unicode('Lankstinuko atsiuntimas baigtas: ' + os.path.basename(str(self.reply.url().path())), "utf-8"))
        f = open(userdir + '/.cache/deadprogram/pdfs/' + self.shop + '/' + os.path.basename(self.url).split('?utm_source')[0], 'wb')
        f.write(dl.readAll())
        f.flush()
        f.close()
        self.downloading = False
        self.downloadpdfs()
        if len(self.downloadlist) == 0:
            self.downlopdedpdfs = True
            self.checkforpdfupdates = False
            if not self.loadpdfjs and self.downlopdedpdfs:
                self.createhtmlfrompdf()
