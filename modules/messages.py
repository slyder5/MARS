# Messages #
############

# Import

import praw
import json
import logging
import time

# VARIABLES LEGEND
#
# Use this section to build your messages. You want the information AFTER the equal sign (=) to put in your messages.
#
# subreddit = data["running_subreddit"]
# username = data["running_username"]
# 

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

def stop(data,msg,r,mail):
	r.send_message("/r/" + data["running_subreddit"],msg["stop_subject"] % data["running_subreddit"],msg["stop_body"] % (mail.author.name,mail.body))
	
# EOF
