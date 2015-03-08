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

# Reads in the json for the messages
def read_msg_json():
	with open("settings/messages.json","r") as json_msg:
		msg = json.load(json_msg)
	return msg

# COMMANDS MODULE FUNCTIONS
def remind(comment):
	comment.reply(msg["remind"]).distinguish()

def stop(data,msg,r,mail):
	r.send_message("/r/" + data["running_subreddit"],msg["stop_subject"] % data["running_subreddit"],msg["stop_body"] % (data["running_username"],mail.author.name,mail.body))

# COMMENTS MODULE FUNCTIONS
def confirm(data,msg,awardee_comment,awardee):
	confirmation =  msg["confirmation"] % (msg["token"],awardee_comment.author.name,awardee_comment.author.name,msg["token"],data["running_subreddit"],awardee,msg["token"],data["running_subreddit"],data["running_username"])
	return confirmation
	
# EOF
