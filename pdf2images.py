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

def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path

version = 0.001

import os, time
from PyQt4 import QtCore, QtGui
import popplerqt4

userdir = os.path.expanduser('~')
userprogpath = SEP('/.cache/deadprogram/')

class imagesFromPdf(QtCore.QThread):
    FinishedExtractingImages = QtCore.pyqtSignal(str)
    reloadcomboboxes = QtCore.pyqtSignal()
    
    def __init__(self, dpi):
        QtCore.QThread.__init__(self)
        self.dpi = dpi
        self.htmlfp = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title> </title>
<style media="screen" type="text/css">
.img-frame {
    background:#303030;
    padding:8px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
    
html {
    background:#3c3c3c; 
}
</style>
</head>
<body>
    <div id="gallery">\n'''
        self.htmlsp = '''    </div>
</body>
</html>
'''
    def __del__(self):
        self.wait()
        
    def run(self):
        time.sleep(0.5)
        self.FinishedExtractingImages.emit('Tikrinu ar nebuvo atsiųsta lankstinukų')
        path = userdir + userprogpath + 'pdfs'
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                pass
            for filename in filenames:
                if not os.path.exists(dirname + SEP('/dir_') + filename) and not os.path.basename(dirname).startswith('dir_'):
                    os.mkdir(dirname + SEP('/dir_') + filename)
                    htmlfp = self.htmlfp
                    htmlsp = self.htmlsp
                    html = open(dirname + SEP('/dir_') + filename + SEP('/index.html'), 'w')
                    doc = popplerqt4.Poppler.Document.load(dirname + SEP('/') + filename)
                    doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
                    doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)
                    numpages = doc.numPages()
                    page = doc.page(0)
                    for pagenum in range(numpages):
                        page = doc.page(pagenum)
                        image = page.renderToImage(self.dpi, self.dpi)
                        pixmap = QtGui.QPixmap.fromImage(image)
                        pixmap.save(dirname + SEP('/dir_') + filename + SEP('/doc') + str(pagenum + 1) + '.jpg', format='JPG', quality = 100)
                        htmlfp += '<img src="file://' + dirname + SEP('/dir_') + filename + SEP('/doc') + str(pagenum + 1) + '.jpg"' + ' border="0" alt="" class="img-frame"> \n'
                    htmlfp += htmlsp
                    html.write(htmlfp)
                    html.close()
                    self.FinishedExtractingImages.emit('Sukuriau paveikslėlius iš atnaujintų lankstinukų: ' + filename)
        self.FinishedExtractingImages.emit('Neradau naujų lankstinukų')
        self.reloadcomboboxes.emit()
        return

