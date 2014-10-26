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

    


## Config file:

* Edit scrape.conf to fit your system
* Paths should always include the trailing '/'
* Max file size is in MB

## Usage:

    $ python scrape.py <subreddit> <subfolder>
    $ python scrape.py liquiddnb 1
    
    This will scrape http://www.reddit.com/r/liquiddnb and download audio files to the /path/to/inDIR/1/, then convert them to .mp3 and put them in /path/to/outDIR/1/
    
    $ python scrape.py trance+electro 2
    
    You can also specify multiple subreddits for scraping at the same time by seperating them with a '+'
    

## Todo: 

* Add possibility to enable MySQL logging of # of files per scrape, locations, genre, etc.
