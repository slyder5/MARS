# Login #
#########

# Import

import os
import praw
import logging

# Variables

# Functions

def start(data):
	logging.debug("Starting Module: Account")
	try:
		if data["m_account"] == "1":
			return login(data)
		elif data["m_account"] == "0":
			return readonly(data)
	except:
		logging.warning("Configuration failed - Please run setup")
		raise SystemExit(0)

def login(data):
	r = praw.Reddit(user_agent = data["running_username"])
	try:
		logging.info(data["running_username"] + ": Attempting Login")
		r.login(data["running_username"],data["running_password"])
		logging.info("Login Successful")
	except:
		logigng.info("Login Failed")
		raise SystemExit(0)
	return r

def readonly(data):
	logging.info("Acount Module Disabled - using Read Only mode")
	r = praw.Reddit(user_agent = data["running_username"] + " Read Only mode")
	return r

# EOF