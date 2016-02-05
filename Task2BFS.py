import urllib
import re
from bs4 import BeautifulSoup
import urlparse
import time


def crawler(URL,keyword):
	prefix = "http://en.wikipedia.org"
	crawler = []
	visited = []
	crawler.append(URL)
	visited.append(URL)
	count = 1
	depth = 1
	while depth < 5 and crawler is not None and len(visited)<1000:
		length = len(crawler)
		for i in range(0,length):
			preurl = crawler.pop(0)
			htmltext = get_content(prefix+preurl)
			soup = BeautifulSoup(htmltext)
			for tag in soup.findAll(href = re.compile("^/wiki/")):
				time.sleep(1)
				link = tag.get('href')
				if "#" in link:
					link = avoid_dash(link)
				if ":" not in link and link not in visited:
					if len(visited)<1000:
						if keyword in link:
							count += 1
							crawler.append(link)
							visited.append(link)
							print count,prefix+link
						elif tag.string is not None and keyword in tag.string:
							count += 1
							crawler.append(link)
							visited.append(link)
							print count,prefix+link
						elif match_content(soup,keyword):
							count += 1
							crawler.append(link)
							visited.append(link)
							print count,prefix+link
					else:
						break
		depth += 1

def get_content(url):
	try:
		htmltext = urllib.urlopen(url)
		return htmltext
	except:
		return get_content(url)


def match_content(soup,keyword):
	if keyword in soup.text:
		return True
	else:
		return False

def avoid_dash(link_with_dash):
	oldlink = link_with_dash
	index = oldlink.index('#')
	newlink = oldlink[0:index]
	return newlink

if __name__ == "__main__":
	URL = "/wiki/Sustainable_energy"
	keyword = "solar"
	crawler(URL,keyword)