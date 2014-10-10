# encoding: utf-8

# MARS #
########

# Import #
##########

import os
from settings import *
from modules import *
import logging
from logging.handlers import TimedRotatingFileHandler

# Variables #
#############

# Reads in configuration file
data = config.read_json()

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
if data["loglevel"] == "debug":
	consoleHandler.setLevel(logging.DEBUG)
elif data["loglevel"] == "info":
	consoleHandler.setLevel(logging.INFO)
else:
	consoleHandler.setLevel(logging.WARNING)
consoleHandler.setFormatter(consoleFormatter)
rootLogger.addHandler(consoleHandler)

# Functions #
#############

r = account.start(data)
link = "http://www.reddit.com/r/PixelOrange/comments/2iqwgh/mars_test_thread_october/cl4m2jt"
token_comment = r.get_submission(link).comments
for comment in token_comment:
	print comment.author
	wiki.start(data,r,comment,"Awarder","pixeltest1","1111")

# EOF
