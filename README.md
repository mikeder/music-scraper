Reddit Music Scraper v1.2
======

* Scrapes YouTube links from http://www.reddit.com/r/<subreddit>

* Store links, and song info(title, size) and date into a SQLite database

* Best available audio is then downloaded and converted to mp3(192k) via pydub

* Required libraries :  requests, pafy, pydub


## Installation

** This install process has been updated for use with Python 3 **

If you dont have avconv or ffmpeg installed:

    $ sudo apt-get install libav-tools

For ubuntu / debian, you need python-pip

    $ sudo apt-get install python3-pip
    $ sudo pip3 install pafy pydub requests

Clone this repo

    $ git clone --recursive https://github.com/mikeder/music-scraper.git

    * The --recursive flag is needed to also clone the ReddiWrap submodule


## Config file:

* ~/.rsdc is generated on first run, edit it to fit your system
* Paths should always include the trailing '/'
* Max file size is in MB

## Usage:

    $ python rsdc.py <subreddit>
    $ python rsdc.py liquiddnb
    $ python rsdc.py trance+electro
    
You can specify multiple subreddits for scraping at the same time by seperating
them with a '+' (new files aren't yet seperated into appropriate folders when 
scraped this way)

## Changelog:
v1.2:
* Improvements:
  * SQLite Database added (link tracking, datetime, size, title)
  * /data/scraped.db

v1.1.2:
* Improvements:
  * Made Album MP3 tag == /r/subreddit

v1.1.1:
* Bug fixes:
  * Updated submodule so that ReddiWrap.py can find Web.py after a fresh clone.

v1.1.0:
* Bug fixes:
  * Artist no longer includes /subreddit in mp3 tag.
  * Script no longer fails on first run if config doesn't exist.
  * Use of Reddit API eliminates issue with hitting request limit.

* Improvements:
  * Implemented ReddiWrap (Reddit API wrapper).
  * https://github.com/derv82/reddiwrap/
  * Removed unused variables and cleaned up functions.
  * BeautifulSoup no longer a dependency.

## Todo: 

* Done for now, ill add to this when I think of new ideas.
