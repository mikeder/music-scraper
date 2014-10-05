# Reddit.com music subreddit  scraper/downloader/convertor - Mike Eder 2014
#! /usr/bin/python

import httplib2, time, pafy, re, sys, os
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()

# Get vars from sys.argv

sub = str(sys.argv[1])
full = 'http://www.reddit.com/r/' + sub
dir = str(sys.argv[2])
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
			video = pafy.new(ytLinks[i])
			audio = video.getbestaudio() # selects best available audio stream
			title = re.sub('[/,.!@$#<>()]', '', video.title)
			file = dir + title + '.' + audio.extension
			size = audio.get_filesize() / 1048576
			line = 'Downloading: %s - %sMB' % (file, str(size))
			if os.path.isfile(file):
				print '%s already exists, skipping' % file
			else: # download audio if it doesn't already exist
				print line
				audio.download(filepath=file)
				sources.append(file)
				print '%s' % ''*len(line)
				tSize.append(size)
			i += 1
		except Exception: # handle exceptions by skipping restricted/private videos
			print 'Error opening %s, skipping' % ytLinks[i]
# -- Uncomment below line to show exception value --
#			print sys.exc_info()[:2]
			sys.exc_clear()
			i += 1
	tSize = sum(tSize)
	end = time.time() # end time for download timer
	dlTime = round(end - start)
	dlTimeStr = ''
	if dlTime < 60: # determine if downloaded in seconds or minutes
		dlTimeStr = ' seconds'
	else:
		dlTime = round(dlTime / 60)
		dlTimeStr = ' minutes'
	if sources: # if source array isn't empty display downloaded file paths and time
		print 'New files:\r'
		print '\n'.join(sources)
		print 'Total downloaded: %dMB in %d%s' % (tSize, dlTime, dlTimeStr)
	else: # source array is empty
		print 'No new files downloaded.'

print 'Attempting to download %d new songs' % len(ytLinks)
# Call the download function
ytDL()
