# encoding: utf-8

# Import #
##########

import logging
from modules import account

# Variables #
#############

data["running_subreddit"] = "PixelOrange"
data["m_account"] = "1"
r = account.start(data)

# Functions #
#############

print data
print r
