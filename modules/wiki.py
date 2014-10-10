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
  today = datetime.date.today()
  user_wiki_page = r.get_wiki_page(data["running_subreddit"],"user/" + awardee)
  if user_wiki_page:
    logging.debug("Found existing user wiki page")
  else:
    logging.debug("Could not find existing user wiki page")

def placeholder():
    
    if int(flair_count) < 2:
      initial_text = "/u/%s has received %s delta for the following comments:\n\n" % (awardee,flair_count)
    else:
      initial_text = "/u/%s has received %s deltas for the following comments:\n\n" % (awardee,flair_count)
    add_title = "| Submission | Delta Comment | Awarded By | Date |\n| --- | :-: | --- | --- |\n"
    add_content = "|[%s](%s)|[Link](%s)|/u/%s|%s/%s/%s|\n" % (submission_title,submission_url,
          token_comment.permalink + "?context=2",awarder,today.month,today.day,today.year)
    full_update = initial_text + add_title + add_content
    r.edit_wiki_page(data["running_subreddit"],"user/" + awardee,full_update,"Created user's delta history page.")
  try:
    tracker_page = r.get_wiki_page(data["running_subreddit"],"index/delta_tracker")
    logging.debug("Found existing tracker wiki page")
  except:
    logging.debug("Could not find existing tracker wiki page")
    add_link = "* /u/%s - [Delta List](/r/%s/wiki/%s)" % (awardee,data["running_subreddit"],awardee)
    r.edit_wiki_page(data["running_subreddit"],"delta_tracker",add_link,"Updated tracker")

# EOF
