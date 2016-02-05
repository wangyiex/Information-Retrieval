import urllib
import re
from bs4 import BeautifulSoup
import urlparse
import time

def crawlerDFS(URL,keyword):			#The crawler DFS function 
	prefix = "http://en.wikipedia.org"
	crawler = []						#use a list to keep the url node
	crawered = []						#keep the url we have already met before to avoid double check
	visited = []						#use a list to store 1000 unique URL and avoid loop
	visited.append(prefix+URL)
	crawered.append(URL)
	crawler.append((URL,1,True))		#use tuple to store the url depth and a boolean argument(use to check whether the keyword in the url or anchor text)
	count = 0
	while len(visited)< 1000:
		linktuple = crawler.pop(0)
		preurl = linktuple[0]
		depth = linktuple[1]
		boolean = linktuple[2]
		if depth<=5:
			if boolean and preurl not in visited and len(visited) < 1000:
				visited.append(preurl)
				count += 1
				print count,prefix+preurl
				htmltext = get_content(prefix+preurl)
				time.sleep(1)
				soup = BeautifulSoup(htmltext)
				for tag in soup.findAll(href = re.compile("^/wiki/")):
					link = tag.get('href')
					if "#" in link:
						link = avoid_dash(link)
					if ":" not in link and link not in crawered:
						if keyword in link:
							crawler.insert(0,(link,depth+1,True))
							crawered.append(link)
						elif tag.string is not None and keyword in tag.string:
							crawler.insert(0,(link,depth+1,True))
							crawered.append(link)
						else:
							crawler.insert(0,(link,depth+1,False))
							crawered.append(link)
						continue
			if not boolean:
				htmltext = get_content(prefix+preurl)
				time.sleep(1)
				soup = BeautifulSoup(htmltext)
				if match_content(soup,keyword) and preurl not in visited and len(visited) < 1000:
					visited.append(preurl)
					count += 1
					print count,prefix+preurl
					for tag in soup.findAll(href = re.compile("^/wiki/")):
						link = tag.get('href')
						if "#" in link:
							link = avoid_dash(link)
						if ":" not in link and link not in crawered:
							if keyword in link:
								crawler.insert(0,(link,depth+1,True))
								crawered.append(link)
							elif tag.string is not None and keyword in tag.string:
								crawler.insert(0,(link,depth+1,True))
								crawered.append(link)
							else:
								crawler.insert(0,(link,depth+1,False))
								crawered.append(link)
							continue

def get_content(url):					#I write the function in this way in order to deal with 10060 socket
	try:								#connect error, when meet this except, I just keep openning the url
		htmltext = urllib.urlopen(url)	#until suceess
		return htmltext
	except:
		return get_content(url)


def match_content(soup,keyword):		#The function named match_content accept a soup Object and a keyword
	if keyword in soup.text:			#and then check whether the keyword is in the soup text or not
		return True
	else:
		return False

def avoid_dash(link_with_dash):      	#The function named avoid_dash dealing with the url with a '#' in it
	oldlink = link_with_dash		 	#For example when the argument is "/wiki/abc#a" return "/wiki/abc"	
	index = oldlink.index('#')
	newlink = oldlink[0:index]
	return newlink

if __name__ == "__main__":
	URL = "/wiki/Sustainable_energy" 	#main call the function crawlerDFS with a keyword and a seed link
	keyword = "solar"
	crawlerDFS(URL,keyword)