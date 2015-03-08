# Messages #
############

# Import

import praw
import json
import logging
import time

# Variables

# Functions

def start():
  msg = read_msg_json()

def read_msg_json():
	with open("settings/messages.json","r") as json_msg:
		msg = json.load(json_msg)
	return msg
