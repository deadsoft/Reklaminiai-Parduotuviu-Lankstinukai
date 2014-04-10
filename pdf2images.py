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

import os, time
from PyQt4 import QtCore, QtGui
import popplerqt4

userdir = os.path.expanduser('~')

class imagesFromPdf(QtCore.QThread):
    FinishedExtractingImages = QtCore.pyqtSignal(str)
    reloadcomboboxes = QtCore.pyqtSignal()
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.htmlfp = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title> </title>
<style media="screen" type="text/css">
.img-frame {
    background:#303030;
    padding:8px;
    width:98%;
}
    
html {
    background:#3c3c3c;
    width:100%;
}
body {
    background:#3c3c3c;
    width:99%;
}
</style>
</head>

<body>
    <div id="myGallery">\n'''
        self.htmlsp = '''    </div>
</body>
</html>
'''
    def __del__(self):
        self.wait()
        
    def run(self):
        time.sleep(0.5)
        self.FinishedExtractingImages.emit('Tikrinu ar neatsiųsta lankstinukų atnaujinimų')
        path = userdir + '/.cache/deadprogram/pdfs'
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                pass
            for filename in filenames:
                if not os.path.exists(dirname + '/dir_' + filename) and not os.path.basename(dirname).startswith('dir_'):
                    os.mkdir(dirname + '/dir_' + filename)
                    htmlfp = self.htmlfp
                    htmlsp = self.htmlsp
                    html = open(dirname + '/dir_' + filename + '/index.html', 'w')
                    doc = popplerqt4.Poppler.Document.load(dirname + '/' + filename)
                    doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
                    doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)
                    numpages = doc.numPages()
                    page = doc.page(0)
                    for pagenum in range(numpages):
                        page = doc.page(pagenum)
                        image = page.renderToImage(150, 150)
                        pixmap = QtGui.QPixmap.fromImage(image)
                        pixmap.save(dirname + '/dir_' + filename + '/' + 'doc' + str(pagenum + 1) + '.png')
                        htmlfp += '<img src="file://' + dirname + '/dir_' + filename + '/' + 'doc' + str(pagenum + 1) + '.png"' + ' border="0" alt="" class="img-frame"> \n'
                    htmlfp += htmlsp
                    html.write(htmlfp)
                    html.close()
                    self.FinishedExtractingImages.emit('Sukuriau paveikslėlius iš atnaujintų lankstinukų: ' + filename)
        self.FinishedExtractingImages.emit('Baigtas lankstinukų atnaujinimų tikrinimas')
        self.reloadcomboboxes.emit()
        return

