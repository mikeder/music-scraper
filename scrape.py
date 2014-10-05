# Reddit.com music subreddit link scraper - Mike Eder 2014
#! /usr/bin/python

import httplib2, timeit, pafy, re, sys
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()

# Get args from sys.argv

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

# Remove Duplicates
ytLinks = unique(ytLinks)
scLinks = unique(scLinks)

# Function to perform youtube-dl on YT links

def ytDL():
	i = 0
	for link in ytLinks:
		i = int(i)
		video = pafy.new(ytLinks[i])
		audio = video.getbestaudio()
		title = re.sub('[/,.!@$#]', '', video.title)
		print "Downloading: " + title + "." + audio.extension
		audio.download(filepath=dir + title + "." + audio.extension)
		i += 1


ytDL()
#print str(" ".join(ytLinks))
