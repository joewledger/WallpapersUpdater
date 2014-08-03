#!/usr/bin/env python
import os
import praw
import random
import urllib.request
import datetime
import platform


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
f.write(urllib.request.urlopen(url).read())
f.close()

op_sys = platform.system()

if(op_sys == "Linux"):
	directory = os.getcwd() + '/'
	setup = 'file://' + directory + imageName
	os.system("DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri '%s'" % (setup))

if(op_sys == "Windows"):
	directory = os.getcwd() + '\\'
	setup = directory + imageName
	cmd1 = 'reg add "HKCU\Control Panel\Desktop" /v Wallpaper /t REG_SZ /f /d "%s"' % (setup)
	os.system(cmd1)



f = open('log.txt','a')
log = "Image: " + imageName + ", Time: " + str(datetime.datetime.now()) + '\n'
f.writelines(log)
f.close()

if(op_sys == "Windows"):
	cmd2 = "%SystemRoot%\System32\RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters"
	print(cmd2)
	os.system(cmd2)