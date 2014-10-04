# Reddit.com music subreddit link scraper - Mike Eder 2014
#! /usr/bin/python

import httplib2, timeit, pafy, re, sys
from bs4 import BeautifulSoup, SoupStrainer


http = httplib2.Http()

# List possible subreddits
#subs = ['electronicmusic','dnb','liquiddnb','trance','house','trap']
#print "Subreddits available for scraping:"
#for index, item in enumerate(subs):
#	print index, item
#try:
#	sub = int(raw_input('Select a subreddit to grab links from: '))
#except ValueError:
#	print "You must enter a valid number!"

# Get sub from sys.argv

sub = str(sys.argv[1])
full = 'http://www.reddit.com/r/' + sub
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

# Output link lists
#print "Scraped links from www.reddit.com/r/" + subs[sub]
#print "YouTube:"
#print "\n".join(ytLinks)
#print "SoundCloud:"
#print "\n".join(scLinks)

# Function to perform youtube-dl on YT links

def ytDL():
	i = 0
	for link in ytLinks:
		i = int(i)
		video = pafy.new(ytLinks[i])
		audio = video.getbestaudio(preftype="m4a",ftypestrict=True)
		title = re.sub('[/,.!@$#]', '', video.title)
		print "Downloading: " + title + "." + audio.extension
		audio.download(filepath="/home/meder/Source/in/" + title + "." + audio.extension)
		i += 1


ytDL()
#print str(" ".join(ytLinks))
