#!/usr/bin/env python
import os
import praw
import random
import urllib


r = praw.Reddit(user_agent='joeapplication')
print("Downloading links")
wallpapers = r.get_subreddit('wallpapers').get_top_from_week(limit=25)
earth = r.get_subreddit('earthporn').get_top_from_week(limit=25)
minimal = r.get_subreddit('minimalwallpaper').get_top_from_year(limit=20)
links = []
for w in wallpapers: links.append(str(w.url))
for e in earth: links.append(str(e.url))
for m in minimal: links.append(str(m.url))
for l in links:
	if(l.find("i.imgur") == -1 and l.find("ppcdn.500px") == -1):
		links.remove(l)
url = links[random.randint(0,len(links) - 1)]
imageName = url.replace("http://i.imgur.com/","").replace("http://ppcdn.500px.org/","").replace("/","")
f = open(imageName, "wb")
print(imageName)
print("Downloading image")
f.write(urllib.urlopen(url).read())
f.close()

directory = os.getcwd() + '/'

setup = 'file://' + directory + imageName
os.system("DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri '%s'" % (setup))


