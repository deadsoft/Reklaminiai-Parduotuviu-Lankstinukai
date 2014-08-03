# -*- coding: utf-8 -*-
"""
	ReklaminiaiParduotuviųLankstinukai
	Copyright (C) <2011-2014> <Algirdas Butkus> <butkus.algirdas@gmail.com>

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
version = 0.002

from PyQt4 import QtCore
import time

class LinkParser(QtCore.QThread):
    addtext = QtCore.pyqtSignal(str)
    url = QtCore.pyqtSignal(str, str)
    finishedurlparsing = QtCore.pyqtSignal(bool)
    def __init__(self, queue_list):
        QtCore.QThread.__init__(self)
        self.queue_list = queue_list
        self.download_queue = []
        from BeautifulSoup import BeautifulSoup
        import urllib2
        self.urlib = urllib2
        self.bsoup = BeautifulSoup
        self.threads = []

    def __del__(self):
        self.wait()

    def run(self):
        time.sleep(1.5)
        for label in self.queue_list:
            exec 'self.' + label + '(label)'
        for item in self.download_queue:
            self.url.emit(item[0], item[1])
        self.finishedurlparsing.emit(True)
        return
        
    def Maxima(self, label):
        try:
            pages = []
            html_page = self.urlib.urlopen('http://www.maxima.lt/akcijos/')
            soup = self.bsoup(html_page)
            for link in soup.findAll(attrs={'class': 'mainSubmenuLink'}):
                if 'http://www.maxima.lt/akcijos/maxima-kaininis' in link['href']:
                    pages.append(link['href'])
            for link in pages:
                html_page = self.urlib.urlopen(link)
                soup = self.bsoup(html_page)
                for link in soup.findAll('a', href=True):
                    if str(link['href']).endswith('pdf'):
                        if not str(link['href']).endswith('Nr18-s.pdf'):
                            self.download_queue.append((label, link['href']))
            self.addtext.emit('Tikrinu ar Maxima turi atnaujinimų')
        except:
            pass

    def Rimi(self, label):
        try:
            html_page = self.urlib.urlopen('http://www.rimi.lt/rimi-pasiulymai/rimi-leidiniai')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'item'})
            for link in search:
                html_page = self.urlib.urlopen('http://www.rimi.lt' + link.find('a')['href'])
                soup = self.bsoup(html_page)
                search2 = soup.findAll(attrs={'class': 'pdf'})
                self.download_queue.append((label,  'http://www.rimi.lt' + search2[0].find('a')['href']))
            elf.addtext.emit('Tikrinu ar Rimi turi atnaujinimų')
        except:
            pass

    def Norfa(self, label):
        try:
            html_page = self.urlib.urlopen('http://www.norfa.lt/lt/leidiniai')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'downloadPdf'})
            for link in search:
                self.download_queue.append((label, link.find('a')['href']))
                self.addtext.emit('Tikrinu ar Norfa turi atnaujinimų')
        except:
            pass

    def Iki(self, label):
        try:
            html_page = self.urlib.urlopen('http://www.iki.lt/lt.php/akcijos/kainu_leidinys')
            soup = self.bsoup(html_page)
            search = soup.findAll('div', attrs={'class': 'nomargin'})
            self.download_queue.append((label, 'http://www.iki.lt/' + str(search[1].a).split('href="')[1].split('"')[0]))
            
            html_page = self.urlib.urlopen('http://iki.lt/lt.php/akcijos/savaitele-plius')
            soup = self.bsoup(html_page)
            search = soup.findAll('div', attrs={'class': 'nomargin'})
            self.download_queue.append((label, 'http://www.iki.lt/' + str(search[1].a).split('href="')[1].split('"')[0]))
            self.addtext.emit('Tikrinu ar Iki turi atnaujinimų')
        except:
            pass

    def Cento(self, label):
        try:
            html_page = self.urlib.urlopen('http://www.cento.lt/view.php?id=13')
            soup = self.bsoup(html_page)
            search = soup.findAll('a', attrs={'class': 'deftxt'})
            for link in search:
                if str(link).split('href="')[1].split('"')[0].endswith('.pdf'):
                    self.download_queue.append((label, 'http://www.cento.lt/' + str(link).split('href="')[1].split('"')[0]))
        except:
            pass

    def Jysk(self, label):
        try:
            pages = []
            html_page = self.urlib.urlopen('http://jysk.lt/?l=2')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'catalogue'})  
            for link in search:
                pages.append(('http://jysk.lt/' + link.find('a')['href']))
            for link in pages:
                html_page = self.urlib.urlopen(link)
                soup = self.bsoup(html_page)
            for link in soup.findAll(attrs={'class': 'd_pdf'}):
                self.download_queue.append((label, 'http://jysk.lt/' +  link['href']))
        except:
            pass

    def Supernetto(self, label):
        try:
            html_page = self.urlib.urlopen('http://www.supernetto.lt/')
            soup = self.bsoup(html_page)
            search = soup.findAll('li', attrs={'class': 'first'})
            for link in search[1:]:
                self.download_queue.append((label, 'http://www.supernetto.lt' + str(link).split('href="')[1].split('"')[0]))
        except:
            pass

