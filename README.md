Reddit Music Scraper
======

* Scrapes YouTube links from http://www.reddit.com/r/<subreddit>

* Store links, and song info(title, size) and date into a SQLite database

* Best available audio is then downloaded and converted to mp3(320k) via pydub


## Installation

If you dont have avconv or ffmpeg installed:

    # Debian
    $ sudo apt-get install libav-tools
    
    # OSX
    $ brew install ffmpeg

For ubuntu / debian, you need python-pip

    $ sudo apt-get install python3-pip
    $ sudo pip3 install pafy pydub requests

Clone this repo

    $ git clone https://github.com/mikeder/music-scraper.git
    $ cd music-scraper/
    $ pip install .
    


## Config file:

* ~/.rsdc is generated on first run, edit it to fit your system
* Paths should always include the trailing '/'
* Max file size is in MB

## Usage:

Pip installation will provide the `rsdc` console script:

    $ rsdc <subreddit>
    $ rsdc liquiddnb
    $ rsdc trance+electro
    
You can specify multiple subreddits for scraping at the same time by seperating
them with a '+' (new files aren't yet seperated into appropriate folders when 
scraped this way)

## Changelog:
* Improvements:
  * SQLite Database added (link tracking, datetime, size, title)
  * /data/scraped.db

* Improvements:
  * Made Album MP3 tag == /r/subreddit

* Bug fixes:
  * Updated submodule so that ReddiWrap.py can find Web.py after a fresh clone.

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

* Build docker container, push to personal repo
* Better dependency and submodule management
* pip package?
* sqlite -> mysql