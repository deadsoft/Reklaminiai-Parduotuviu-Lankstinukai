#!/bin/sh

#Run as root user. sudo ./install.sh, or su -c "./install.sh".

curdir=$(dirname $0)
if [ ! -d "/usr/lib/deadprogram" ]; then
mkdir "/usr/lib/deadprogram"
fi
if [ ! -d "/usr/share/deadprogram" ]; then
mkdir "/usr/share/deadprogram"
fi

cd $curdir

cp -f BeautifulSoup.py linkparser.py pdf2images.py oldpdfdeleter.py deadprogram.py updater.py main.py /usr/lib/deadprogram
cp -f DeadProgram.desktop /usr/share/applications
cp -fr web build icons /usr/share/deadprogram
