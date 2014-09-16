# Reddit.com music subreddit link scraper - Mike Eder 2014
#!/usr/bin/env python2

import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()

# List possible subreddits
subs = ['electronicmusic','dnb','liquiddnb','trance','house','trap']
print "Subreddits available for scraping:"
for index, item in enumerate(subs):
	print index, item
try:
	sub = int(raw_input('Select a subreddit to grab links from: '))
except ValueError:
	print "You must enter a valid number!"

status, response = http.request('http://www.reddit.com/r/' + subs[sub])
# soup = BeautifulSoup(open.http('http://www.reddit.com/r/' + subs[sub]))

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

# Output link lists
print "Scraped links from www.reddit.com/r/" + subs[sub]
print "YouTube:"
print "\n".join(unique(ytLinks))
print "SoundCloud:"
print "\n".join(unique(scLinks))

