# encoding: utf-8

# Comments #
############

# Import #
##########

import praw
import logging
import re

# Functions #
#############

def start_increment(data,r,awardee):
  logging.debug("Starting Module: Token - Increment")
  old_flair,old_count = get_flair(data,r,awardee)
  new_flair,new_count = increment_flair(old_count)
  set_flair(data,r,awardee,new_flair)
  return new_count

def start_decrement(data,r,awardee):
  logging.debug("Starting Module: Token - Decrement")
  old_flair,old_count = get_flair(data,r,awardee)
  new_flair,new_count = decrement_flair(old_count)
  set_flair(data,r,awardee,new_flair)
  return new_count

def get_flair(data,r,awardee):
  logging.debug("Getting the awardee's flair")
  awardee_flair = r.get_flair(data["running_subreddit"],awardee)
  if awardee_flair["flair_text"] == None:
    flair_count = 0
  else:
    flair_count = re.search('(\d+)', awardee_flair["flair_text"])
    if flair_count.group(0):
      flair_count = int(flair_count.group(0))
  return (awardee_flair,flair_count)

def increment_flair(flair_count):
  logging.debug("Incrementing the flair")
  flair_count = flair_count + 1
  awardee_flair["flair_text"] = str(flair_count) + "∆"
  return (awardee_flair,flair_count)

def decrement_flair(flair_count):
  logging.debug("Decrementing the flair")
  if flair_count > 0:
    flair_count = flair_count - 1
  awardee_flair["flair_text"] = str(flair_count) + "∆"
  return (awardee_flair,flair_count)

def set_flair(data,r,awardee,awardee_flair):
  logging.debug("Setting the awardee's new flair")
  r.set_flair(data["running_subreddit"],awardee,awardee_flair["flair_text"])

# EOF
