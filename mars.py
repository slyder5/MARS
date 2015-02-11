# encoding: utf-8

# MARS #
########

# Import #
##########

import os
import time
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
fileHandler = TimedRotatingFileHandler("mars.log",when="midnight",backupCount=14)
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

def mars(data):
	# Screen Formatting
	os.system("cls" if os.name == "nt" else "clear")
	print "MARS - Modular Automated Reddit Script\n"

	data["environment"] = "prod"
	data = config.check_environment(data)
	
	# Account Module
	r = account.start(data)
	
	run = True
	while run:
		# Commands Module
		commands.start(data,r)

		# Comments Module
		comments.start(data,r)
		
		# Wait 10 seconds
		wait_time = 10
		logging.info("Sleeping for %s seconds" % wait_time)
		time.sleep(wait_time)

# Run #
#######

mars(data)

# EOF
