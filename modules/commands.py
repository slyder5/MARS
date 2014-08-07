# Commands #
############

# Import #
##########

import praw
import logging
import comments
from settings import config
from pprint import pprint

# Variables #
#############

# Functions #
#############

# Starts the commands module
def start(data,r):
	logging.debug("Starting Module - Commands")
	check_mailbox(data,r)

# Checking the mailbox for mail
def check_mailbox(data,r):
	logging.debug("Checking Mailbox")
	mailbox = r.get_unread(unset_has_mail=True,update_user=True)
	for mail in mailbox:
		if type(mail) == praw.objects.Message: # Bot received mail
			logging.info("You've got mail.")
			read_mail(data,r,mail)
		if type(mail) == praw.objects.Comment: # Someone replied to bot
			logging.info("Someone replied to you.")
			read_comment_reply(data,r,mail)
		mail.mark_as_read() # Marks mail as read

# Reads the mail
def read_mail(data,r,mail):
	logging.info("Reading mail from %s" % mail.author.name)
	command = mail.subject.lower()
	logging.info("Subject: %s" % command)
	if command == "remind": # Useful for reminding redditors about tokens
		remind(data,r,mail)
	elif command == "add": # The same as if the bot found the comment itself
		add(data,r,mail)
	elif command == "rescan": # Same functionality as add
		add(data,r,mail)
	elif is_moderator(data,r,mail.author.name): 
		if command == "force add": # Force add skips token check
			force_add(data,r,mail)
		elif command == "reset": # Resets bot's scanned comments
			reset(data)
		elif command == "delete": # Deletes token from user
			delete(data,r,mail)
		elif command == "stop": # Stops bot
			stop(data,r,mail)

# Reminds users how to use the token system
def remind(data,r,mail):
	logging.debug("Remind Command")
	reminder = True
	lines = separate_mail(mail.body)
	for line in lines:
		links = r.get_submission(line).comments
		for comment in links:
			is_match,is_reply = comments.check_already_replied(data,data["msg_remind"],comment.replies,
									str(data["running_username"]).lower())
			if is_match == "match":
				logging.info("Reminder found: Ignoring request.")
				reminder = False
			elif is_match == "confirm":
				logging.info("Found a confirmation. Reminder not needed.")
				reminder = False
			elif is_match == "error":
				logging.info("Found an error. Reminder not needed.")
				reminder = False
			elif is_match:
				logging.info("Found an old comment I can edit.")
				reminder = False
				is_reply.edit(data["msg_remind"])
				logging.info("Edited comment and left the reminder.")
	if reminder:
		for comment in links:
			if comment.author:
				if str(comment.author.name).lower() != str(data["running_username"]).lower():
					logging.info("User has been sent a reminder.")
					comment.reply(data["msg_remind"])
				else:
					logging.info("Silly person tried to remind me how to do my job.")

# Checks comment for token - Same functionality as if bot found the token itself
def add(data,r,mail):
	logging.debug("Add Command")
	lines = separate_mail(mail.body)
	for line in lines:
		links = r.get_submission(line).comments
		comments.process_comments(data,r,links)

# Checks to see if user is a moderator
def is_moderator(data,r,name):
	logging.debug("Comparing User to Moderators")
	name = str(name).lower()
	moderators = r.get_moderators(data["running_subreddit"])
	for mod in moderators:
		mod = str(mod).lower()
		if mod == name:
			return True

# Forces award (skips token check and length check)
def force_add(data,r,mail):
	logging.warning("Force Add Command")
	lines = separate_mail(mail.body)
	for line in lines:
		links = r.get_submission(line).comments
		for comment in links:
			token_found = "strict"
			comments.start_checks(data,r,comment,token_found)

# Resets last scanned comment
def reset(data):
	logging.debug("Reset Command")
	data["last_scanned"] = ""
	config.write_json(data)

# Removes token from flair, wiki, scoreboard, and removes confirmation comment
def delete(data,r,mail):
	logging.warning("Delete Command")
	match_options = ["match","confirm"]
	lines = separate_mail(mail.body)
	for line in lines:
		links = r.get_submission(line).comments
		for comment in links:
			is_match,is_reply = comments.check_already_replied(data,data["msg_confirmation"],comment.replies,
									str(data["running_username"]).lower())
			if is_match in match_options:
				is_reply.delete()
			else:
				logging.warning("No token to delete.")

# Stops bot
def stop(data,r,mail):
	logging.warning(data["stop_warning"])
	r.send_message("/r/" + data["running_subreddit"],data["stop_subject"],data["stop_body"])
	mail.mark_as_read()
	raise SystemExit(0)

# Separates the mail for processing
def separate_mail(body):
	logging.debug("Separating Mail")
	return body.split("\n")

# Reads the comment replies
def read_comment_reply(data,r,mail):
	logging.debug("Reading the reply to my comment.")
	print("Placeholder: Read comment reply")

# EOF
