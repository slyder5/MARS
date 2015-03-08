# Messages #
############

# Import

import praw
import json
import logging
import time

# Variables

# Functions

def read_msg_json():
	with open("settings/messages.json","r") as json_msg:
		msg = json.load(json_msg)
	return msg

def remind():
	logging.debug("Not Ready")

def add():
	logging.debug("Not Ready")

def approve():
	logging.debug("Not Ready")

def force_add():
	logging.debug("Not Ready")

def remove():
	logging.debug("Not Ready")

def stop():
	logging.debug("Not Ready")

# EOF
