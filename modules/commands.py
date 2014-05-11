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

def start(data,r):
	logging.debug("Starting Module - Commands")
	check_mailbox(data,r)

def check_mailbox(data,r):
	mailbox = r.get_unread(unset_has_mail=True,update_user=True)
	for mail in mailbox:
		if type(mail) == praw.objects.Message:
			print("You've got mail.")
			read_mail(data,r,mail)
		if type(mail) == praw.objects.Comment:
			print("Someone replied to you! How nice!!!")
			read_comment_reply(mail)
		mail.mark_as_read()

def read_mail(data,r,mail):
	logging.info("Reading mail from %s" % mail.author.name)
	command = mail.subject.lower()
	logging.info("Subject: %s" % command)
	if command == "force add":
		print("Do them force adds")
	elif command == "add":
		print("Do them add checks")
	elif command == "remind":
		print("Do them reminders")
	elif command == "rescan":
		print("Do them rescans")
	elif command == "reset":
		print("Reset the bot's scanned comments")
	elif command == "stop":
		if is_moderator(data,r,mail.author.name):
			r.send_message("/r/" + data["running_subreddit"],
							data["msg_stop_subject"],data["msg_stop_body"])
			logging.warning(data["msg_stop_warning"])
			mail.mark_as_read()
			raise SystemExit(0)
		else:
			logging.warning("Non-mod tried using a mod command.")

def is_moderator(data,r,name):
	moderators = r.get_moderators(data["running_subreddit"])
	mod_names = [mod.name for mod in moderators]
	return name in mod_names

# EOF