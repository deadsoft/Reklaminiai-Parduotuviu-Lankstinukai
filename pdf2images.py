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

def SEP(path):
    separator = os.path.sep
    if separator != '/':
        path = path.replace('/', os.path.sep)
    return path

version = 0.001

import os, time, platform, shutil
from PyQt4 import QtCore, QtGui
if platform.system() == "Linux":
	import popplerqt4
elif platform.system() == "Windows":
	import subprocess

userdir = os.path.expanduser('~')
userprogpath = SEP('/.cache/deadprogram/')
    
class imagesFromPdf(QtCore.QThread):
    txt = QtCore.pyqtSignal(str)
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
</style>\n'''
        self.htmlfp2 =  '<script src="' + userdir + userprogpath + 'jquery/jquery-1.9.1.min.js"></script>' + '''
<script type="text/javascript">
$(document).ready(function () {
$('#gallery img').mouseover(function() {
   my_hub.connect(this.id);
});
});
</script>        
</head>
<body>
    <div id="gallery">\n'''
        self.htmlfp += self.htmlfp2
        self.htmlsp = '''    </div>
</body>
</html>
'''
    def __del__(self):
        self.wait()
        
    def run(self):
        time.sleep(0.5)
        found = False
        self.txt.emit('Tikrinu ar nebuvo atsiųsta lankstinukų')
        self.txt.emit('Išjungiau lanktinukų pasirinkimą kol apdirbu. Tiesiog palauk kažkiek, jei reikia.')
        path = userdir + userprogpath + 'pdfs'
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                pass
            for filename in filenames:
                if os.path.exists(dirname + SEP('/dir_') + filename):
                    if len(os.listdir(dirname + SEP('/dir_') + filename)) <= 1 or os.path.getsize(dirname + SEP('/dir_') + filename + SEP('/index.html')) == 0:
                        self.txt.emit('Radau neapdirbtų lankstinukų. Programos spraga arba buvo nutraukta...')
                        shutil.rmtree(dirname + SEP('/dir_') + filename)
                if platform.system() == 'Linux':
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
                        idnum = 1
                        for pagenum in range(numpages):
                            page = doc.page(pagenum)
                            image = page.renderToImage(self.dpi, self.dpi)
                            pixmap = QtGui.QPixmap.fromImage(image)
                            pixmap.save(dirname + SEP('/dir_') + filename + SEP('/doc') + str(pagenum + 1) + '.jpg', format='JPG', quality = 80)
                            htmlfp += '<img src="' + dirname + SEP('/dir_') + filename + SEP('/doc') + str(pagenum + 1) + '.jpg"' + ' border="0" alt="" class="img-frame" id="' + str(idnum) + '" > \n'
                            idnum += 1
                        htmlfp += htmlsp
                        html.write(htmlfp)
                        html.close()
                        self.txt.emit('Sukuriau paveikslėlius iš atnaujintų lankstinukų: ' + filename)
                        found = True
                elif platform.system() == 'Windows':
                    if not os.path.exists(dirname + SEP('/dir_') + filename) and not os.path.basename(dirname).startswith('dir_'):
                        htmlfp = self.htmlfp
                        htmlsp = self.htmlsp
                        os.mkdir(dirname + SEP('/dir_') + filename)
                        arglist = ['C:\\Program Files\\RPL\\gs\\bin\\gswin32c.exe', "-dBATCH", "-dNOPAUSE", "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-sOutputFile=%s" % dirname + SEP('/dir_') + filename + SEP('/doc%02d.jpg'), "-sDEVICE=jpeg", "-r%s" % str(self.dpi), dirname + SEP('/') + filename]
                        process =  subprocess.Popen(
                        args=arglist,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                        a = process.communicate()[0]
                        process.wait()
                        html = open(dirname + SEP('/dir_') + filename + SEP('/index.html'), 'w')
                        idnum = 1
                        for item in os.listdir(dirname + SEP('/dir_') + filename):
                            if item != 'index.html':
                                htmlfp += '<img src="' + dirname + SEP('/dir_') + filename + SEP('/') + item  + '"' + ' border="0" alt="" class="img-frame" id="' + str(idnum) + '" > \n'
                                idnum += 1
                        htmlfp += htmlsp
                        html.write(htmlfp)
                        html.close()
                        self.txt.emit('Sukuriau paveikslėlius iš atnaujintų lankstinukų: ' + filename)
                        found = True
        if not found:
            self.txt.emit('Neradau naujų lankstinukų')
        self.reloadcomboboxes.emit()
        return
