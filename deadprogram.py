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

'''pyinstaller --clean --hidden-import=PyQt4.QtXml --workpath=/tmp --specpath=/tmp/spec --distpath=/tmp/dist -s --noupx --onefile -n DeadProgram -y  /usr/lib/deadprogram/main.py'''

version = 0.001

def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path

import platform
if platform.system() == "Windows":
    import win32file
from base64 import b64encode
from PyQt4.QtGui import QPainter
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from gui import Ui_MainWindow
from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import pyqtSlot as Slot
import urllib, sys, os, json, shutil, time

userdir = os.path.expanduser('~')
userprogpath = SEP('/.cache/deadprogram/')
sys.path.insert(0, userdir + userprogpath + 'modules')

import pdf2images, oldpdfdeleter, linkparser, updater, imagedeleter

dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi']

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


class DeadProgram(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
             
        self.downloadlist = []
        self.threads = []
        self.loadpdfjs = False
        self.downloading = False
        self.checkforpdfupdates = False
        self.deletingoldpdfs = False
        self.downlopdedpdfs = False
        self.usecsszoom = False
        self.fullScreen = False
        self.combohighlighted = 0
        self.lastprogramupdatechecktime = 1
        self.lastpdfupdatechecktime = 1
        self.pdftoimagesdpi = 150
        self.currentpdfpage = 1
        self.numofpdfpages = 0
        self.currenthtmlpath = str
        
        self.doubleSpinBox.valueChanged.connect(self.setzoomincss)
        self.tabWidget.currentChanged.connect(self.tabchangedwindowtitle)
        self.checkBox.stateChanged.connect(self.pdfjscheckboxstatechanged)
        self.checkBox_5.stateChanged.connect(self.cssscalecheckboxstatechanged)
        self.comboBox.highlighted.connect(self.comboboxlasthighlighted)
        self.Intbuttonmaxima.pressed.connect(lambda: self.loadurl(self.Intbuttonmaxima))
        self.Intbuttonnorfa.clicked.connect(lambda: self.loadurl(self.Intbuttonnorfa))
        self.Intbuttoniki.clicked.connect(lambda: self.loadurl(self.Intbuttoniki))
        self.Intbuttonrimi.clicked.connect(lambda: self.loadurl(self.Intbuttonrimi))
        self.pushButton_22.clicked.connect(lambda: self.webView.load(QtCore.QUrl("about:blank")))
        self.pushButton.clicked.connect(self.webView.reload)
        self.pushButton_3.clicked.connect(self.webView.stop)
        self.pushButton_4.clicked.connect(self.webView.forward)
        self.pushButton_5.clicked.connect(self.webView.back)
        self.pushButton_2.clicked.connect(self.loadurlfromlineedit)
        self.pushButton_7.clicked.connect(self.checkforprogramupdates)
        self.pushButton_8.clicked.connect(lambda: self.deleteoldpdfs(self.spinBox.value()))
        self.pushButton_8.clicked.connect(self.stupidworkaround)
        self.pushButton_10.clicked.connect(self.deleteimages)
        self.pushButton_6.clicked.connect(self.nextpage)
        self.pushButton_11.clicked.connect(self.previouspage)
#        self.pushButton_10.setEnabled(False)
        self.webView.loadStarted.connect(self.updatelineedit)
        self.webView.loadFinished.connect(self.updatelineedit)
        self.webView.urlChanged.connect(self.updatelineedit)
        self.webView.linkClicked.connect(self.webviewlinkclicked)
        self.webView.statusBarMessage.connect(self.webviewstatusbarmessage)
        self.webView.titleChanged.connect(self.webviewtitlechanged)
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

        if platform.system() == "Windows":
            self.checkBox.setEnabled(False)
        
        self.lineEdit.insert('about:blank')
        self.lineEdit.setDragEnabled(True)
        self.lineEdit.installEventFilter(self)
        self.comboBox.installEventFilter(self)
        self.comboBox.setAcceptDrops(True)
        self.pushButton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_9.installEventFilter(self)
        self.comboBoxview = self.comboBox.view()
        self.comboBoxview.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        
        QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self.toogleFullScreen)
        
        webpage = self.webView.page()
        webpage.unsupportedContent.connect(self.webpageunsupportedcontent)
        webpage.linkHovered.connect(self.webpagelinkhovered)
        webpage.setForwardUnsupportedContent(True)
        webpage.setLinkDelegationPolicy(QtWebKit.QWebPage.DontDelegateLinks)
        
        settings = self.webView.settings()
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        settings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, False)
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptCanAccessClipboard, False)
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, False)
        settings.setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.JavaEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, False)
        settings.setAttribute(QtWebKit.QWebSettings.DnsPrefetchEnabled, True)
        settings.setLocalStoragePath(userdir  + userprogpath + 'cache')
        settings.setMaximumPagesInCache(20)
        settings.setOfflineStoragePath(userdir  + userprogpath + 'cache')
        
        self.webView_2.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.HighQualityAntialiasing)
        self.webView.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.HighQualityAntialiasing)

        self.webView_2.loadFinished.connect(self.onLoad)
        
        self.settings_2 = self.webView_2.settings()
        self.settings_2.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptCanAccessClipboard, True)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.JavaEnabled, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, False)
        self.settings_2.setAttribute(QtWebKit.QWebSettings.DnsPrefetchEnabled, False)
        self.settings_2.setLocalStoragePath(userdir  + userprogpath + 'cache')
        self.settings_2.setMaximumPagesInCache(20)
        self.settings_2.setOfflineStoragePath(userdir  + userprogpath + 'cache')

        self.myHub = Hub()
        self.myHub.on_client_event.connect(self.setcurrentpdfpage)
        self.page_2 = self.webView_2.page()
        self.page_2.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.frame_2 = self.page_2.mainFrame()

        self.readSettings()
        self.addbrowserbookmarks()
        self.loadpdfcomboboxes()
        os.chdir(userdir + userprogpath)

        
        if not self.loadpdfjs:
            self.downlopdedpdfs = True            
            self.createhtmlfrompdf()
            
        if self.loadpdfjs:
            if platform.system() == "Windows":
                if platform.release() == 'XP':
                    pass
                else:
                    self.webView_2.load(QtCore.QUrl(userdir + userprogpath + SEP('web/viewer.html?file=pdftoload.pdf')))
            else:
                self.webView_2.load(QtCore.QUrl(userdir + userprogpath + SEP('web/viewer.html?file=pdftoload.pdf')))
        else:
            self.loadcurrenthtml()
            
        self.downloader = QtWebKit.QWebView()
        self.downloader.page().setForwardUnsupportedContent(True)
        self.downloader.page().unsupportedContent.connect(self.downloadstart)
        self.downloadmanager = QtNetwork.QNetworkAccessManager()
        self.downloadmanager.finished.connect(self.downloadfinished)

    def setcurrentpdfpage(self, page):
        self.currentpdfpage = int(page)

    def onLoad(self):
        self.frame_2.addToJavaScriptWindowObject("my_hub", self.myHub)
#        self.frame_2.evaluateJavaScript("ApplicationIsReady()")

    def htmldata(self, htmlfile):
        f = open(htmlfile, 'r')
        html = f.read()
        f.close()
        return html

    def comboboxesenabledisable(self, info):
        if info == 'enable':
            for a, item in self.combolist:
                item.setEnabled(True)
        elif info == 'disable':
            for a, item in self.combolist:
                item.setEnabled(False)
        
    def toogleFullScreen(self):
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()            
        self.fullScreen = not (self.fullScreen)

    def cssscalecheckboxstatechanged(self, state):
        if state == 2:
            self.loadcustomcss()
        elif state == 0:
            self.settings_2.setUserStyleSheetUrl(QtCore.QUrl(''))
            self.usecsszoom = False

    def loadcustomcss(self):
        css = b64encode('img {zoom:' + str(self.doubleSpinBox.value()) + '!important;}')
        self.settings_2.setUserStyleSheetUrl(QtCore.QUrl('data:text/css;charset=utf-8;base64,' + css ))
        self.usecsszoom = True

    def setzoomincss(self, value):
        if self.usecsszoom:
            css = b64encode('img{zoom:' + str(value) + '  !important;}')
            self.settings_2.setUserStyleSheetUrl(QtCore.QUrl('data:text/css;charset=utf-8;base64,' + css ))
            self.loadcurrenthtml()

    def deleteimages(self):
        a = imagedeleter.ImageDeleter()
        self.threads.append(a)
        self.threads[len(self.threads)-1].finished.connect(self.addtxt)
        a.start()
        self.downlopdedpdfs = True
        self.createhtmlfrompdf()

    def deletecssscalingfromhtmls(self):
        dirs = ['Iki', 'Maxima', 'Norfa', 'Rimi']
        for item in dirs:
            dirr = userdir + userprogpath + SEP('pdfs/') + item
            for filename in os.listdir(dirr):
                if os.path.exists(os.path.join(dirr + SEP('/dir_') + filename)):                   
                        f = open(dirr + SEP('/dir_') + filename + SEP('/index.html'), 'r')
                        data = f.read()
                        f.close()
                        newfiledata = data.replace('    width:98%;', ' ')
                        f = open(dirr + SEP('/dir_') + filename + SEP('/index.html'), 'w')
                        f.write(newfiledata)
                        f.close()
        
    def tabchangedwindowtitle(self, i):
        self.setWindowTitle(self.tabWidget.tabText(i))

    def pdfjscheckboxstatechanged(self, state):
        if state == 2:
            self.loadpdfjs = True
            self.doubleSpinBox.setEnabled(False)
            self.checkBox_5.setEnabled(False)
            self.webView_2.load(QtCore.QUrl(userdir + userprogpath + SEP('web/viewer.html?file=pdftoload.pdf')))
        elif state == 0:
            self.loadpdfjs = False
            self.doubleSpinBox.setEnabled(True)
            self.checkBox_5.setEnabled(True)
            if not self.downlopdedpdfs:
                self.downlopdedpdfs = True
                self.createhtmlfrompdf()
                self.loadcurrenthtml()
                
    def loadcurrenthtml(self):
        try:
            if platform.system() == "Windows":
                if platform.release() == 'XP':
                    pass
                else:
                    self.webView_2.load(QtCore.QUrl(self.currenthtmlpath  + '#' + str(self.currentpdfpage)))
            else:            
                self.webView_2.load(QtCore.QUrl(self.currenthtmlpath  + '#' + str(self.currentpdfpage)))
        except:
            pass
                
    def webpagelinkhovered(self, url):
        pass

    def webpageunsupportedcontent(self, url):
        pass

    def webviewtitlechanged(self, title):
        self.setWindowTitle('Interneto puslapis:' + title)

    def webviewstatusbarmessage(self, txt):
        pass

    def webviewlinkclicked(self, url):
        pass

    def loadpdfcomboboxes(self):
        for item in self.combolist:
            shop = item[0]
            pdfsinshopsdir = sorted(os.listdir(userdir + userprogpath + SEP('pdfs/') + shop + SEP('/')), key=lambda p: os.path.getctime(os.path.join(userdir + userprogpath + SEP('pdfs/') + shop + SEP('/'), p)))
            pdfss = []
            for pdf in pdfsinshopsdir:
                if not pdf.startswith('dir_'):
                    pdfss.append(pdf)
            item[1].clear()
            item[1].addItem(shop)
            item[1].addItems(pdfss)

    def createhtmlfrompdf(self):
        self.comboboxesenabledisable('disable')
        b = pdf2images.imagesFromPdf(self.pdftoimagesdpi)
        self.threads.append(b)
        self.threads[len(self.threads)-1].txt.connect(self.addtxt)
        self.threads[len(self.threads)-1].reloadcomboboxes.connect(self.loadpdfcomboboxes)
        self.threads[len(self.threads)-1].reloadcomboboxes.connect(self.downlopdedpdfsfalse)
        b.start()

    def downlopdedpdfsfalse(self):
        self.downlopdedpdfs = False
        self.comboboxesenabledisable('enable')
        
    def loadurlfromlineedit(self):
        url = str(self.lineEdit.displayText())
        if url.startswith('http://'):
            self.webView.load(QtCore.QUrl(url))
        elif url.startswith('https://'):
            self.webView.load(QtCore.QUrl(url))
        elif url.startswith('data:'):
            self.webView.load(QtCore.QUrl(url))
        elif url.startswith('ftp://'):
            self.webView.load(QtCore.QUrl(url))
        elif url.startswith('www.'):
            self.webView.load(QtCore.QUrl('http://' + url))
        elif url.startswith('/'):
            self.webView.load(QtCore.QUrl(url))
        elif url.startswith('c:'):
            self.webView.load(QtCore.QUrl(url))
        else:
            self.webView.load(QtCore.QUrl('http://www.' + url))
        
    def comboboxlasthighlighted(self, num):
        self.combohighlighted = num
        
    def eventFilter(self, source, event):        
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
        self.setWindowTitle('Internetas: ' + self.comboBox.currentText())
        
    def savebrowserbookmarks(self):
        lst = []
        for n in range(self.comboBox.count()):
            lst.append(('Site title', str(self.comboBox.itemText(n))))
        f = open(userdir + userprogpath + 'browserbookmarks.txt', 'w')
        json.dump(lst, f,  indent=4)
        f.close()

    def addbrowserbookmarks(self):
        try:
            f = open(userdir + userprogpath + 'browserbookmarks.txt', 'r')
            lst = json.load(f)
            for tpl in lst:
                self.comboBox.addItem(tpl[1])
        except:
                pass

    def infobox(self, text):
        box = QtGui.QMessageBox()
        box.setText(unicode(text, "utf-8"))
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
            self.deleteoldpdfs(self.spinBox.value())
        if settings.value("autodelpdfstime").toInt()[1]:
            self.spinBox.setValue(settings.value("autodelpdfstime").toInt()[0])
        if settings.value("pdftoimagesdpi").toInt()[1]:
            self.spinBox_4.setValue(settings.value("pdftoimagesdpi").toInt()[0])
            self.pdftoimagesdpi = settings.value("pdftoimagesdpi").toInt()[0]
        if settings.value("usecsszoom").toBool():
            self.usecsszoom = True
            self.checkBox_5.setChecked(True)
            self.loadcustomcss()
        if settings.value("zoomfactor").toFloat()[1]:
            self.doubleSpinBox.setValue(settings.value("zoomfactor").toFloat()[0])
        for item in self.checkboxlist:
             if settings.value(item.text()).toBool():
                item.setChecked(True)
        if settings.value("currenthtmlpath").toString():
            self.currenthtmlpath = settings.value("currenthtmlpath").toString()
        if settings.value("currentpdfpage").toInt()[1]:
            self.currentpdfpage = settings.value("currentpdfpage").toInt()[0]
        if settings.value("numofpdfpages").toInt()[1]:
            self.numofpdfpages = settings.value("numofpdfpages").toInt()[0]
        
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
        settings.setValue("pdftoimagesdpi", self.spinBox_4.value())
        settings.setValue("usecsszoom", self.checkBox_5.isChecked())
        settings.setValue("zoomfactor", self.doubleSpinBox.value())
        settings.setValue("currenthtmlpath", self.currenthtmlpath)
        settings.setValue("currentpdfpage", self.currentpdfpage)
        settings.setValue("numofpdfpages", self.numofpdfpages)        
        self.savebrowserbookmarks()   
        
    def deleteoldpdfs(self, days):
        self.pushButton_8.setEnabled(False) 
        a = oldpdfdeleter.OldPdfDeleter(days)
        self.threads.append(a)
        self.threads[len(self.threads)-1].TxtInfo.connect(self.addtxt)
        self.threads[len(self.threads)-1].finished.connect(self.loadpdfcomboboxes)
        self.threads[len(self.threads)-1].finished.connect(self.enablepushButton_8)
        a.start()

    def enablepushButton_8(self):
        self.pushButton_8.setEnabled(True)

    def stupidworkaround(self):
        self.plainTextEdit.appendPlainText(unicode('Jei yra trinu senus lankstinukus', "utf-8"))
            
    def checkforprogramupdates(self):
        self.pushButton_7.setEnabled(False)
        self.plainTextEdit.appendPlainText(unicode('Tikrinu ar nėra programos atnaujinimo', "utf-8"))
        b = updater.Updater()
        self.threads.append(b)
        self.threads[len(self.threads)-1].foundupdate.connect(self.addtxt)
        self.threads[len(self.threads)-1].updated.connect(self.addtxt)
        self.threads[len(self.threads)-1].updated.connect(self.enablepushButton_7)
        b.start()

    def enablepushButton_7(self):
        self.pushButton_7.setEnabled(True)

    def nextpage(self):
        if self.currentpdfpage <= self.numofpdfpages - 1:
            self.currentpdfpage = self.currentpdfpage + 1
            if platform.system() == "Windows":
                self.webView_2.load(QtCore.QUrl(self.currenthtmlpath + '#' + str(self.currentpdfpage)))
            else:
                self.webView_2.load(QtCore.QUrl(self.currenthtmlpath + '#' + str(self.currentpdfpage)))
        
    def previouspage(self):
        if self.currentpdfpage >= 2:
            self.currentpdfpage = self.currentpdfpage - 1
            if platform.system() == "Windows":
                self.webView_2.load(QtCore.QUrl(self.currenthtmlpath + '#' + str(self.currentpdfpage)))
            else:
                self.webView_2.load(QtCore.QUrl(self.currenthtmlpath + str("#") + str(self.currentpdfpage)))

    def getnumofpdfpages(self, htmlpath):
        try:
            f = open(htmlpath, 'r')
            txt = f.readlines()
            f.close()
        except:
            txt = 'aaa \n bbb'
        for line in txt:
            if line.find('frame" id="') != -1:
                self.numofpdfpages = int(line.split('id="')[1].split('"')[0])

    def loadpdf(self, combobox):
        index = combobox.currentIndex()
        if index != 0:
            if self.loadpdfjs:
                pdf = userdir + userprogpath + SEP('pdfs/') + combobox.itemText(0) + SEP('/') + combobox.itemText(index)
                if os.path.exists(userdir + userprogpath + SEP('web/pdftoload.pdf')):
                    os.remove(userdir + userprogpath + SEP('web/pdftoload.pdf'))
                if platform.system() == "Windows":
                    if platform.release() == 'XP':
                        pass
                    else:
                        win32file.CreateHardLink(str(userdir + userprogpath + SEP('web/pdftoload.pdf')), str(pdf))
                        self.webView_2.load(QtCore.QUrl(userdir + userprogpath + SEP('web/viewer.html?file=pdftoload.pdf')))
                else:
                    os.link(pdf, userdir + userprogpath + SEP('web/pdftoload.pdf'))
                    self.webView_2.load(QtCore.QUrl(userdir + userprogpath + SEP('web/viewer.html?file=pdftoload.pdf')))
            else:
                html = userdir + userprogpath + SEP('pdfs/') + combobox.itemText(0) + SEP('/dir_') + combobox.itemText(index) + SEP('/index.html')
                self.getnumofpdfpages(html)
                self.currenthtmlpath = html
                self.currentpdfpage = 1
                if os.path.exists(userdir + userprogpath + SEP('web/htmltoload.html')):
                    os.remove(userdir + userprogpath + SEP('web/htmltoload.html'))
                if platform.system() == "Windows":
                    if platform.release() == 'XP':
                        self.webView_2.load(QtCore.QUrl(html))
                    else:
#                        win32file.CreateHardLink(str(userdir + userprogpath + SEP('web/htmltoload.html')), str(html))
                        self.webView_2.load(QtCore.QUrl(html))
                else:
#                    os.link(html, userdir + userprogpath + SEP('web/htmltoload.html'))
                    self.webView_2.load(QtCore.QUrl(html))
        for item in self.combolist:
            shop = item[0]
            if shop != combobox.itemText(combobox.currentIndex()):
                item[1].setCurrentIndex(0)
        self.setWindowTitle('Lankstinukas ' + combobox.itemText(0) + ': ' + combobox.itemText(index))
             
    def updatepdfs(self):
        self.pushButtondownloadpdf.setEnabled(False)
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
               self.setWindowTitle('Internetas: ' + item[0])
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
                if not os.path.exists(userdir + userprogpath + SEP('pdfs/') + self.shop + SEP('/') + os.path.basename(self.url).split('?utm_source')[0]):
                    self.downloader.load(QtCore.QUrl(self.url))
                    self.addtxt('Radau ' + self.shop + ' atnaujinimą')
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
        f = open(userdir + userprogpath + SEP('pdfs/') + self.shop + SEP('/') + os.path.basename(self.url).split('?utm_source')[0], 'wb')
        f.write(dl.readAll())
        f.flush()
        f.close()
        self.downloading = False
        self.downloadpdfs()
        if len(self.downloadlist) == 0:
            self.downlopdedpdfs = True
            self.checkforpdfupdates = False
            if not self.loadpdfjs:
                self.createhtmlfrompdf()
 
class Hub(QtCore.QObject):
 
    def __init__(self):
        super(Hub, self).__init__()
 
 
    @Slot(str)
    def connect(self, config):
        self.on_client_event.emit(config)
 
    @Slot(str)
    def disconnect(self, config):
        pass
 
    on_client_event = Signal(str)
    on_actor_event = Signal(str)
    on_connect = Signal(str)
    on_disconnect = Signal(str)
