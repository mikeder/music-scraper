#!/usr/bin/env python

# RSDC - Reddit Scrape Download Convert (Mike Eder 2014)

import httplib2, time, pafy, re, sys, os, ConfigParser
from bs4 import BeautifulSoup, SoupStrainer
from pydub import AudioSegment

config = ConfigParser.RawConfigParser()
config.readfp(open(r'/etc/rsdc.config'))


http = httplib2.Http()

# Get vars from sys.argv and rsdc.config

sub = str(sys.argv[1])
full = 'http://www.reddit.com/r/' + sub
inDir = config.get('paths', 'inDir')
outDir = config.get('paths', 'outDir')

print 'Scraping links from ' + full
status, response = http.request(full)

# Function to remove duplicate links
def unique(items):
	found = set([])
	keep = []
	
	for item in items:
		if item not in found:
			found.add(item)
			keep.append(item)
	return keep

# Arrays to hold links
ytLinks = []
scLinks = []

# For loop to append found links
for link in BeautifulSoup(response).find_all('a', href=True):
	if 'https://www.youtube.com' in link['href']:
		ytLinks.append(str(link['href']))
	if 'https://soundcloud.com' in link['href']:
		scLinks.append(str(link['href']))

# Remove Duplicates from link arrays
ytLinks = unique(ytLinks)
scLinks = unique(scLinks)

# Array to hold downloaded files path for conversion function
sources = []

# Function to perform audio download on YT links
def ytDL():
	i = 0
	tSize = [] # array to hold file sizes for sum at the end
	start = time.time() # start time for download timer
	for link in ytLinks:
		try:
			link = ytLinks[i]
			video = pafy.new(link)
			audio = video.getbestaudio() # selects best available audio stream
			title = re.sub('[/,.!@$#<>()]', '', video.title)
			file = inDir + title + '.' + audio.extension
			size = audio.get_filesize() / 1048576
			line1 = '%d. Opening: %s' % (i + 1, link)	
			line2 = '   Downloading to: %s - %sMB' % (file, str(size))
			if os.path.isfile(file):
				print '%s already exists, skipping' % file
			else: # download audio if it doesn't already exist
				print line1
				print line2
				audio.download(filepath=file)
				sources.append(file)
				print '%s' % ''*len(line2)
				tSize.append(size)
			i += 1
		except Exception: # handle restricted/private videos etc.
			err = sys.exc_info()[:2]
			print '%d. **Problem** %s, skipping' % (i + 1, err[1])
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
		print 'Total download: %d files, %dMB, in %d%s' % (len(sources), tSize, dlTime, dlTimeStr)
	else: # source array is empty
		print 'No new files downloaded.'

# Function to process new files for artist, title, ext.
def proc(i):
	path = sources[i]
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
def convert():
	i = 0
	c = 0
	start = time.time()
	try:
		for file in sources:
			(path, file, ext, artist, title) = proc(i)
			inFile = AudioSegment.from_file(path)
			comments = 'Ripped by music-scraper w/ help from pafy and pydub'
# Export converted file in mp3 format to below dir
			if artist == title:
				outFile = '%s.mp3' % (artist)
			else:
				outFile = '%s-%s.mp3' % (artist, title)
			
			print '%d. Exporting: %s' % (i+1, outFile)
			inFile.export(outDir + outFile, format='mp3', bitrate='192k', tags={'artist': artist, 'title': title, 'album': 'YT Rip', 'comments': comments})
			c += 1		
			i += 1
	except:
		err = sys.exc_info()[:2]
                print '  **Problem** %s Export failed..' % (err[1])
                sys.exc_clear()
                i += 1
	end = time.time()
	cvTime = round(end - start)
        cvTimeStr = ''
        if cvTime < 60: # determine if in seconds or minutes
                cvTimeStr = ' seconds'
        else:
                cvTime = round(cvTime / 60)
                cvTimeStr = ' minutes'
	if sources:
		print 'Converted %d files in %d %s' % (c, cvTime, cvTimeStr)
	else:
		print 'No files to convert. :('

print 'Attempting to download %d new songs' % len(ytLinks)
# Call the download function
ytDL()
print 'Converting files to MP3'
convert()
