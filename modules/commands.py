# Commands #
############

# Import #
##########

import praw
import logging

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
	mailbox = r.get_unread(unset_has_mail=True,update_user=True)
	for mail in mailbox:
		if type(mail) == praw.objects.Message: # Bot received mail
			print("You've got mail.")
			read_mail(data,r,mail)
		if type(mail) == praw.objects.Comment: # Someone replied to bot
			print("Someone replied to you! How nice!!!")
			read_comment_reply(mail)
		mail.mark_as_read() # Marks mail as read

# Reads the mail
def read_mail(data,r,mail):
	logging.info("Reading mail from %s" % mail.author.name)
	command = mail.subject.lower()
	logging.info("Subject: %s" % command)
	if command == "force add": # Force add skips token check
		force_add(data,r,mail)
	elif command == "add": # The same as if the bot found the comment itself
		print("Do them add checks")
	elif command == "remind": # Useful for reminding redditors about deltas
		print("Do them reminders")
	elif command == "rescan": # Rescans a previously scanned comment
		print("Do them rescans")
	elif command == "reset": # Resets bot's scanned comments
		print("Reset the bot's scanned comments")
	elif command == "stop": # Stops bot
		if is_moderator(data,r,mail.author.name):
			r.send_message("/r/" + data["running_subreddit"],
							data["msg_stop_subject"],data["msg_stop_body"])
			logging.warning(data["msg_stop_warning"])
			mail.mark_as_read()
			raise SystemExit(0)
		else:
			logging.warning("Non-mod tried using a mod command.")

def force_add(data,r,mail):
	if is_moderator(data,r,mail.author.name):
		separate_mail(mail.body)
	else:
		logging.warning("Non-mod tried using a mod command.")

def is_moderator(data,r,name):
	logging.debug("Comparing User to Moderators")
	moderators = r.get_moderators(data["running_subreddit"])
	mod_names = [mod.name for mod in moderators]
	return name in mod_names

def separate_mail(body):
	logging.debug("Separating Mail")
	return body.split("\n")

# EOF
