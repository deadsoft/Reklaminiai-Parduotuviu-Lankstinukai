# -*- coding: utf-8 -*-
"""
	ReklaminiaiParduotuviųLankstinukai
	Copyright (C) <2011-2015> <Algirdas Butkus> <butkus.algirdas@gmail.com>

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
version = 0.017

from PyQt4 import QtCore

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
        for label in self.queue_list:
            exec 'self.' + label + '(label)'
        for item in self.download_queue:
            self.url.emit(item[0], item[1])
        self.finishedurlparsing.emit(True)
        self.addtext.emit('Baigiau tikrinti parduotuves')
        return
        
    def Maxima(self, label):
        try:
            self.addtext.emit('Tikrinu ar Maxima turi atnaujinimų')
            pages = []
            html_page = self.urlib.urlopen('http://www.maxima.lt/leidiniai/', timeout = 5)
            soup = self.bsoup(html_page)
            for link in soup.findAll(attrs={'class': 'btn red '}):
                self.download_queue.append((label, 'http://www.maxima.lt' + link['data-url']))
            for link in soup.find(attrs={'class': 'in'}).findAll("a"):
                self.download_queue.append((label, 'http://www.maxima.lt' + link['data-url']))
            for link in soup.findAll(attrs={'class': 'swiper-slide'}):
                self.download_queue.append((label, 'http://www.maxima.lt' + link.find('div')['data-url']))
                
        except:
            pass

    def Norfa(self, label):
        try:
            self.addtext.emit('Tikrinu ar Norfa turi atnaujinimų')
            pages = []
            html_page = self.urlib.urlopen('http://www.norfa.lt/lt/leidiniai', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.find(attrs={'class': 'thirdMenu'}).findAll("a")
            for link in search:
                pages.append(link.get("href"))
            for link in pages:
                html_page = self.urlib.urlopen(link, timeout = 5)
                soup = self.bsoup(html_page)
                search = soup.findAll(attrs={'class': 'downloadPdf'})
                for link in search:
                    self.download_queue.append((label, link.find('a')['href']))
                    
        except:
            pass

    def Iki(self, label):
        try:
            self.addtext.emit('Tikrinu ar Iki turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.iki.lt/lt.php/akcijos/kainu_leidinys', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll('div', attrs={'class': 'nomargin'})
            self.download_queue.append((label, 'http://www.iki.lt/' + str(search[1].a).split('href="')[1].split('"')[0]))
            
            html_page = self.urlib.urlopen('http://iki.lt/lt.php/akcijos/savaitele-plius', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll('div', attrs={'class': 'nomargin'})
            self.download_queue.append((label, 'http://www.iki.lt/' + str(search[1].a).split('href="')[1].split('"')[0]))

        except:
            pass

    def Rimi(self, label):
        try:
            self.addtext.emit('Tikrinu ar Rimi turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.rimi.lt/rimi-pasiulymai/rimi-leidiniai', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'item'})
            for link in search:
                html_page = self.urlib.urlopen('http://www.rimi.lt' + link.find('a')['href'], timeout = 5)
                soup = self.bsoup(html_page)
                search2 = soup.findAll(attrs={'class': 'pdf'})
                self.download_queue.append((label,  'http://www.rimi.lt' + search2[0].find('a')['href']))
        except:
            pass

    def Aibe(self, label):
        try:
            self.addtext.emit('Tikrinu ar Aibė turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.aibe.lt/lt/akcijos/aibe-leidiniai', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'pdf'})
            for link in search:
                self.download_queue.append((label,  'http://www.aibe.lt/' + link['href']))
        except:
            pass

    def FRESH_MARKET(self, label):
        try:
            self.addtext.emit('Tikrinu ar FRESH MARKET turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.freshmarket.lt/akcijos', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'get-pdf'})
            for link in search:
                self.download_queue.append((label,  'http://www.freshmarket.lt/' + link['href']))
        except:
            pass
            
    def PROMO_CashCarry(self, label):
        try:
            pages = []
            self.addtext.emit('Tikrinu ar PROMO CashCarry turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.cashcarry.lt/', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.find(attrs={'class': 'banner_area clearfix'}).findAll("a")
            for link in search:
                pages.append(link['href'])
            for link in pages:
                html_page = self.urlib.urlopen(link, timeout = 5)
                soup = self.bsoup(html_page)
                search = soup.find(attrs={'class': 'stext clearfix'})
                self.download_queue.append((label,  search.find('a')['href']))
        except:
            pass
            
    def PRISMA(self, label):
        try:
            self.addtext.emit('Tikrinu ar PRISMA turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.prisma.lt/lt/leidiniai/', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'getPDFOffer'})
            for link in search:
                self.download_queue.append((label,  'http://www.prisma.lt' + link.find('a')['href']))
        except:
            pass

    def EUROKOS(self, label):
        try:
            self.addtext.emit('Tikrinu ar EUROKOS turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.eurokos.lt/leidiniai/akciju-leidiniai/', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'leid_parsisiusti'})
            for link in search:
                self.download_queue.append((label,  link.find('a')['href']))
            
        except:
            pass

    def Drogas(self, label):
        try:
            self.addtext.emit('Tikrinu ar Drogas turi atnaujinimų')
            html_page = self.urlib.urlopen('https://www.drogas.lt/lit/laikrastis/', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'content-block'})
            for link in search:
                 self.download_queue.append((label,  'https://www.drogas.lt' + link.find('a')['href']))          
        except:
            pass

    def ERMITAZAS(self, label):
        try:
            self.addtext.emit('ERMITAŽAS kolkas nesiunčiamas')
            try:
                import santaka
                urllist = santaka.run()
                for item in urllist:
                  self.download_queue.append((label,  item))
                  print item  
                
            except:
                pass
        except:
            pass
            
    def Senukai(self, label):
        try:
            self.addtext.emit('Tikrinu ar Senukai turi atnaujinimų')
            html_page = self.urlib.urlopen('http://www.senukai.lt/index.php?&cl=newspapers_list', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.findAll(attrs={'class': 'pdf'})
            for link in search:
                self.download_queue.append((label,  link['href']))
        except:
            pass

    def Moki_Vezi(self, label):
        try:
            self.addtext.emit('Tikrinu ar Moki Veži turi atnaujinimų')
            html_page = self.urlib.urlopen('http://mokivezi.lt/leidiniai/', timeout = 5)
            soup = self.bsoup(html_page)
            search = soup.find(attrs={'class': 'leidinys_block'}).find("a")['href']
            self.download_queue.append((label,  search))
        except:
            pass
