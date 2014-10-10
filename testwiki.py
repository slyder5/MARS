# encoding: utf-8

# Import #
##########

import logging
from modules import account
from modules import wiki
from logging.handlers import TimedRotatingFileHandler

# Variables #
#############

data = {}
data["running_subreddit"] = "PixelOrange"
data["running_username"] = "pixelsbot"
data["running_password"] = "PixelOrange"
data["m_account"] = "1"
r = account.start(data)
link = "http://www.reddit.com/r/PixelOrange/comments/2iqwgh/mars_test_thread_october/cl4m2jt"

# Logging #
###########

consoleFormatter = logging.Formatter("%(asctime)s: %(message)s",datefmt="%I:%M:%S %p")
fileFormatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s",datefmt="%I:%M:%S %p")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
fileHandler = TimedRotatingFileHandler("testwiki.log",when="midnight",backupCount=14)
fileHandler.setFormatter(fileFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(consoleFormatter)
rootLogger.addHandler(consoleHandler)

# Functions #
#############

token_comment = r.get_submission(link).comments
for comment in token_comment:
  print comment.author
  wiki.start(data,r,comment,"Awarder","pixeltest1","2")

# EOF
