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
  logging.debug("Starting Module: Token")
  awardee_flair = get_flair(data,r,awardee)
  set_flair(data,r,awardee,awardee_flair)

def get_flair(data,r,awardee):
  logging.debug("Getting the awardee's flair")
  awardee_flair = r.get_flair(data["running_subreddit"],awardee)
  if awardee_flair["flair_text"] == None:
    awardee_flair["flair_text"] = "1∆"
    logging.debug(awardee_flair["flair_text"])
    return awardee_flair
  else:
    flair_count = re.search('(\d+)', awardee_flair["flair_text"])
    flair_count = int(flair_count.group(0))
    logging.debug(flair_count)
    flair_count = flair_count + 1
    awardee_flair["flair_text"] = str(flair_count) + "∆"
    logging.debug(awardee_flair["flair_text"])
    return awardee_flair

def set_flair(data,r,awardee,awardee_flair):
  logging.debug("Setting the awardee's new flair")
  r.set_flair(data["running_subreddit"],awardee,awardee_flair["flair_text"])

# EOF
