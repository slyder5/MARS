# Comemnts #
############

# Import #
##########

import re
import logging

# Variables #
#############

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

# Comment processing
def process_comments(data,r,sub_comments):
	logging.debug("Processing Comments")
	running_username = str(data["running_username"]).lower()
	logging.debug("Running username is: %s" % running_username)
	for comment in sub_comments: # for each comment in batch
		comment_author = str(comment.author.name).lower()
		if comment_author != running_username: # ignore my own comments
			logging.info("Searching comment by: %s\n%s" % (
				comment.author.name	if comment.author else "[deleted]",
				comment.permalink)) # Shows redditor and permalink
			lines = split_comment(comment.body) # Gets comment lines
			token_found = search_line(data["token"],lines) # Checks for match
			if token_found: # Starts checks when a token is found
				token_comment = comment # Recognized as awarder comment
				awarder = comment_author # Recognized as awarder
				logging.debug("A token was found.")
				awardee_comment = r.get_info(thing_id=token_comment.parent_id)
				awardee = str(awardee_comment.author.name).lower()
				if awardee == running_username: # Prevents reply to bot
					logging.info("User replied to me")
				elif awardee == comment_author: # Prevents reply to self
					logging.info("User replied to self")
				elif check_already_replied(data["msg_confirmation"],
										   token_comment.replies,
										   running_username):
					logging.info("Already Confirmed")
				else:
					optional_checks(data,r,awardee_comment,awardee,
									token_comment,awarder,token_found)

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
					logging.info("Found Delta - Starting Checks")
					return token

# Check to make sure I haven't already replied
def check_already_replied(msg_confirmation,replies,running_username):
	logging.debug("Checking Already Replied")
	for reply in replies:
		if reply.author:
			if str(reply.author.name).lower() == running_username:
				if str(reply.body).lower() == str(msg_confirmation).lower():
					return True

# Optional checks based on configuration
def optional_checks(data,r,awardee_comment,awardee,token_comment,awarder,
					token_found):
	logging.debug("Optional Checks")
	if check_awardee_not_author(data["check_ana"],
								token_comment.submission.author,
								awardee):
		print("\nBad recipient\n")
	elif check_awarder_to_awardee_history(data,r,awardee_comment,awardee,
										  token_comment,awarder):
		print("\nAlready awarded this thread\n")
	elif check_length(data,token_comment.body,token_found):
		print("\nInsufficient length\n")

# Check to ensure submission author is not receiving a delta
def check_awardee_not_author(check_ana,sub_author,awardee):
	if check_ana == "1":
		logging.debug("Checking Awardee Not Author")
		return str(sub_author).lower() == str(awardee).lower()
	elif check_ana == "0":
		logging.debug("Check Recipient Not Author is disabled.")

# Checks to see if the awarder has already awarded the awardee in this thread
def check_awarder_to_awardee_history(data,r,awardee_comment,awardee,
									 token_comment,awarder):
	if data["check_history"] == "1":
		# TREE means it will only search the root comment and all replies
		logging.debug("Checking Awarder to Awardee History - TREE")
		root = awardee_comment
		while not root.is_root: # Move to the top comment
			root = r.get_info(thing_id=root.parent_id)
		if iterate_replies(data,r,root,awardee,awarder):
			logging.info("Delta awarded elsewhere in tree")
			return True
	elif data["check_history"] == "2":
		# FOREST means it will search the entire submission
		logging.debug("Checking Awarder to Awardee History - FOREST")
		print("\nCheck entire submission\n")
	elif data["check_history"] == "0":
		logging.debug("Check Awarder to Awardee History is disabled.")

# Iterates through the comment tree - VERY expensive
def iterate_replies(data,r,comment,awardee,awarder):
	iterate = "Yes"
	logging.debug("Iterating Replies")
	msg_confirmation = data["msg_confirmation"]
	running_username = str(data["running_username"]).lower()
	comments = r.get_submission(comment.permalink).comments
	for comment in comments:
		if iterate == "Yes":
			if check_already_replied(msg_confirmation,comment.replies,
									 running_username):
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
	awarder = str(comment.author.name).lower()
	logging.debug("Awarder: %s" % awarder)
	logging.debug("Original Awarder: %s" % orig_awarder)
	if awarder == orig_awarder:
		return True

# Checks original awardee against recently found awardee
def check_awardee(r,comment,orig_awardee):
	logging.debug("Checking Awardee")
	awardee_comment = r.get_info(thing_id=comment.parent_id)
	awardee = str(awardee_comment.author.name).lower()
	logging.debug("Awardee: %s" % awardee)
	logging.debug("Comment Author: %s" % awardee)
	if awardee == orig_awardee:
		return True

# Check length of comment against minimum requirement
def check_length(data,body,token_found):
		if data["check_length"] == "1":
			logging.debug("Checking Comment Length")
			return len(body) < int(data["min_length"]) + len(token_found)
		elif data["check_length"] == "0":
			logging.debug("Check Comment Length is disabled.")

# EOF