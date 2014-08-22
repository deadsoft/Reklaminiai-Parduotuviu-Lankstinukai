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

version = 0.006

import os, time, platform, shutil
from PyQt4 import QtCore, QtGui
if platform.system() == "Linux":
	import popplerqt4
elif platform.system() == "Windows":
	import subprocess

userdir = os.path.expanduser('~')
userprogpath = SEP('/.cache/deadprogram/')
    
class imagesFromPdf2(QtCore.QThread):
    txt = QtCore.pyqtSignal(str)
    reloadcomboboxes = QtCore.pyqtSignal()
    
    def __init__(self, dpi, shop, url):
        QtCore.QThread.__init__(self)
        self.dpi = dpi
        self.shop = shop
        self.url = url
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
    
html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    background:#3c3c3c
}
* {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
}
.scrollable {
    overflow: auto;
    width: 100%;
    height: 100%;
}
</style>\n'''
        self.htmlfp2 =  '<script src="' + userdir + userprogpath + 'jquery/jquery-1.9.1.min.js"></script>\n' + '<script src="' + userdir + userprogpath + 'jquery/jquery.scrollview.js"></script>\n' + '''
<script type="text/javascript">
$(document).ready(function () {
$('#gallery img').mouseover(function() {
   my_hub.connect(this.id);
});
});
</script>
<script type="text/javascript">''' + '''$(document).ready(function(){$("#gallery").scrollview({grab:"''' + userdir + userprogpath + '''jquery/openhand_8_8.cur", grabbing:"''' + userdir + userprogpath + '''jquery/closedhand_8_8.cur"});});''' +  '''
        </script>      
</head>
<body>
    <div class="scrollable"  id="gallery">\n'''
        self.htmlfp += self.htmlfp2
        self.htmlsp = '''    </div>
</body>
</html>
'''
    def __del__(self):
        self.wait()
        
    def run(self):
        path = userdir + userprogpath + SEP('pdfs/') + self.shop
        if os.path.exists(path + SEP('/dir_') + self.url):
            if len(os.listdir(path + SEP('/dir_') + self.url)) <= 1 or os.path.getsize(path + SEP('/dir_') + self.url + SEP('/index.html')) == 0:
                shutil.rmtree(path + SEP('/dir_') + self.url)
        if not os.path.exists(path + SEP('/dir_') + self.url) and not os.path.basename(path).startswith('dir_'):
            os.mkdir(path + SEP('/dir_') + self.url)
            if not os.path.exists(path + SEP('/dir_') + self.url + '/working'):
                working = open(path + SEP('/dir_') + self.url + SEP('/working'), 'w')
                working.close()            
            if platform.system() == 'Linux':
                htmlfp = self.htmlfp
                htmlsp = self.htmlsp
                html = open(path + SEP('/dir_') + self.url + SEP('/index.html'), 'w')
                doc = popplerqt4.Poppler.Document.load(path + SEP('/') + self.url)
                doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
                doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)
                numpages = doc.numPages()
                page = doc.page(0)
                idnum = 1
                for pagenum in range(numpages):
                    page = doc.page(pagenum)
                    image = page.renderToImage(self.dpi, self.dpi)
                    pixmap = QtGui.QPixmap.fromImage(image)
                    pixmap.save(path + SEP('/dir_') + self.url + SEP('/doc') + str(pagenum + 1) + '.jpg', format='JPG', quality = 80)
                    htmlfp += '<img src="' + path + SEP('/dir_') + self.url + SEP('/doc') + str(pagenum + 1) + '.jpg"' + ' border="0" alt="" class="img-frame" id="' + str(idnum) + '" > \n'
                    idnum += 1
                htmlfp += htmlsp
                html.write(htmlfp)
                html.close()
                self.txt.emit('Sukuriau paveikslėlius iš lankstinuko ' + self.shop + ': ' + self.url)
                self.reloadcomboboxes.emit()
            elif platform.system() == 'Windows':
                htmlfp = self.htmlfp
                htmlsp = self.htmlsp
                html = open(path + SEP('/dir_') + self.url + SEP('/index.html'), 'w')
                arglist = ['C:\\Program Files\\RPL\\gs\\bin\\gs.exe', "-dNumRenderingThreads=2", "-dBATCH", "-dNOPAUSE", "-dSAFER", "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-sDEVICE=jpeg", "-dJPEGQ=90", "-sOutputFile=%s" % path + SEP('/dir_') + self.url + SEP('/doc%02d.jpg'), "-r%s" % str(self.dpi), path + SEP('/') + self.url]
                process = subprocess.Popen(args=arglist, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                a = process.communicate()[0]
                process.wait()
                idnum = 1
                for item in os.listdir(path + SEP('/dir_') + self.url):
                    if item != 'index.html' and item != 'working':
                        htmlfp += '<img src="' + path + SEP('/dir_') + self.url + SEP('/') + item  + '"' + ' border="0" alt="" class="img-frame" id="' + str(idnum) + '" > \n'
                        idnum += 1
                htmlfp += htmlsp
                html.write(htmlfp)
                html.close()
                self.txt.emit('Sukuriau paveikslėlius iš lankstinuko ' + self.shop + ': ' + self.url)
                self.reloadcomboboxes.emit()
        try:
            os.remove(path + SEP('/dir_') + self.url + SEP('/working'))
        except:
            pass
