#!/usr/bin/env python3

# RSDC - Reddit Scrape Download Convert - sqweebking 2014
# scrape.py

import requests
import time
import pafy
import re
import sys
import os
import errno
import configparser
from pydub import AudioSegment
from bs4 import BeautifulSoup, SoupStrainer

def setup():
 print('Making you a config file!')
 config = configparser.ConfigParser()
 config['PATHS'] = {
 			'baseurl' : ' http://reddit.com/r/',
			'indir' : ' /home/music/scraped/in/',
			'outdir' : ' /home/music/scraped/out/'}
 config['LIMITS'] = {
 			'maxFS' : '20'}
 cfile = '/home/meder/.rsdc'
 with open(cfile, 'w') as configFile:
  config.write(configFile)
 print('A default config as been placed in ~/.rsdc, edit it to your liking')
 configFile.close()
 main()

def main():

 try: 
   cfile = '/home/meder/.rsdc'
   print('Reading config')
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
 except Exception:
  err = sys.exc_info()[:2]
  print('* Problem reading: %s' % (err[1])) 
  setup()
 
 sub = str(sys.argv[1])
 page = baseurl + sub
 links = scrape(page)
 download(sub,links)

# Scrape function takes URL of a page, looks for YouTube links and puts found
# links into an array for download function
def scrape(page):
 # Array to hold links
 links = []

 print('Scraping: ' + page)
 response = requests.get(page)
 content = response.content
 # For loop to append found links
 for link in BeautifulSoup(content).find_all('a', href=True):
  if 'https://www.youtube.com' in link['href']:
   links.append(str(link['href']))
  if 'http://youtu.be' in link['href']:
   links.append(str(link['href']))

 time.sleep(1)
 # Remove Duplicates from link array
 links = list(set(links))
 print('Found %d links' % len(links))
 return (links)

# Function to perform download sequence on array
def download(sub, links):
 i = 0
 sources = []
 checkIN = checkPath(inDir + sub)
 checkOUT = checkPath(outDir + sub)
 tSize = [] # array to hold file sizes for sum at the end
 start = time.time() # start time for download timer
 print('Attempting to download %d new songs' % len(links))
 print('Files larger than %dMB will be skipped' % (maxFS))
 for link in links:
  try:
   link = links[i]
   line1 = '%d. Opening: %s' % (i + 1, link)
   print(line1)
   video = pafy.new(link)
   audio = video.getbestaudio() # selects best available audio 
   title = re.sub('[\'/,;:.!@$#<>()]', '', str(video.title))
   file = inDir + sub + '/' + title + '.' + audio.extension
   size = audio.get_filesize() / 1048576	
   size = round(size)
   line2 = '- Downloading to: %s - %sMB' % (file, str(size))
   if os.path.isfile(file):
    print('- Source file already exists, skipping')
   elif size > maxFS: #Skip file if greater than max set in config
    print('- File size is greater than max allowed for download, skipping') 
   else: # download audio if it doesn't already exist
    print(line2)
    audio.download(filepath=file)
    print('%s' % ''*len(line2))
    tSize.append(size)
    convert(file)
    sources.append(file)
   i += 1
  except Exception: # handle restricted/private videos etc.
   err = sys.exc_info()[:2]
   print('* Problem: %s, skipping' % (err[1]))
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
  print('Total download: %d files, %dMB, in %d%s' % (len(sources), tSize, dlTime, dlTimeStr))
 else: # source array is empty
  print('No new files downloaded.')
 return sources
# Function to process new files for artist, title, ext.
def proc(track):
 path = track
 file = path[len(inDir):-4]
 ext = path[-4:]
 split = file.split('-')
 where = file.find('-')
 if len(split) > 2:
  artist = split[0] + split[1]
  title = split[2]
 elif len(split) < 2:
  artist = file
  title = file
 elif len(split) == 2:
  artist = split[0]
  title = split[1]
 else:
  split = file.split(' ')
  artist = split[0]
  title = split - split[0]
 return (path, file, ext, artist, title)
	
# Function to convert files to mp3
def convert(track):
 start = time.time()
 try:
  (path, file, ext, artist, title) = proc(track)
  inFile = AudioSegment.from_file(path)
  comments = 'Ripped by music-scraper w/ help from pafy and pydub'
# Export converted file in mp3 format to below dir
  if artist == title:
   outFile = '%s.mp3' % (artist)
  else:
   outFile = '%s-%s.mp3' % (artist, title)
  print('- Exporting to: %s' % (outDir + outFile))
  inFile.export(outDir + outFile, format='mp3', bitrate='192k', tags={'artist': artist, 'title': title, 'album': 'YT Rip', 'comments': comments})
 except:
  err = sys.exc_info()[:2]
  print('* Problem** %s Export failed..' % (err[1]))
  pass
 end = time.time()
 cvTime = round(end - start)
 cvTimeStr = ''
 if cvTime < 60: # determine if in seconds or minutes
  cvTimeStr = ' seconds'
 else:
  cvTime = round(cvTime / 60)
  cvTimeStr = ' minutes'

def checkPath(path):
 try:
  os.makedirs(path)
  print('Created new directory %s' % path)
 except OSError as exception:
  print('Directory exists %s' % path)
  if exception.errno != errno.EEXIST:
   raise 

# Call main
main()
