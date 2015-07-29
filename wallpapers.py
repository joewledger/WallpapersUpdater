#!/usr/bin/env python
import os
import praw
import random
import urllib
import datetime
from enum import Enum
import itertools


class Status(Enum):
	success = 0
	failure = 1
	

def main():
	savedir = "/home/joe/Pictures/Wallpapers"
	subreddits = ['earthporn','minimalwallpaper','wallpapers']
	image_url = find_wallpaper(subreddits)
	status = Status.failure
	num_tries = 0
	while(num_tries < 5 and status == Status.failure):
		image_uri, status = download_wallpaper(image_url,savedir)
		num_tries += 1
	log(image_uri,status)
	if(status == Status.success):
		change_wallpaper(image_uri,status)
	
def find_wallpaper(subreddits):	
	agent = praw.Reddit(user_agent='joeapplication')
	wallpapers = itertools.chain.from_iterable([agent.get_subreddit(x).get_top_from_week(limit=25) for x in subreddits])
	urls = [str(wallpaper.url) for wallpaper in wallpapers]
	return random.choice(urls)

def download_wallpaper(url,savedir):
	image_name = url[url.rfind("/") + 1:]
	save_location = "%s%s" % (savedir,image_name)
	try:
		file_saver = urllib.URLopener()
		file_saver.retrieve(url, save_location)
		return save_location, Status.success
	except:
		return save_location, Status.failure
	
def log(image_uri,status):
	return None

def change_wallpaper(image_uri,status):
	filepath = "file://%s" % image_uri
	os.system('gsettings set org.cinnamon.desktop.background picture-uri "%s"' % filepath)

if __name__ == '__main__':
	main()
