# encoding: utf-8

# Import #
##########

import logging
from modules import account

# Variables #
#############

data = {}
data["running_subreddit"] = "PixelOrange"
data["running_username"] = "pixelsbot"
data["running_password"] = "PixelOrange"
data["m_account"] = "1"
r = account.start(data)

# Functions #
#############

print data
print r
