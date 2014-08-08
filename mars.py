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

	# First Time Setup
	if data["initialize"]:
		if data["initialize"] == 0:
			ui.start(data)
		else:
			condition = True
			while condition:
				reset = raw_input("Do you wish to run setup (yes/no)? ")
				if reset == "yes":
					condition = False
					ui.start(data)
				elif reset == "no":
					condition = False
				else:
					print("Please type yes or no.\n")
	else:
		ui.start(data)

	# Checks environment settings
	condition = True
	while condition:
		env = raw_input("Do you wish to run the script in prod or test? ")
		if env == "prod" or env == "test":
			data["environment"] = env
			condition = False
		else:
			print("Please enter prod or test.\n")
	data = config.check_environment(data)

	# Account Module
	r = account.start(data)
	
	# Commands Module
	commands.start(data,r)

	# Comments Module
	comments.start(data,r)

# Run #
#######

mars(data)

# EOF
