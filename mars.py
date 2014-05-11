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

# Checks environment settings
data = config.check_environment(data)

# Logging #
###########

consoleFormatter = logging.Formatter("%(asctime)s: %(message)s",
										datefmt="%I:%M:%S %p")
fileFormatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s",
									datefmt="%I:%M:%S %p")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
fileHandler = TimedRotatingFileHandler("mars.log",when="midnight",
										backupCount=14)
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

def mars():
	# Screen Formatting
	os.system("cls" if os.name == "nt" else "clear")
	print "MARS - Modular Automated Reddit Script\n"

	# Account Module

	r = account.start(data)
	
	# Commands Module
	
	if data["m_commands"] == "1":
		commands.start(data,r)
	elif data["m_commands"] == "0":
		print "This feature not yet implemented."

	# Comments Module

	if data["m_comments"] == "1":
		comments.start(data,r)
	elif data["m_comments"] == "0":
		print "This feature not yet implemented."

# Run #
#######

mars()

# EOF
