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

version = 0.001

from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from gui import Ui_MainWindow
import urllib, sys, os, json, shutil, time

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
if not os.path.exists(userdir + '/.cache/deadprogram/css/'):
    os.mkdir(userdir + '/.cache/deadprogram/css')
if not os.path.exists(userdir + '/.cache/deadprogram/modules/custom.css'):
    open(userdir + '/.cache/deadprogram/modules/custom.css', 'a').close()
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


class DeadProgram(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
#        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
 #       self.setAutoFillBackground(True)
        
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

        self.tabWidget.currentChanged.connect(self.tabchangedwindowtitle)
        self.checkBox.stateChanged.connect(self.pdfjscheckboxstatechanged)
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
        
        self.lineEdit.insert('about:blank')
        self.lineEdit.setDragEnabled(True)
        self.lineEdit.installEventFilter(self)
        self.comboBox.installEventFilter(self)
        self.comboBox.setAcceptDrops(True)
        self.pushButton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_9.installEventFilter(self)
        self.comboBoxview = self.comboBox.view()
        self.comboBoxview.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        
        settings = self.webView.settings()
        webpage = self.webView.page()
        webpage.unsupportedContent.connect(self.webpageunsupportedcontent)
        webpage.linkHovered.connect(self.webpagelinkhovered)
        webpage.setForwardUnsupportedContent(True)
        webpage.setLinkDelegationPolicy(QtWebKit.QWebPage.DontDelegateLinks)
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
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
        settings.setLocalStoragePath(userdir  + '/.cache/deadprogram/cache')
        settings.setMaximumPagesInCache(20)
        settings.setOfflineStoragePath(userdir  + '/.cache/deadprogram/cache')
        settings.setUserStyleSheetUrl(QtCore.QUrl(userdir  + '/.cache/deadprogram/css/custom.css'))
        
        settings_2 = self.webView_2.settings()
#        settings_2.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
#        settings_2.setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptCanAccessClipboard, True)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavascriptCanCloseWindows, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.JavaEnabled, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, False)
        settings_2.setAttribute(QtWebKit.QWebSettings.DnsPrefetchEnabled, False)
        settings_2.setLocalStoragePath(userdir  + '/.cache/deadprogram/cache')
        settings_2.setMaximumPagesInCache(20)
        settings_2.setOfflineStoragePath(userdir  + '/.cache/deadprogram/cache')
        settings_2.setUserStyleSheetUrl(QtCore.QUrl(userdir  + '/.cache/deadprogram/css/custom.css'))
        
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

    def tabchangedwindowtitle(self, i):
        self.setWindowTitle(self.tabWidget.tabText(i))

    def pdfjscheckboxstatechanged(self, state):
        if state == 2:
            self.loadpdfjs = True
        elif state == 0:
            self.loadpdfjs = False
            self.downlopdedpdfs = True
            self.createhtmlfrompdf()

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
        b = pdf2images.imagesFromPdf(150)
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
        self.setWindowTitle('Internetas: ' + self.comboBox.currentText())
        
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
        self.threads[len(self.threads)-1].finished.connect(self.loadpdfcomboboxes)
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
        self.setWindowTitle('Lankstinukas ' + combobox.itemText(0) + ': ' + combobox.itemText(index))        
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
            if not self.loadpdfjs:
                self.createhtmlfrompdf()
