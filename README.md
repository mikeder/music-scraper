Python Music Scraper
======

* Python script to scrape YouTube and Soundcloud links from electronic music subreddits from http://www.reddit.com.

* It currently only handles YouTube links for download and convertions via pafy and pydub.

* Required libraries :  httplib2, time, pafy, re, sys, os, ps4, pydub


## Installation

    $ git clone https://github.com/sqweebking/music-scraper.git
    

For ubuntu / debian, you need python-pip

    $ apt-get install python-pip

for soundcloud downloading, you'll need to get ID3

    $ wget 'http://ftp.de.debian.org/debian/pool/main/p/python-id3/python-id3_1.2.orig.tar.gz'
    $ tar -zxvf python-id3_1.2.orig.tar.gz
    $ cd python-id3-1.2.orig
    $ python setup.py install
    
## download from soundcloud

example:


    $ cd downloader
    $ python scDL.py https://soundcloud.com/iguanodon/witchcraft-valley



## Todo: 

* Add config file functionality for in/out dir, export format and MySql(download counts, time to dl, etc.)

* Describe args
