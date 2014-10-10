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
from urllib2 import HTTPError
import re

# Functions #
#############

def start(data,r,token_comment,awarder,awardee,flair_count):
  logging.debug("Starting Module: Wiki")
  submission_title = token_comment.submission.title
  submission_url = token_comment.submission.permalink
  today = datetime.date.today()
  try:
    user_wiki_page = r.get_wiki_page(data["running_subreddit"],"user/" + awardee)
    logging.debug("Found existing user wiki page")
    user_found = True
  except Exception as e:
    if e.response.status_code == 404:
      logging.debug("Did not find existing user wiki page")
      user_found = False
  if user_found:
    update_wiki_page(data,r,token_comment,awarder,awardee,flair_count,user_wiki_page)
  else:
    new_wiki_page(data,r,token_comment,awarder,awardee,flair_count)
  try:
    tracker_page = r.get_wiki_page(data["running_subreddit"],"index/delta_tracker")
    logging.debug("Found existing user wiki page")
    tracker_found = True
  except Exception as e:
    if e.response.status_code == 404:
      logging.debug("Did not find existing user wiki page")
      tracker_found = False
  if not tracker_found:
    update_tracker_page(data,r,awardee)
  else:
    new_tracker_page(data,r,awardee)

def new_wiki_page(data,r,token_comment,awarder,awardee,flair_count):
  submission_title = token_comment.submission.title
  submission_url = token_comment.submission.permalink
  today = datetime.date.today()
  if int(flair_count) < 2:
    initial_text = "/u/%s has received %s delta for the following comments:\n\n" % (awardee,flair_count)
  else:
    initial_text = "/u/%s has received %s deltas for the following comments:\n\n" % (awardee,flair_count)
  add_header = "| Submission | Delta Comment | Awarded By | Date |\n| --- | :-: | --- | --- |\n"
  add_content = "|[%s](%s)|[Link](%s)|/u/%s|%s/%s/%s|\n" % (submission_title,submission_url,
        token_comment.permalink + "?context=2",awarder,today.month,today.day,today.year)
  full_update = initial_text + add_header + add_content
  r.edit_wiki_page(data["running_subreddit"],"user/" + awardee,full_update,"Created user's delta history page.")

def new_tracker_page(data,r,awardee):
  initial_text = "Below is a list of all of the users that have earned deltas.\n\n"
  add_header = "| User | Delta List |\n| --- | --- |\n"
  add_content = "|/u/%s|[Link](/r/%s/wiki/%s)|\n" % (awardee,data["running_subreddit"],awardee)
  full_update = initial_text + add_header + add_content
  r.edit_wiki_page(data["running_subreddit"],"index/delta_tracker",full_update,"Updated tracker")

def update_wiki_page(data,r,token_comment,awarder,awardee,flair_count,user_wiki_page):
  submission_title = token_comment.submission.title
  submission_url = token_comment.submission.permalink
  today = datetime.date.today()
  old_content = user_wiki_page.content_md
  if int(flair_count) < 2:
    initial_text = "/u/%s has received %s delta for the following comments:\n\n" % (awardee,flair_count)
  else:
    initial_text = "/u/%s has received %s deltas for the following comments:\n\n" % (awardee,flair_count)
  lines = old_content.split("\n")
  table = []
  for line in lines:
    if re.match("(\|)",line):
      if not re.match("(\| Submission |\| --- \|)",line):
        table.append(line)
  table.sort()
  print("Printing table")
  print table
  new_content = '\n'.join(table)
  full_update = initial_text + new content
  r.edit_wiki_page(data["running_subreddit"],"user/" + awardee,full_update,"Updated user's delta history page.")

def update_tracker_page(data,r,awardee):
  return

# EOF
