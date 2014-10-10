# encoding: utf-8

# Import #
##########

import logging
from modules import account
from modules import wiki

# Variables #
#############

data = {}
data["running_subreddit"] = "PixelOrange"
data["running_username"] = "pixelsbot"
data["running_password"] = "PixelOrange"
data["m_account"] = "1"
r = account.start(data)
link = "http://www.reddit.com/r/PixelOrange/comments/2iqwgh/mars_test_thread_october/cl4m2jt"

# Functions #
#############

token_comment = r.get_submission(link).comments
print token_comment.body
print token_comment.author
wiki.start(data,r,token_comment,"Awarder","pixeltest1","2")

# EOF
