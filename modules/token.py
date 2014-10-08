# encoding: utf-8

# Comments #
############

# Import #
##########

import praw
import logging

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
    awardee_flair["flair_text"] = "1∆",
    print awardee_flair["flair_text"]
    return awardee_flair
  else:
    print("This user has more than no flair.")

def set_flair(data,r,awardee,awardee_flair):
  logging.debug("Setting the awardee's new flair")
  r.set_flair(data["running_subreddit"],awardee,awardee_flair["flair_text"])

# EOF
