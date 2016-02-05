import urllib
import re
from bs4 import BeautifulSoup
import urlparse
import time

def crawler():
	prefix = "http://en.wikipedia.org"
	crawler = []
	visited = []
	raw = []
	crawler.append("/wiki/Sustainable_energy")
	visited.append(prefix+"/wiki/Sustainable_energy")
	depth = 1
	while depth < 5:
		length = len(crawler)
		for i in range(0,length):
			preurl = crawler.pop(0)
			htmltext = urllib.urlopen(prefix+preurl)
			time.sleep(1)
			soup = BeautifulSoup(htmltext)
			for tag in soup.findAll(href = re.compile("^/wiki/")):
				link = tag.get('href')
				if "#" in link:
					link = avoid_dash(link)
				if ":" not in link and link not in visited:					
					if len(visited)<1000:
						visited.append(prefix+link)
						crawler.append(link)
						raw.append(urllib.urlopen(prefix+link).read())
						time.sleep(1)
						print prefix+link
		depth += 1

def avoid_dash(link_with_dash):
	oldlink = link_with_dash
	index = oldlink.index('#')
	newlink = oldlink[0:index]
	return newlink

if __name__ == "__main__":
    crawler()			