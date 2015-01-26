#!/usr/bin/env python3

# RSDC - sqweebking (2014)
# Reddit: Scrape, Download, Convert
# rsdc.py v1.2

import requests
import time
import datetime
import pafy
import re
import sys
import os
import errno
import configparser
from pydub import AudioSegment
from os.path import expanduser
from reddiwrap.ReddiWrap import ReddiWrap
import sqlite3

home = expanduser("~")
sub = str(sys.argv[1])
cwd = os.path.dirname(os.path.realpath(__file__))
dbpath = cwd + '/data/scraped.db'

def readConfig():
  try: 
    cfile = home + '/.rsdc'
    config = configparser.ConfigParser()
    config.read(cfile)
    # Get vars from config file
    baseurl = config['PATHS']['baseurl']
    global downloadDir 
    downloadDir = config['PATHS']['downloadDir']
    global maxFS
    maxFS = int(config['LIMITS']['maxfs'])
    print('[RSDC] OK')
  except Exception:
    print('[RSDC] FAIL') 
    setup()

def setup():
  print('[RSDC] Generating new config..')
  config = configparser.ConfigParser()
  config['PATHS'] = {
 	    	'baseurl' : ' http://reddit.com/r/',
		'downloadDir' : home + '/Downloads/rsdc'}
  config['LIMITS'] = {
        	'maxFS' : '20'}
  cfile = home + '/.rsdc'
  with open(cfile, 'w') as configFile:
    config.write(configFile)
  print('[RSDC] Default config created: %s/.rsdc, restarting..' % home)
  configFile.close()
  readConfig()

def main():
  print('** Reddit: Scrape, Download, Convert **')
  print('[RSDC] Check config file')
  readConfig()
  print('[RSDC] Check download directory')
  checkPath('%s/%s' % (downloadDir, sub))
  print('[RSDC] Check database')
  if os.path.isfile(dbpath):
    print('[RSDC] OK')
  else:
    createDB()
    print('[RSDC] Database created')
  links = scrape(sub)
  download(links)

# Updated scrape function uses Reddit API, via reddiwrapper, to grab post urls,
# sort out the YouTube links and return them as a list
def scrape(sub):
  reddit = ReddiWrap(user_agent='RSDC by sqweebking')
  # List to hold links
  links = []
  print('[RSDC] Scraping /r/%s' % sub)
  posts = reddit.get('/r/%s' % sub)
  for post in posts:
    if 'youtube' in post.url or 'youtu.be' in post.url:
      links.append(post.url)
  return(links)

# Create database if it doesn't exist
def createDB():
  sql = '''
        CREATE TABLE IF NOT EXISTS
          data(id INTEGER PRIMARY KEY,
          date DATETIME,
          sub TEXT,
          link TEXT,
          title TEXT,
          size INT)'''
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.execute(sql)
  db.commit()
  db.close()

# Check database for existing links before download
def checkDB(link):
  sql = '''
        SELECT date FROM data WHERE link = ?''' 
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.execute(sql,(link,))
  exists = cursor.fetchall()
  db.close()
  if exists:
    return 1
  else:
    return 0

# Update scraped database with new downloads
def updateDB(link, title, size):
  date = datetime.datetime.now()
  sql = '''
        INSERT INTO data(date, sub, link, title, size)
        VALUES(?,?,?,?,?)'''
  data = [(date,sub,link,title,size)]
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.executemany(sql,data)
  db.commit()
  db.close()

# Perform download sequence on link list 
def download(links):
  i = 0
  count = 0 
  tSize = [] # list to hold file sizes for sum at the end
  start = time.time() # start time for download timer
  print('[RSDC] Attempting to download %d new songs' % len(links))
  print('[RSDC] Files larger than %dMB will be skipped' % (maxFS))
  for link in links:
    try:
      url = links[i]
      line1 = '%d. Opening: %s' % (i + 1, url)
      print('[RSDC] ' + line1)
      video = pafy.new(url)
      audio = video.getbestaudio() # selects best available audio
      title = re.sub('[\'/,;:.!@$#<>]', '', video.title)
      file = '%s/%s/%s.%s' % (downloadDir, sub, title, audio.extension)
      size = audio.get_filesize() / 1048576	
      size = round(size)
      line2 = '- Downloading: %s - %sMB' % (file, str(size))
      exists = checkDB(url)
      if exists:
        print('[RSDC] [SKIP] Link found in database')
      elif size > maxFS: #Skip file if greater than max set in config
        print('[RSDC] [SKIP] File size is greater than %dMB' % (maxFS)) 
      else: # download audio if it doesn't already exist
        print('[RSDC] ' + line2)
        audio.download(filepath=file)
        print('%s' % ''*len(line2))
        tSize.append(size)
        convert(file, url)
        updateDB(url, title, size)
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
  dlTime = round(end - start)
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
  else: # nothing was actually downloaded
    print('[RSDC] No new files downloaded.')
  return 0 

# Process new files for artist, title, ext.
def proc(file):
  path = '%s/%s/' % (downloadDir, sub)
  track = file[len(path):-4]
  split = track.split('-')
  where = track.find('-')
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
    split = file.split(' ')
    a = split[0]
    t = split - split[0]
  return (a, t)
	
# Convert downloaded file to mp3 and tag with tags from proc() 
def convert(file, url):
  start = time.time()
  try:
    (artist, title) = proc(file)
    inFile = AudioSegment.from_file(file)
    if artist == title:
      outFile = '%s.mp3' % (artist)
    else:
      outFile = '%s-%s.mp3' % (artist, title)
    path = '%s/%s/%s' % (downloadDir, sub, outFile)
    print('[RSDC] - Exporting: %s' % (path))
    inFile.export(path, 
                  format='mp3', 
                  bitrate='192k', 
                  tags={'artist': artist,
                        'title': title, 
                        'album': '/r/%s' % sub, 
                        'comments': url})
  except:
    err = sys.exc_info()[:2]
    print('[RSDC] [FAIL] %s' % (err[1]))
    pass
  end = time.time()
  cvTime = round(end - start)
  cvTimeStr = ''
  if cvTime < 60: # determine if in seconds or minutes
    cvTimeStr = ' seconds'
  else:
    cvTime = round(cvTime / 60)
    cvTimeStr = ' minutes'

# Check Directories, and create them if not exist
def checkPath(path):
  try:
    os.makedirs(path)
    print('[RSDC] [NEW] %s' % path)
  except OSError as exception:
    print('[RSDC] [OK] %s' % path)
    if exception.errno != errno.EEXIST:
      raise 

# Call main
if __name__ == "__main__":
  main()
