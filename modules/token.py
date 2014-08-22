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
  get_flair(data,r,awardee)

def get_flair(data,r,awardee)
  awardee_flair = r.get_flair(data["running_subreddit"],awardee)
  print(awardee_flair)
