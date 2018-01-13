#!/usr/bin/env python

# RSDC - sqweebking (2014)
# Reddit: Scrape, Download, Convert

import time
import datetime
import pafy
import re
import sys
import os
import errno
import configparser
import urllib
from pydub import AudioSegment
from os.path import expanduser
from reddiwrap.ReddiWrap import ReddiWrap
import sqlite3


def setup(a_home_path):
    print('[RSDC] Generating new config..')
    config_file = a_home_path + '/.rsdc.conf'
    database_path = a_home_path + '/.rsdc.db'
    download_path = a_home_path + '/Downloads/rsdc'
    config = configparser.ConfigParser()
    config['paths'] = {}
    config['paths']['database_path'] = database_path
    config['paths']['download_path'] = download_path
    config['limits'] = {}
    config['limits']['max_downloads'] = '100'
    config['limits']['max_filesize'] = '20'
    with open(config_file, 'w') as outfile:
        config.write(outfile)
    outfile.close()
    return config_file


def main():
    print('** Reddit: Scrape, Download, Convert **')
    try:
        sub = str(sys.argv[1])
    except:
        sub = None
        print "Expecting <sub> as first argument"
        exit(1)

    # Setup
    home = expanduser("~")
    config_path = home + '/.rsdc.conf'
    config = configparser.ConfigParser()

    # Checks
    print '[RSDC] Check config file'
    if not os.path.isfile(config_path):
        config_path = setup(home)
    config.read(config_path)
    download_dir = config['paths']['download_path']
    print('[RSDC] Check download directory')
    checkPath('%s/%s' % (download_dir, sub))
    print('[RSDC] Check database')
    database_path = config['paths']['database_path']
    if os.path.isfile(database_path):
        print('[RSDC] OK')
    else:
        createDB(database_path)
    links = scrape(sub)
    download(config, links, sub)


def scrape(sub):
    """
    Scrape a subreddit for YouTube links and return them as a list
    :param sub:
    :return:
    """
    reddit = ReddiWrap(user_agent='RSDC by sqweebking')
    links = []
    print('[RSDC] Scraping /r/%s' % sub)
    posts = reddit.get('/r/%s' % sub)
    for post in posts:
        if 'youtube' in post.url or 'youtu.be' in post.url:
            links.append(post.url)
    return links


def createDB(a_db_path):
    sql = '''
        CREATE TABLE IF NOT EXISTS
        data(id INTEGER PRIMARY KEY,
            date DATETIME,
            sub TEXT,
            link TEXT,
            title TEXT,
            size FLOAT)
        '''
    print "Creating {db}".format(db=a_db_path)
    db = sqlite3.connect(a_db_path)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    print('[RSDC] Database created')


def link_exists_in_db(a_db, a_link):
    """
    Check database for existing links prior to download
    :param a_db:
    :param a_link:
    :return:
    """
    sql = '''
        SELECT date FROM data WHERE link = ?'''
    db = sqlite3.connect(a_db)
    cursor = db.cursor()
    cursor.execute(sql,(a_link,))
    exists = cursor.fetchall()
    db.close()
    if exists:
        return True
    else:
        return False


def add_link_to_db(a_db, a_sub, a_link, a_title, a_size):
    """
    Update scraped database with new download metadata
    :param a_db:
    :param a_sub:
    :param a_link:
    :param a_title:
    :param a_size:
    :return:
    """
    date = datetime.datetime.now()
    sql = '''
        INSERT INTO data(date, sub, link, title, size)
        VALUES(?,?,?,?,?)'''
    data = [(date,a_sub,a_link,a_title,a_size)]
    db = sqlite3.connect(a_db)
    cursor = db.cursor()
    cursor.executemany(sql,data)
    db.commit()
    db.close()


def download(a_config, a_link_list, a_sub):
    """
    Download a list of links to the given directory
    :param a_link_list: list of YouTube links to download and process
    :param a_config: dictionary containing configuration values
    :return:
    """
    db = a_config['paths']['database_path']
    download_dir = a_config['paths']['download_path']
    max_filesize = int(a_config['limits']['max_filesize'])

    i = 0
    count = 0
    tSize = [] # list to hold file sizes for sum at the end
    start = time.time() # start time for download timer
    print '[RSDC] Attempting to download %d new songs' % len(a_link_list)
    print '[RSDC] Files larger than {}MB will be skipped'.format(max_filesize)
    for link in a_link_list:
        if 'attribution_link' in link:
            link = urllib.unquote_plus(link)
            link = "https://www.youtube.com/{}".format(link[link.find('watch'):])
        try:
            line1 = '%d. Opening: %s' % (i + 1, link)
            print('[RSDC] ' + line1)
            video = pafy.new(link)
            audio = video.getbestaudio() # selects best available audio
            title = re.sub('[\'/,;:.!@$#<>]', '', video.title)
            file = '%s/%s/%s.%s' % (download_dir, a_sub, title, audio.extension)
            size = audio.get_filesize() / 1048576
            size = round(size, 2)
            line2 = '- Downloading: %s - %sMB' % (file, str(size))
            exists = link_exists_in_db(db, link)
            if exists:
                print('[RSDC] [SKIP] Link found in database')
            elif size > max_filesize:
                # Skip file if greater than max set in config
                print('[RSDC] [SKIP] File size is greater than %dMB' % max_filesize)
            else:
                # download audio if it doesn't already exist
                print('[RSDC] ' + line2)
                audio.download(filepath=file)
                print('%s' % ''*len(line2))
                tSize.append(size)
                convert(file, download_dir, a_sub, link)
                add_link_to_db(db, a_sub, link, title, size)
                count += 1
                os.remove(file)
            i += 1
        except Exception: # handle restricted/private videos etc.
            err = sys.exc_info()[:2]
            print('[RSDC] [FAIL] %s' % (err[1]))
            pass
            i += 1
    tSize = sum(tSize)
    end = time.time() # end time for download timer
    dlTime = round(end - start, 2)
    dlTimeStr = ''
    if dlTime < 60: # determine if seconds or minutes
        dlTimeStr = ' seconds'
    else:
        dlTime = round(dlTime / 60)
        dlTimeStr = ' minutes'
    if count: # if download count > 0 display downloads info
        print('[RSDC] Total download: %d files, %dMB, in %d%s' % (count,
                                                      tSize,
                                                      dlTime,
                                                      dlTimeStr))
    else:
        # nothing was actually downloaded
        print('[RSDC] No new files downloaded.')
    return 0


def proc(a_file, a_download_dir, a_sub):
    """
    Process new files for artist, title, ext.
    :param a_file:
    :param a_download_dir:
    :param a_sub:
    :return: Artist and Title
    """
    path = '%s/%s/' % (a_download_dir, a_sub)
    track = a_file[len(path):-4]
    split = track.split('-')
    if len(split) > 2:
        a = split[0] + split[1]
        t = split[2]
    elif len(split) < 2:
        a = track
        t = ''
    elif len(split) == 2:
        a = split[0]
        t = split[1]
    else:
        split = a_file.split(' ')
        a = split[0]
        t = split - split[0]
    return a, t


def convert(a_file, a_download_dir, a_sub, a_url):
    """
    Convert downloaded file to mp3 and tag with tags from proc()
    :param a_file:
    :param a_download_dir:
    :param a_sub:
    :param a_url:
    :return: None
    """
    start = time.time()
    try:
        (artist, title) = proc(a_file, a_download_dir, a_sub)
        in_file = AudioSegment.from_file(a_file)
        if artist == title:
            out_file = '%s.mp3' % artist
        else:
            out_file = '%s-%s.mp3' % (artist, title)
        path = '%s/%s/%s' % (a_download_dir, a_sub, out_file)
        print '[RSDC] - Exporting: %s' % path
        in_file.export(path,
                       format='mp3',
                       bitrate='320k',
                       tags={'artist': artist,
                             'title': title,
                             'album': '/r/%s' % a_sub,
                             'comments': a_url})
    except:
        err = sys.exc_info()[:2]
        print('[RSDC] [FAIL] %s' % (err[1]))
        pass
    end = time.time()
    cvTime = round(end - start, 2)
    cvTimeStr = ''
    if cvTime < 60: # determine if in seconds or minutes
        cvTimeStr = ' seconds'
    else:
        cvTime = round(cvTime / 60)
        cvTimeStr = ' minutes'


def checkPath(path):
    """
    Check Directories, and create them if not exist
    :param path:
    :return:
    """
    try:
        os.makedirs(path)
        print('[RSDC] [NEW] %s' % path)
    except OSError as exception:
        print('[RSDC] [OK] %s' % path)
        if exception.errno != errno.EEXIST:
            raise


if __name__ == "__main__":
  main()
