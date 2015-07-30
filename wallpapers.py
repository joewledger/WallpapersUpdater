#!/usr/bin/env python
import os
import praw
import random
import urllib
import datetime
from enum import Enum
import itertools
import time


class Status(Enum):
    changed_wallpaper = 0
    finished_download = 1
    selected_url = 2
    unchanged_wallpaper = 3
    failed_download = 4
    no_suitable_url = 5
    enter_control = 6

def main():
    savedir = "/home/joe/Pictures/Wallpapers"
    subreddits = ['earthporn','minimalwallpaper','wallpapers']
    file_extensions = ['.png','.jpg']
    num_tries = 0

    status = Status.enter_control
    image_uri = None

    image_url ,status = find_wallpaper(subreddits,file_extensions)
    if(status == Status.selected_url):
        image_uri,status = download_wallpaper(image_url,savedir)
    if(status == Status.finished_download):
        status = change_wallpaper(image_uri)
    log(image_uri,savedir,status)
	
def find_wallpaper(subreddits,file_extensions):
    agent = praw.Reddit(user_agent='joeapplication')
    wallpapers = itertools.chain.from_iterable([agent.get_subreddit(x).get_top_from_week(limit=25) for x in subreddits])
    urls = [str(wallpaper.url) for wallpaper in wallpapers]
    url = ""
    while(not url.endswith(tuple(file_extensions))):
        if(len(urls) == 0):
            return None, Status.no_suitable_url
        url = random.choice(urls)
        urls.remove(url)
    return url, Status.selected_url

def download_wallpaper(url,savedir):
    image_name = url[url.rfind("/") + 1:]
    save_location = "%s/%s" % (savedir,image_name)
    try:
        file_saver = urllib.URLopener()
        file_saver.retrieve(url, save_location)
        return save_location, Status.finished_download
    except:
        return save_location, Status.failed_download
	
def log(image_uri,savedir,status):
    log_file = "%s/log.txt" % savedir
    log_flag = "a" if os.path.isfile(log_file) else "w"
    writer = open(log_file,log_flag)
    status_message = "Something unexpected happened, please try again."
    if(status == Status.changed_wallpaper): status_message = "The wallpaper has been changed successfully."
    elif(status == Status.unchanged_wallpaper): status_message = "The wallpaper downloaded successfully but could not be set"
    elif(status == Status.failed_download): status_message = "The wallpaper failed to download"
    elif(status == Status.no_suitable_url): status_message = "There were no suitable images that met the search criteria"
    writer.write("Image_URI: %s\tStatus: %s\tDate: %s\tTime: %s" % (image_uri,status_message, time.strftime("%m/%d/%y"),time.strftime("%I:%M:%S")))
    writer.close()

def change_wallpaper(image_uri):
    filepath = "file://%s" % image_uri
    try:
        os.system('gsettings set org.cinnamon.desktop.background picture-uri "%s"' % filepath)
        return Status.changed_wallpaper
    except:
        return Status.unchanged_wallpaper

if __name__ == '__main__':
    main()
