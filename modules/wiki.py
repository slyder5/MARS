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
import pprint

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
    tracker_page = r.get_wiki_page(data["running_subreddit"],data["running_username"] + "/tracker")
    logging.debug("Found existing tracker wiki page")
    tracker_found = True
  except Exception as e:
    if e.response.status_code == 404:
      logging.debug("Did not find existing tracker wiki page")
      tracker_found = False
  if tracker_found:
    update_tracker_page(data,r,awardee,token_comment,tracker_page)
  else:
    new_tracker_page(data,r,awardee,token_comment)

def new_wiki_page(data,r,token_comment,awarder,awardee,flair_count):
  submission_title = token_comment.submission.title
  submission_url = token_comment.submission.permalink
  today = datetime.date.today()
  add_header = "| Date | Submission | Delta Comment | Awarded By |\n| --- | :-: | --- | --- |\n"
  add_content = "|%s/%s/%s|[%s](%s)|[Link](%s)|/u/%s|" % (today.month,today.day,today.year,submission_title,
  submission_url,token_comment.permalink + "?context=2",awarder)
  if int(flair_count) < 2:
    initial_text = "/u/%s has received %s delta for the following comment:\n\n" % (awardee,flair_count)
  else:
    initial_text = "/u/%s has received %s deltas for the following comments:\n\n" % (awardee,flair_count)
  full_update = initial_text + add_header + add_content
  r.edit_wiki_page(data["running_subreddit"],"user/" + awardee,full_update,"Created user's delta history page.")

def update_wiki_page(data,r,token_comment,awarder,awardee,flair_count,user_wiki_page):
  submission_title = token_comment.submission.title
  submission_url = token_comment.submission.permalink
  today = datetime.date.today()
  old_content = user_wiki_page.content_md
  add_header = "| Date | Submission | Delta Comment | Awarded By |\n| --- | :-: | --- | --- |\n"
  add_content = "|%s/%s/%s|[%s](%s)|[Link](%s)|/u/%s|" % (today.month,today.day,today.year,submission_title,
                submission_url,token_comment.permalink + "?context=2",awarder)
  if int(flair_count) < 2:
    initial_text = "/u/%s has received %s delta for the following comment:\n\n" % (awardee,flair_count)
  else:
    initial_text = "/u/%s has received %s deltas for the following comments:\n\n" % (awardee,flair_count)
  lines = old_content.split("\n")
  note = ""
  table = []
  for line in lines:
    if re.match("(\|)",line):
      if not re.match("(\| Date |\| --- \|)",line):
        table.append(line)
    elif re.match("Any delta history",line):
      note = line + "\n\n"
  table.append(add_content)
  table.sort(reverse=True)
  new_content = '\n'.join(table)
  full_update = initial_text + note + add_header + new_content
  r.edit_wiki_page(data["running_subreddit"],"user/" + awardee,full_update,"Updated user's delta history page.")

def new_tracker_page(data,r,awardee,token_comment):
  initial_text = "Below is a list of all of the users that have earned deltas.\n\n"
  add_header = "| User | Delta List | Delta Earned|\n| --- | --- | --- |\n"
  add_content = "|/u/%s|[Link](/r/%s/wiki/user/%s)|[Link](%s)|" % (awardee,data["running_subreddit"],
                awardee,token_comment.permalink + "?context=2")
  full_update = initial_text + add_header + add_content
  r.edit_wiki_page(data["running_subreddit"],data["running_username"] + "/tracker",full_update,"Updated tracker")

def update_tracker_page(data,r,awardee,token_comment,tracker_page):
  initial_text = "Below is a list of all of the users that have earned deltas.\n\n"
  add_header = "| User | Delta List | Last Delta Earned |\n| --- | --- | --- |\n"
  add_content = "|/u/%s|[Link](/r/%s/wiki/user/%s)|[Link](%s)|" % (awardee,data["running_subreddit"],
                awardee,token_comment.permalink + "?context=2")
  old_content = tracker_page.content_md
  awardee_already_exists = False
  lines = old_content.split("\n")
  table = []
  for line in lines:
    if re.match("(\|)",line):
      if not re.match("(\| User |\| --- \|)",line):
        if awardee not in line:
          table.append(line)
        else:
          table.append(add_content)
          awardee_already_exists = True
  if awardee_already_exists:
    table.append(add_content)
  else:
    table.append(add_content)
  table.sort()
  new_content = '\n'.join(table)
  full_update = initial_text + add_header + new_content
  r.edit_wiki_page(data["running_subreddit"],data["running_username"] + "/tracker",full_update,"Updated tracker")

# EOF
