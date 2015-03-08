# Commands #
############

# Import #
##########

import praw
import logging
import comments
import token
import wiki
import messages
from settings import config
from pprint import pprint
import time

# Variables #
#############

# Functions #
#############

# Starts the commands module
def start(data,msg,r):
	logging.debug("Starting Module: Commands")
	check_mailbox(data,msg,r)

# Checking the mailbox for mail
def check_mailbox(data,msg,r):
	logging.debug("Checking Mailbox")
	mailbox = r.get_unread(unset_has_mail=True,update_user=True)
	for mail in mailbox:
		if type(mail) == praw.objects.Message: # Bot received mail
			logging.info("I've got mail.")
			read_mail(data,msg,r,mail)
		if type(mail) == praw.objects.Comment: # Someone replied to bot
			logging.info("Someone replied to me.")
			read_comment_reply(data,msg,r,mail)
		mail.mark_as_read() # Marks mail as read

# Reads the mail
def read_mail(data,msg,r,mail):
	logging.info("Reading mail from %s" % mail.author.name)
	command = mail.subject.lower()
	logging.info("Subject: %s" % command)
	if command == "remind": # Useful for reminding redditors about tokens
		remind(data,msg,r,mail)
	elif command == "add": # The same as if the bot found the comment itself
		add(data,msg,r,mail)
	elif command == "rescan": # Same functionality as add
		add(data,msg,r,mail)
	elif is_moderator(data,msg,r,mail.author.name): 
		if command == "approve": # Approves token in queue
			approve(data,msg,r,mail)
		elif command == "force add": # Force add skips token check
			force_add(data,msg,r,mail)
		elif command == "reset": # Resets bot's scanned comments
			reset(data)
		elif command == "remove low effort": # Removes token from user
			remove(data,msg,r,mail,msg["remove_low_effort"])
		elif command == "remove remind": # Removes token from user
			remove(data,msg,r,mail,msg["remove_remind"])
		elif command == "remove abuse": # Removes token from user
			remove(data,msg,r,mail,msg["remove_abuse"])
		elif command == "stop": # Stops bot
			stop(data,msg,r,mail)

# Reminds users how to use the token system
def remind(data,msg,r,mail):
	logging.debug("Remind Command")
	running_username = str(data["running_username"]).lower()
	reminder = True
	lines = separate_mail(mail.body)
	for line in lines:
		links = r.get_submission(line).comments
		for comment in links:
			if comment.replies:
				if comments.check_already_replied(data,msg["confirmation"],comment.replies,running_username):
					logging.info("Already Confirmed")
					reminder = False
				elif comments.check_already_replied(data,msg["error_length"],comment.replies,running_username):
					if comment.edited:
						comments.process_comments(data,msg,r,links)
						reminder = False
				elif comments.check_already_replied(data,msg["error_bad_recipient"],comment.replies,running_username):
					logging.info("Already Notified - Bad Recipient")
					reminder = False
				elif comments.check_already_replied(data,msg["error_submission_history"],comment.replies,running_username):
					logging.info("Already Notified - Submission History Error")
					reminder = False
				elif comments.check_already_replied(data,msg["remind"],comment.replies,running_username):
					logging.info("Already Reminded")
					reminder = False
		wait()
	if reminder:
		for comment in links:
			if comment.author:
				if str(comment.author.name).lower() != str(data["running_username"]).lower():
					logging.info("User has been sent a reminder.")
					messages.remind(comment)
					#comment.reply(msg["remind"]).distinguish()
				else:
					logging.info("Silly person tried to remind me how to do my job.")

# Checks comment for token - Same functionality as if bot found the token itself
def add(data,msg,r,mail):
	logging.debug("Add Command")
	proceed = True
	lines = separate_mail(mail.body)
	for line in lines:
		try:
			links = r.get_submission(line).comments
			proceed = True
		except:
			logging.error("No Link Found in: %s" % line)
			proceed = False
		if proceed == True:
			comments.process_comments(data,msg,r,links)
			wait()
	r.send_message(mail.author.name,"Add Complete","The Add command has been completed for:\n\n%s" % mail.body)

# Checks to see if user is a moderator
def is_moderator(data,msg,r,name):
	logging.debug("Comparing User to Moderators")
	name = str(name).lower()
	moderators = r.get_moderators(data["running_subreddit"])
	for mod in moderators:
		mod = str(mod).lower()
		if mod == name:
			return True

def approve(data,msg,r,mail):
	logging.debug("Approve Command")
	lines = separate_mail(mail.body)
	for line in lines:
		wiki.remove_queue_line(data,msg,r,line)
		wait()

# Forces award (skips token check and length check)
def force_add(data,msg,r,mail):
	logging.warning("Force Add Command")
	proceed = True
	lines = separate_mail(mail.body)
	for line in lines:
		try:
			links = r.get_submission(line).comments
			proceed = True
		except:
			logging.error("No Link Found in: %s" % line)
			proceed = False
		if proceed == True:
			for comment in links:
				token_found = "force"
				comments.start_checks(data,msg,r,comment,token_found)
				wait()
	r.send_message("/r/" + data["running_subreddit"],"Force Add Detected","Force Add from %s detected on:\n\n%s" % (mail.author.name,mail.body))

# Resets last scanned comment
def reset(data):
	comment.clear_history()

# Removes token from flair, wiki, scoreboard, and removes confirmation comment
def remove(data,msg,r,mail,message):
	logging.warning("Remove Command")
	lines = separate_mail(mail.body)
	username = str(data["running_username"]).lower()
	for line in lines:
		links = r.get_submission(line).comments
		for comment in links:
			if comments.check_already_replied(data,msg["confirmation"],comment.replies,username):
				for reply in comment.replies:
					if reply.author:
						if str(reply.author.name).lower() == username:
							reply.delete()
				awardee_comment = r.get_info(thing_id=comment.parent_id)
				if awardee_comment.author:
					awardee = str(awardee_comment.author.name).lower()
					flair_count = token.start_decrement(data,msg,r,awardee)
					wiki.remove_wiki_line(data,msg,r,comment.permalink,awardee,flair_count)
				messages.remove(message)
				# comment.reply(message).distinguish()
				comment.unsave()
				comment.remove(spam=False)
				wiki.remove_queue_line(data,msg,r,line)
				print("Placeholder: Remove text from scoreboard")
			else:
				logging.warning("No token to remove.")
		wait()
	r.send_message("/r/" + data["running_subreddit"],"Remove Detected","Remove from %s detected on:\n\n%s" % (mail.author.name,mail.body))

# Stops bot
def stop(data,msg,r,mail):
	logging.warning(msg["stop_warning"] % data["running_username"])
	messages.stop(data,msg,r,mail)
	#r.send_message("/r/" + data["running_subreddit"],msg["stop_subject"],msg["stop_body"] % (mail.author.name,mail.body))
	mail.mark_as_read()
	raise SystemExit(0)

# Separates the mail for processing
def separate_mail(body):
	logging.debug("Separating Mail")
	return body.split("\n")

# Reads the comment replies
def read_comment_reply(data,msg,r,mail):
	logging.debug("Reading the reply to my comment.")
	bots_comment = r.get_info(thing_id=mail.parent_id)
	orig_comment = r.get_info(thing_id=bots_comment.parent_id)
	link = r.get_submission(orig_comment.permalink).comments
	if str(msg["confirmation"]).lower()[0:15] not in str(bots_comment.body).lower():
		logging.debug("Rescanning Comment")
		comments.process_comments(data,msg,r,link)
	else:
		logging.debug("This comment did not need rescanned.")

def wait():
	wait_time = 35
	logging.debug("Sleeping for %s seconds to clear cache" % wait_time)
	time.sleep(wait_time)

# EOF
