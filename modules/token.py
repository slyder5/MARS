# Comments #
############

# Import #
##########

import praw
import logging

# Functions #
#############

def get_flair(data,r,awardee):
  awardee_flair = r.get_flair(data["running_subreddit"],awardee)
  print(awardee_flair)
