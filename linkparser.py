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
version = 0.008

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
            self.addtext.emit('Tikrinu ar Maxima turi atnaujinimų')
            pages = []
            html_page = self.urlib.urlopen('http://www.maxima.lt/akcijos/')
            soup = self.bsoup(html_page)
            for link in soup.findAll(attrs={'class': 'mainSubmenuLink'}):
                if 'http://www.maxima.lt/akcijos/maxima-kaininis' in link['href'] or 'http://www.maxima.lt/akcijos/maxima-leidinys' in link['href']:
                    pages.append(link['href'])
            for link in pages:
                html_page = self.urlib.urlopen(link)
                soup = self.bsoup(html_page)
                for link in soup.findAll('a', href=True):
                    if str(link['href']).endswith('pdf'):
                        if not str(link['href']).endswith('Nr18-s.pdf'):
                            self.download_queue.append((label, link['href']))
        except:
            pass

    def Norfa(self, label):
        try:
            self.addtext.emit('Tikrinu ar Norfa turi atnaujinimų')
            pages = []
            html_page = self.urlib.urlopen('http://www.norfa.lt/lt/leidiniai')
            soup = self.bsoup(html_page)
            search = soup.find(attrs={'class': 'thirdMenu'}).findAll("a")
            for link in search:
                self.pages.append(link.get("href"))
            for link in pages:
                html_page = self.urlib.urlopen(link)
                soup = self.bsoup(html_page)
                search = soup.findAll(attrs={'class': 'downloadPdf'})
                for link in search:
                    self.download_queue.append((label, link.find('a')['href']))
                    
        except:
            pass

    def Iki(self, label):
        try:
            self.addtext.emit('Tikrinu ar Iki turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.iki.lt/lt.php/akcijos/kainu_leidinys')
            soup = self.bsoup(html_page)
            search = soup.findAll('div', attrs={'class': 'nomargin'})
            self.download_queue.append((label, 'http://www.iki.lt/' + str(search[1].a).split('href="')[1].split('"')[0]))
            
            html_page = self.urlib.urlopen('http://iki.lt/lt.php/akcijos/savaitele-plius')
            soup = self.bsoup(html_page)
            search = soup.findAll('div', attrs={'class': 'nomargin'})
            self.download_queue.append((label, 'http://www.iki.lt/' + str(search[1].a).split('href="')[1].split('"')[0]))

        except:
            pass


    def Rimi(self, label):
        try:
            self.addtext.emit('Tikrinu ar Rimi turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.rimi.lt/rimi-pasiulymai/rimi-leidiniai')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'item'})
            for link in search:
                html_page = self.urlib.urlopen('http://www.rimi.lt' + link.find('a')['href'])
                soup = self.bsoup(html_page)
                search2 = soup.findAll(attrs={'class': 'pdf'})
                self.download_queue.append((label,  'http://www.rimi.lt' + search2[0].find('a')['href']))
        except:
            pass

            
    def Senukai(self, label):
        try:
            self.addtext.emit('Tikrinu ar Senukai turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.senukai.lt/index.php?&cl=newspapers_list')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'pdf'})
            for link in search:
                self.download_queue.append((label,  link['href']))
        except:
            pass


    def Aibe(self, label):
        try:
            self.addtext.emit('Tikrinu ar Aibė turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.aibe.lt/lt/akcijos/aibe-leidiniai')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'pdf'})
            for link in search:
                self.download_queue.append((label,  'http://www.aibe.lt/' + link['href']))
        except:
            pass


    def FRESH_MARKET(self, label):
        try:
            self.addtext.emit('Tikrinu ar FRESH MARKET turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.freshmarket.lt/akcijos')
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'get-pdf'})
            for link in search:
                self.download_queue.append((label,  'http://www.freshmarket.lt/' + link['href']))
        except:
            pass

    def Moki_Vezi(self, label):
        try:
            self.addtext.emit('Tikrinu ar Moki Veži turi atnaujinimų')
            html_page = self.urlib.urlopen('http://mokivezi.lt/leidiniai/')
            soup = self.bsoup(html_page)
            search = soup.find(attrs={'class': 'leidinys_block'}).find("a")['href']
            self.download_queue.append((label,  search))
        except:
            pass
