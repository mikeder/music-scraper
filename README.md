Python Music Scraper
======

* Python script to scrape YouTube and Soundcloud links from electronic music subreddits from http://www.reddit.com.

* It currently only handles YouTube links for download and convertions via pafy and pydub.

* Required libraries :  httplib2, BeautifulSoup4, pafy, pydub, soundcloud


## Installation

If you dont have avconv or ffmpeg installed:

    $ apt-get install libav-tools

For ubuntu / debian, you need python-pip

    $ apt-get install python-pip
    $ pip install BeautifulSoup4 httplib2 pafy pydub soundcloud

Clone this repo

    $ git clone https://github.com/sqweebking/music-scraper.git

    


# Config file:

/usr/local/etc/rsdc.config

    [paths]
    
    HTTP = http://www.reddit.com/r/
    
    inDIR = /home/music/source/in/
    
    outDIR = /home/music/source/out/
    
* Always include the trailing '/' or else things will break.

## Usage:
    $ python scrape.py liquiddnb 1
    
    This will scrape http://www.reddit.com/r/liquiddnb and download audio files to the inDIR, then convert them to .mp3 and put them in the outDIR.
    
For SoundCloud downloading, you'll need to get ID3

    $ wget 'http://ftp.de.debian.org/debian/pool/main/p/python-id3/python-id3_1.2.orig.tar.gz'; echo '33f6ac3987ddc7b7d91cae4b56d6fbc2  python-id3_1.2.orig.tar.gz' | md5sum -c
    # python-id3_1.2.orig.tar.gz: OK
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
