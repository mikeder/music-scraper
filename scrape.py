#!/usr/bin/env python3

# RSDC - Reddit Scrape Download Convert - sqweebking 2014
# scrape.py

import requests
import time
import pafy
import re
import sys
import os
import configparser
from pydub import AudioSegment
from bs4 import BeautifulSoup, SoupStrainer

config = configparser.ConfigParser()
config.read('scrape.conf')

# Get vars from config file
hyp = config['PATHS']['http']
inDir = config['PATHS']['inDIR']
outDir = config['PATHS']['outDIR']
maxFS = int(config['LIMITS']['maxFS'])
subDir = ''
sub = str(sys.argv[1])
if len(sys.argv) > 2: # If a sub directory is given, append it to the working
# directories
 subDir = str(sys.argv[2]) + '/'
 inDir = inDir + subDir
 outDir = outDir + subDir
else:
 pass
page = hyp + sub

# Scrape function takes URL of a page, looks for YouTube links and puts found
# links into an array for later use.
def scrape(url):
 # Array to hold links
 ytLinks = []

 print('Scraping links from: ' + page)
 response = requests.get(page)
 content = response.content
 # For loop to append found links
 for link in BeautifulSoup(content).find_all('a', href=True):
  if 'https://www.youtube.com' in link['href']:
   ytLinks.append(str(link['href']))
  if 'http://youtu.be' in link['href']:
   ytLinks.append(str(link['href']))
 # Remove Duplicates from link array
 ytLinks = list(set(ytLinks))

 return (ytLinks)

# Function to perform download sequence on array
def download():
 i = 0
 ytLinks = scrape(page)
 sources = []
 tSize = [] # array to hold file sizes for sum at the end
 start = time.time() # start time for download timer
 print('Attempting to download %d new songs' % len(ytLinks))
 print('Files larger than %dMB will be skipped' % (maxFS))
 for link in ytLinks:
  try:
   link = ytLinks[i]
   line1 = '%d. Opening: %s' % (i + 1, link)
   print(line1)
   video = pafy.new(link)
   audio = video.getbestaudio() # selects best available audio 
   title = re.sub('[\'/,;:.!@$#<>()]', '', str(video.title))
   file = inDir + title + '.' + audio.extension
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
   sys.exc_clear()
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
  print('- Exporting as: %s' % (outFile))
  inFile.export(outDir + outFile, format='mp3', bitrate='192k', tags={'artist': artist, 'title': title, 'album': 'YT Rip', 'comments': comments})
 except:
  err = sys.exc_info()[:2]
  print('* Problem** %s Export failed..' % (err[1]))
  sys.exc_clear()
 end = time.time()
 cvTime = round(end - start)
 cvTimeStr = ''
 if cvTime < 60: # determine if in seconds or minutes
  cvTimeStr = ' seconds'
 else:
  cvTime = round(cvTime / 60)
  cvTimeStr = ' minutes'
 
# Call the download function
download()
