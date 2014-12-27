#!/usr/bin/env python3

# RSDC - sqweebking (2014)
# Reddit: Scrape, Download, Convert
# rsdc.py v1.1.0

import requests
import time
import pafy
import re
import sys
import os
import errno
import configparser
from pydub import AudioSegment
from os.path import expanduser
from reddiwrap.ReddiWrap import ReddiWrap

home = expanduser("~")
sub = str(sys.argv[1])

def readConfig():
  try: 
    cfile = home + '/.rsdc'
    config = configparser.ConfigParser()
    config.read(cfile)
    # Get vars from config file
    baseurl = config['PATHS']['baseurl']
    global inDir
    inDir = config['PATHS']['indir']
    global outDir
    outDir = config['PATHS']['outdir']
    global maxFS
    maxFS = int(config['LIMITS']['maxfs'])
    print('[OK]')
  except Exception:
    print('[FAIL]') 
    setup()

def setup():
  print('Generating new config..')
  config = configparser.ConfigParser()
  config['PATHS'] = {
 	    	'baseurl' : ' http://reddit.com/r/',
			  'indir' : home + '/Downloads/rsdc/in',
			  'outdir' : home + '/Downloads/rsdc/out'}
  config['LIMITS'] = {
        'maxFS' : '20'}
  cfile = home + '/.rsdc'
  with open(cfile, 'w') as configFile:
    config.write(configFile)
  print('Default config created: %s/.rsdc, restarting..' % home)
  configFile.close()
  readConfig()

def main():
  print('** Reddit: Scrape, Download, Convert **')
  print('Check config file:')
  readConfig()
  print('Check work directories:')
  checkPath('%s/%s' % (inDir, sub))
  checkPath('%s/%s' % (outDir, sub)) 
  links = scrape(sub)
  download(links)

# Updated scrape function uses Reddit API, via reddiwrapper, to grab post urls,
# sort out the YouTube links and return them as an array.
def scrape(sub):
  reddit = ReddiWrap(user_agent='RSDC by sqweebking')
  # Array to hold links
  links = []
  print('Scraping /r/%s' % sub)
  posts = reddit.get('/r/%s' % sub)
  for post in posts:
    if 'youtube' in post.url or 'youtu.be' in post.url:
      links.append(post.url)
  return(links)

# Perform download sequence on links array
def download(links):
  i = 0
  sources = []
  tSize = [] # array to hold file sizes for sum at the end
  start = time.time() # start time for download timer
  print('Attempting to download %d new songs' % len(links))
  print('Files larger than %dMB will be skipped' % (maxFS))
  for link in links:
    try:
      url = links[i]
      line1 = '%d. Opening: %s' % (i + 1, url)
      print(line1)
      video = pafy.new(url)
      audio = video.getbestaudio() # selects best available audio
      title = re.sub('[\'/,;:.!@$#<>]', '', video.title)
      file = '%s/%s/%s.%s' % (inDir, sub, title, audio.extension)
      size = audio.get_filesize() / 1048576	
      size = round(size)
      line2 = '- Downloading: %s - %sMB' % (file, str(size))
      if os.path.isfile(file):
        print('[SKIP] Source file already exists')
      elif size > maxFS: #Skip file if greater than max set in config
        print('[SKIP] File size is greater than %dMB' % (maxFS)) 
      else: # download audio if it doesn't already exist
        print(line2)
        audio.download(filepath=file)
        print('%s' % ''*len(line2))
        tSize.append(size)
        convert(file, url)
        sources.append(file)
      i += 1
    except Exception: # handle restricted/private videos etc.
      err = sys.exc_info()[:2]
      print('[FAIL] %s' % (err[1]))
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
  if sources: # if source array isn't empty display download info
    print('Total download: %d files, %dMB, in %d%s' % (len(sources), 
                                                       tSize, 
                                                       dlTime, 
                                                       dlTimeStr))
  else: # source array is empty
    print('No new files downloaded.')
  return sources

# Process new files for artist, title, ext.
def proc(file):
  path = '%s/%s/' % (inDir, sub)
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
    path = '%s/%s/%s' % (outDir, sub, outFile)
    print('- Exporting: %s' % (path))
    inFile.export(path, 
                  format='mp3', 
                  bitrate='192k', 
                  tags={'artist': artist,
                        'title': title, 
                        'album': 'RSDC Webrip', 
                        'comments': url})
  except:
    err = sys.exc_info()[:2]
    print('[FAIL] %s' % (err[1]))
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
    print('[NEW] %s' % path)
  except OSError as exception:
    print('[OK] %s' % path)
    if exception.errno != errno.EEXIST:
      raise 

# Call main
if __name__ == "__main__":
  main()
