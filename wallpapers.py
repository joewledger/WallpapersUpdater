#!/usr/bin/python
import os
import praw
import random
import urllib
from enum import Enum
import itertools
import time
import argparse
from crontab import CronTab


class Status(Enum):
    changed_wallpaper = 0
    finished_download = 1
    selected_url = 2
    unchanged_wallpaper = 3
    failed_download = 4
    no_suitable_url = 5
    find_wallpaper = 6
    bad_arguments = 7
    install_crontab = 8
    crontab_success = 9
    crontab_failure = 10

def main():
    image_uri = ""

    parser = argparse.ArgumentParser(description="An automatic desktop wallpaper updater.\nScrapes images from reddit.com wallpaper subreddits.")
    parser.add_argument('savedir',type=str,help="The directory to save wallpapers and log to.")
    parser.add_argument('--subreddits',nargs='+',type=str,help='The subreddits to scrape images from.\nDefault are earthporn, minimalwallpaper, and wallpapers')
    parser.add_argument('--extensions',nargs='+',type=str,help='The allowed file extensions.\nDefault are .jpg and .png')
    parser.add_argument('--install_crontab',type=str,help='Installs program on user\'s crontab.\nOptions are minute, hour, day, week, or month')

    parser.set_defaults(subreddits=['earthporn','minimalwallpaper','wallpapers'],extensions=['.png','.jpg'])

    try:
        args = parser.parse_args()
        status = (Status.find_wallpaper if args.install_crontab == None else Status.install_crontab)
    except:
        status = Status.bad_arguments

    if(status == Status.install_crontab):
        status = install_crontab(args)
    if(status == Status.find_wallpaper):
        image_url ,status = find_wallpaper(args.subreddits,args.extensions)
    if(status == Status.selected_url):
        image_uri,status = download_wallpaper(image_url,args.savedir)
    if(status == Status.finished_download):
        status = change_wallpaper(image_uri)
    try:
        log(image_uri,args.savedir,status)
    except:
        pass

def install_crontab(args):
    cron_command = "DISPLAY=:0.0 /usr/bin/python %s %s --subreddits %s --extensions %s" % (os.path.realpath(__file__),args.savedir," ".join(x for x in args.subreddits)," ".join(y for y in args.extensions))
    try:
        cron = CronTab(user=True)
        job = cron.new(command=cron_command)
        if(args.install_crontab == 'minute'):
            job.setall('*/1 * * * *')
        elif(args.install_crontab == 'hour'):
            job.setall('0 * * * *')
        elif(args.install_crontab == 'day'):
            job.setall('0 0 * * *')
        elif(args.install_crontab == 'week'):
            job.setall('0 0 0 * *')
        elif(args.install_crontab == 'month'):
            job.setall('0 0 0 0 *')
        else:
            return Status.crontab_failure
        job.enable()
        cron.write()
        return Status.crontab_success
    #0 * * * * DISPLAY=:0.0 /usr/bin/python $HOME/Programming/WallpapersUpdater/wallpapers.py /home/joe/Pictures/Wallpapers
    except:
        return Status.crontab_failure
	
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

def change_wallpaper(image_uri):
    filepath = "file://%s" % image_uri
    try:
        os.system('gsettings set org.cinnamon.desktop.background picture-uri "%s"' % filepath)
        return Status.changed_wallpaper
    except:
        return Status.unchanged_wallpaper

def log(image_uri,savedir,status):
    log_file = "%s/log.txt" % savedir
    log_flag = "a" if os.path.isfile(log_file) else "w"
    writer = open(log_file,log_flag)
    status_message = "Something unexpected happened, please try again."
    if(status == Status.changed_wallpaper): status_message = "The wallpaper has been changed successfully."
    elif(status == Status.unchanged_wallpaper): status_message = "The wallpaper downloaded successfully but could not be set."
    elif(status == Status.failed_download): status_message = "The wallpaper failed to download."
    elif(status == Status.no_suitable_url): status_message = "There were no suitable images that met the search criteria."
    elif(status == Status.bad_arguments): status_message = "The command line arguments were entered incorrectly."
    elif(status == Status.crontab_success): status_message = "A new crontab entry was successfully added."
    elif(status == Status.crontab_failure): status_message = "Failed to add new crontab entry."
    writer.write("Image_URI: %s\tStatus: %s\tDate: %s\tTime: %s\n" % (image_uri,status_message, time.strftime("%m/%d/%y"),time.strftime("%I:%M:%S")))
    writer.close()

if __name__ == '__main__':
    main()