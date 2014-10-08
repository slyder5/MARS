# encoding: utf-8

# Comments #
############

# Import #
##########

import praw
import logging
import time
import datetime
import calendar

# Functions #
#############

def start(data,r,token_comment,awarder,awardee,flair_count):
  logging.debug("Starting Module: Wiki")
  submission_url = token_comment.submission.permalink
  submission_title = token_comment.submission.title
  try:
    user_wiki_page = r.get_wiki_page(data["running_subreddit"],"user/" + awardee)
    logging.debug("Found existing wiki page")
  except:
    logging.debug("Could not find existing wiki page")
    initial_text = "/u/%s has received %s delta for the following comments:" % (awardee,flair_count)
    add_link = "\n\n* [%s](%s) (1)\n    1. [Awarded by /u/%s](%s) on %s/%s/%s" % (submission_title, 
      submission_url, awarder, token_comment.permalink + "?context=2",today.month,today.day,today.year)
    full_update = initial_text + add_link
    r.edit_wiki_page(data["running_subreddit"],"user/" + awardee,full_update,"Created user's delta history page.")
  try:
    tracker_page = r.get_wiki_page(data["running_subreddit"],"delta_tracker")
  except:
    add_link = "* /u/%s - [Delta List](/r/%s/wiki/%s)" % (awardee,data["running_subreddit"],awardee)
    r.edit_wiki_page(data["running_subreddit"],"delta_tracker",add_link,"Updated tracker")

# EOF
