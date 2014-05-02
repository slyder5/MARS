# MARS #
########

# Import #
##########

import os
from settings import *
from modules import *
import logging

# Variables #
#############

# Reads in configuration file
data = config.read_json()

# Checks environment settings
data = config.check_environment(data)

# Logging #
###########

logging.basicConfig(filename="mars.log",level=logging.DEBUG,
					format="%(asctime)s %(levelname)s - %(message)s",
					datefmt="%I:%M:%S %p")
console = logging.StreamHandler()
if data["loglevel"] == "debug":
	console.setLevel(logging.DEBUG)
elif data["loglevel"] == "info":
	console.setLevel(logging.INFO)
else:
	console.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s: %(message)s",datefmt="%I:%M:%S %p")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Functions #
#############

def mars():
	# Screen Formatting
	os.system("cls" if os.name == "nt" else "clear")
	print "MARS - Modular Automated Reddit Script\n"

	# Account Module

	r = account.start(data)

	# Comments Module

	if data["m_comments"] == "1":
		comments.start(data,r)
	elif data["m_comments"] == "0":
		print "This feature not yet implemented"

# Run #
#######

mars()

# EOF