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
	logging.debug("Getting subreddit")
	return r.get_subreddit(sub_name)

# Gets the newest comments from the subreddit
def sub_get_comments(subreddit):
	logging.debug("Getting comments")
	return subreddit.get_comments(limit=3) # Limits comments retrieved

# Comment processing
def process_comments(data,r,sub_comments):
	running_username = str(data["running_username"]).lower()
	for comment in sub_comments: # for each comment in batch
		comment_author = str(comment.author.name).lower()
		if comment_author != running_username: # ignore my own comments
			logging.info("Searching comment by: %s\n%s" % (
				comment.author.name	if comment.author else "[deleted]",
				comment.permalink)) # Shows redditor and permalink
			lines = split_comment(comment.body) # Gets comment lines
			token_found = search_line(data["token"],lines) # Checks for match
			if token_found: # Starts checks when a token is found
				parent_comment = r.get_info(thing_id=comment.parent_id)
				parent_author = str(parent_comment.author.name).lower()
				if parent_author == running_username: # Prevents reply to bot
					logging.info("User replied to me")
				elif parent_author == comment_author: # Prevents reply to self
					logging.info("User replied to self")
				elif check_already_replied(data["msg_confirmation"],
										   comment.replies,running_username):
					logging.info("Already confirmed")
				else:
					optional_checks(data,r,parent_comment,comment,token_found)

# Splits comments into lines for more thorough processing
def split_comment(body):
	return body.split("\n\n")

# Search comment for symbol token
def search_line(data_token,lines):
	for line in lines:
		if re.match("(    |&gt;)",line) is None: # Don't look in code or quotes
			for token in data_token: # Check each type of token
				if token in line:
					logging.info("Found Delta - Starting Checks")
					return token


# Check to make sure I haven't already replied
def check_already_replied(msg_confirmation,replies,running_username):
	for reply in replies:
		#print(vars(reply))
		print(reply)
		if reply.author:
			if str(reply.author.name).lower() == running_username:
				if str(reply.body).lower() == str(msg_confirmation).lower():
					return True

# Optional checks based on configuration
def optional_checks(data,r,parent_comment,comment,token_found):
	if check_awardee_not_author(data["check_ana"],
								comment.submission.author,
								parent_comment.author):
		print("\nBad recipient\n")
	elif check_awarder_to_awardee_history(data,r,parent_comment,comment):
		print("\nAlready awarded this thread\n")
	elif check_length(data,comment.body,token_found):
		print("\nInsufficient length\n")

# Check to ensure submission author is not receiving a delta
def check_awardee_not_author(check_ana,sub_author,parent_author):
	if check_ana == "1":
		logging.debug("Checking awardee not author")
		return str(sub_author).lower() == str(parent_author).lower()
	elif check_ana == "0":
		logging.debug("Check recipient not author is disabled.")

# Checks to see if the awarder has already awarded the awardee in this thread
def check_awarder_to_awardee_history(data,r,parent_comment,comment):
	if data["check_history"] == "1":
		logging.debug("Checking awarder to awardee history - TREE")
		comment_author = str(comment.author.name).lower()
		while not parent_comment.is_root:
			parent_comment = r.get_info(thing_id=parent_comment.parent_id)
		if iterate_replies(data,r,parent_comment,comment_author):
			print("Delta awarded elsewhere in tree")
	elif data["check_history"] == "2":
		logging.debug("Checking awarder to awardee history - FOREST")
		print("\nCheck entire submission\n")
	elif data["check_history"] == "0":
		logging.debug("Check awarder to awardee history is disabled.")

# Iterates through the comment tree - VERY expensive
def iterate_replies(data,r,comment,comment_author):
	msg_confirmation = data["msg_confirmation"]
	running_username = str(data["running_username"]).lower()
	comments = r.get_submission(comment.permalink).comments
	for comment in comments:
		if check_already_replied(msg_confirmation,comment.replies,
								 running_username):
			if check_parent(r,comment,comment_author):
				return True
			#print("Already awarded elsewhere in chain.")
		for reply in comment.replies:
			iterate_replies(data,r,reply,comment_author)

def check_parent(r,comment,comment_author):
	parent_comment = r.get_info(thing_id=comment.parent_id)
	parent_author = str(parent_comment.author.name).lower()
	if parent_author == comment_author:
		return True
# Check length of comment against minimum requirement
def check_length(data,body,token_found):
		if data["check_length"] == "1":
			logging.debug("Checking comment length")
			return len(body) < int(data["min_length"]) + len(token_found)
		elif data["check_length"] == "0":
			logging.debug("Check comment length is disabled.")

# EOF