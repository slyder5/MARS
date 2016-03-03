# encoding: utf-8

# Comments #
############

# Import #
##########

import praw
import logging
import re
import messages

# Functions #
#############

def start_increment(data,msg,r,awardee):
  logging.debug("Starting Module: Token - Increment")
  old_flair,old_count = get_flair(data,msg,r,awardee)
  new_flair,new_count = increment_flair(old_flair,old_count)
  set_flair(data,msg,r,awardee,new_flair)
  return new_count

def start_decrement(data,msg,r,awardee):
  logging.debug("Starting Module: Token - Decrement")
  old_flair,old_count = get_flair(data,msg,r,awardee)
  new_flair,new_count = decrement_flair(old_flair,old_count)
  set_flair(data,msg,r,awardee,new_flair)
  return new_count

def get_flair(data,msg,r,awardee):
  logging.debug("Getting the awardee's flair")
  awardee_flair = r.get_flair(data["running_subreddit"],awardee)
  if awardee_flair["flair_text"] == None:
    logging.debug("New Awardee")
    flair_count = 0
    logging.debug("Getting Congrats Subject")
    congrats_first_subject = messages.congrats_first_subject(msg)
    logging.debug("Getting Congrats Body")
    congrats_first_body = messages.congrats_first_body(data,msg,awardee)
    logging.debug("Sending Congrats Mail")
    r.send_message(awardee,congrats_first_subject,congrats_first_body)
  else:
    flair_count = re.search('(\d+)', awardee_flair["flair_text"])
    if flair_count.group(0):
      flair_count = int(flair_count.group(0))
  return (awardee_flair,flair_count)

def increment_flair(flair,old_count):
  logging.debug("Incrementing the flair")
  token = "\u03BB"
  token = token.decode('unicode-escape')
  new_count = old_count + 1
  flair["flair_text"] = str(new_count) + token
  return (flair,new_count)

def decrement_flair(flair,old_count):
  logging.debug("Decrementing the flair")
  token = "\u03BB"
  token = token.decode('unicode-escape')
  if old_count > 0:
    new_count = old_count - 1
  flair["flair_text"] = str(new_count) + token
  return (flair,new_count)

def set_flair(data,msg,r,awardee,awardee_flair):
  logging.debug("Setting the awardee's new flair")
  r.set_flair(data["running_subreddit"],awardee,awardee_flair["flair_text"])

# EOF
