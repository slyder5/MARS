# Comments #
############

# Import #
##########

import re
import logging
import token
from pprint import pprint 

# Functions #
#############

# Starts the comments module
def start(data,r):
	logging.debug("Starting Module: Comments")
	subreddit = get_sub(r,data["running_subreddit"]) # gets subreddit object
	sub_comments = sub_get_comments(subreddit) # gets x comments from sub
	process_comments(data,r,sub_comments) # processes the comments

# Gets subreddit object from reddit
def get_sub(r,sub_name):
	logging.debug("Getting Subreddit")
	return r.get_subreddit(sub_name)

# Gets the newest comments from the subreddit
def sub_get_comments(subreddit):
	logging.debug("Getting Comments")
	return subreddit.get_comments(limit=1) # Limits comments retrieved

# Comment Processing
def process_comments(data,r,sub_comments):
	logging.debug("Processing Comments")
	running_username = str(data["running_username"]).lower()
	logging.debug("Running username is: %s" % running_username)
	for comment in sub_comments: # for each comment in batch
		if not comment.banned_by: # Ignores removed comments
			comment_author = str(comment.author.name).lower()
			if comment_author != running_username: # Ignore my own comments
				logging.info("Searching comment by: %s\n%s" % (comment.author.name
					if comment.author else "[deleted]",comment.permalink)) # Shows redditor and permalink
				lines = split_comment(comment.body) # Gets comment lines
				token_found = search_line(data["token"],lines) # Checks for match
				if token_found: # Starts checks when a token is found
					logging.debug("A token was found.")
					start_checks(data,r,comment,token_found)
				else:
					logging.info("No token found.")
			else:
				logging.debug("Comment found was my own.")
			if comment_author == str(comment.submission.author).lower():
				print("Placeholder: Change Submission Flair")
		else:
			logging.debug("This comment was removed by a mod and has not been scanned.")

# Starts Checks
def start_checks(data,r,token_comment,token_found):
	logging.debug("Starting Checks")
	running_username = str(data["running_username"]).lower()
	awarder = str(token_comment.author.name).lower()
	awardee_comment = r.get_info(thing_id=token_comment.parent_id)
	if awardee_comment.author:
		awardee = str(awardee_comment.author.name).lower()
		if awardee == running_username: # Prevents reply to bot
			logging.info("User replied to me")
		elif awardee == awarder: # Prevents reply to self
			logging.info("User replied to self")
		elif check_already_replied(data,data["msg_confirmation"],token_comment.replies,running_username) == :
			logging.info("Already Confirmed")
		else:
			optional_checks(data,r,token_comment,awarder,awardee_comment,awardee,token_found)
	else:
		logging.info("Unable to award token to deleted comment")

# Splits comments into lines for more thorough processing
def split_comment(body):
	logging.debug("Splitting Comment Body")
	return body.split("\n\n") # Splits double line breaks

# Search comment for symbol token
def search_line(data_token,lines):
	logging.debug("Searching Line For Token")
	for line in lines:
		if re.match("(    |&gt;)",line) is None: # Don't look in code or quotes
			for token in data_token: # Check each type of token
				if token in line:
					logging.info("Found Token - Starting Checks")
					return token

# Check to make sure I haven't already replied
def check_already_replied(data,msg,replies,running_username):
	logging.debug("Checking Already Replied")
	for reply in replies:
		if reply.author:
			if str(reply.author.name).lower() == running_username:
				if str(reply.body).lower() == str(msg).lower():
					return True
					

# Check to make sure I haven't already replied (remind version)
def remind_already_replied(data,msg,replies,running_username):
	logging.debug("Checking Already Replied - Remind Version")
	for reply in replies:
		if reply.author:
			if str(reply.author.name).lower() == running_username:
				body = str(reply.body).lower()
				if body == str(msg).lower():
					logging.debug("Reply message to message match")
					return ("match",reply)
				elif body == str(data["msg_confirmation"]).lower():
					logging.debug("Message confirmation match")
					return ("confirm",reply)
				elif body == str(data["error_bad_recipient"]).lower():
					logging.debug("Error bad recipient match")
					return ("error",reply)
				elif body == str(data["error_submission_history"]).lower():
					logging.debug("Error submission history match")
					return ("error",reply)
				else:
					logging.debug("Unspecified match")
					return ("other",reply)

# Optional checks based on configuration
def optional_checks(data,r,token_comment,awarder,awardee_comment,awardee,token_found):
	logging.debug("Optional Checks")
	if check_awardee_not_author(data["check_ana"],token_comment.submission.author,awardee):
		print("\nBad recipient\n")
	elif check_awarder_to_awardee_history(data,r,awardee_comment,awardee,token_comment,awarder):
		print("\nAlready awarded this thread\n")
	elif check_length(data,token_comment.body,token_found):
		print("\nInsufficient length\n")
	else:
		logging.debug("Token Valid - Beginning Award Process")
		token.start_increment(data,r,awardee)
		token_comment.reply(data["msg_confirmation"] % (awardee,data["running_subreddit"],awardee))
		logging.info("Confirmation Message Sent")

# Check to ensure submission author is not receiving a token
def check_awardee_not_author(check_ana,sub_author,awardee):
	if check_ana == "1":
		logging.debug("Checking Awardee Not Author")
		return str(sub_author).lower() == str(awardee).lower()
	elif check_ana == "0":
		logging.debug("Check Recipient Not Author is disabled.")

# Checks to see if the awarder has already awarded the awardee in this thread
def check_awarder_to_awardee_history(data,r,awardee_comment,awardee,token_comment,awarder):
	if data["check_history"] == "1":
		# TREE means it will only search the root comment and all replies
		logging.debug("Checking Awarder to Awardee History - TREE")
		root = awardee_comment
		while not root.is_root: # Move to the top comment
			root = r.get_info(thing_id=root.parent_id)
		if iterate_replies(data,r,root,awardee,awarder):
			logging.info("Token awarded elsewhere in tree")
			return True
	elif data["check_history"] == "2":
		# FOREST means it will search the entire submission
		logging.debug("Checking Awarder to Awardee History - FOREST")
		print("Placeholder: Check entire submission")
	elif data["check_history"] == "0":
		logging.debug("Check Awarder to Awardee History is disabled.")

# Iterates through the comment tree - VERY expensive
def iterate_replies(data,r,comment,awardee,awarder):
	logging.debug("Iterating Replies")
	iterate = "Yes"
	msg_confirmation = data["msg_confirmation"]
	running_username = str(data["running_username"]).lower()
	comments = r.get_submission(comment.permalink).comments
	for comment in comments:
		if iterate == "Yes":
			if check_already_replied(data,msg_confirmation,comment.replies,running_username):
				if check_awarder(r,comment,awarder):
					if check_awardee(r,comment,awardee):
						iterate = "No"
						return iterate
			for reply in comment.replies:
				iterate = iterate_replies(data,r,reply,awardee,awarder)
				if iterate == "No":
					return iterate
		elif iterate == "No":
			# Not sure this is ever called
			print("Comment NoIteration Called - Remove this line and comment")
			return iterate

# Checks original awarder against recently found awarder
def check_awarder(r,comment,orig_awarder):
	logging.debug("Checking Awarder")
	if comment.author:
		awarder = str(comment.author.name).lower()
	else:
		awarder = "[deleted]"
	if awarder == orig_awarder:
		return True

# Checks original awardee against recently found awardee
def check_awardee(r,comment,orig_awardee):
	logging.debug("Checking Awardee")
	awardee_comment = r.get_info(thing_id=comment.parent_id)
	if awardee_comment.author:
		awardee = str(awardee_comment.author.name).lower()
	else:
		awardee = "[deleted]"
	if awardee == orig_awardee:
		return True

# Check length of comment against minimum requirement
def check_length(data,body,token_found):
	if data["check_length"] == "1":
		logging.debug("Checking Comment Length")
		if token_found != "force":
			return len(body) < int(data["min_length"]) + len(token_found)
	elif data["check_length"] == "0":
		logging.debug("Check Comment Length is disabled.")

# EOF
