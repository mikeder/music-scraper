Python Music Scraper
======

* Scrapes YouTube links from http://www.reddit.com/r/ specified subreddit

* Best available audio is then downloaded and converted to mp3 via pydub

* Required libraries :  requests, BeautifulSoup4, pafy, pydub


## Installation

** This install process has been updated for use with Python 3 **

If you dont have avconv or ffmpeg installed:

    $ sudo apt-get install libav-tools

For ubuntu / debian, you need python-pip

    $ sudo apt-get install python3-pip
    $ sudo pip3 install BeautifulSoup4 pafy pydub requests

Clone this repo

    $ git clone https://github.com/sqweebking/music-scraper.git

    


## Config file:

* ~/.rsdc is generated on first run, edit it to fit your system
* Paths should always include the trailing '/'
* Max file size is in MB

## Usage:

    $ python scrape.py <subreddit>
    $ python scrape.py liquiddnb
    $ python scrape.py trance+electro
    
You can specify multiple subreddits for scraping at the same time by seperating them with a '+'

All files will be saved to /path/to/inDIR/subfolder and /path/to/outDIR/subfolder respectively    

## Todo: 

* Add possibility to enable MySQL logging of # of files per scrape, locations, genre, etc.
