#What is WallpapersUpdater?
Wallpapers Updater is a program that scrapes wallpapers from Reddit.com and sets them as your desktop program.
You can change your wallpaper at any time by running wallpapers.py
Alternatively, you can install wallpapers.py to your crontab to update your wallpapers on a regular basis.
WallpapersUpdater currently only supports Linux Mint, although work is in progress for other Linux distributions.
##How do I install and run WallpapersUpdater?
WallpapersUpdater requires Python2.7, pip, and the following Python packages: praw, enum, argparse, and python-crontab.
To install the dependencies, type the following code into the command line.
'./install.sh'
To install WallpapersUpdater to your crontab with all the default options, type the following:
'python wallpapers.py --install hour
To run WallpapersUpdater one time (get a new wallpaper without scheduling updates), type the following:
python wallpapers.py
##How do I customize WallpapersUpdater?
WallpapersUpdater has a number of customizable features.
To get a summary of these features from the command line type 'python wallpapers.py --help'
* You can choose the directory to save your wallpapers to.
* You can choose the subreddits you wish to download the wallpapers from.
* You can choose the allowed file extensions you wish to allow.
* You can choose if you want to install WallpapersUpdater to your crontab and how often you want your wallpapers to update.
These parameters are read from the command line using Python argparse flags.

An example of how to use these is below.
'python wallpapers.py --savedir ~/Pictures/Wallpapers --subreddits wallpapers minimalwallpaper --extensions .jpg .png --install minute'
This user is saving his wallpapers to his Pictures/Wallpapers directory.
He is downloading wallpapers from http://reddit.com/r/wallpapers and http://reddit.com/r/minimalwallpaper.
He is allowing the .jpg and .png file extensions.
He is setting up his crontab to update his wallpaper every minute.
Of course, leaving any of these flags out is acceptable and will use the program defaults for that option.



