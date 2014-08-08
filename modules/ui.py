# User Interface #
##################

# Import
from settings import *

# Variables

# Functions

def start(data):
	print("\nWelcome to MARS!\n\nThis appears to be your first time running MARS. If this is incorrect or if you have already configured your config.json file, please change the initialize variable to 1 and restart MARS.\n\n")
	prod_setup(data)
	data["initialize"] = "1"
	condition = True
	while condition:
		test = raw_input("Do you have a test environment you wish to run MARS in (yes/no)? ")
		if test == "yes":
			test_setup(data)
			condition = False
		elif test == "no":
			print("Alright.")
			condition = False
		else:
			print("Please type yes or no.\n")

def prod_setup(data):
	data["prod_subreddit"] = raw_input("On what subreddit will MARS run? ")
	data["prod_username"] = raw_input("What is the username of the bot MARS will use (example: DeltaBot)? ")
	data["prod_password"] = raw_input("What is the password of the bot MARS will use (example: Hunter1)? ")
	print("Subreddit: " + data["prod_subreddit"])
	print("Username: " + data["prod_username"])
	print("Password: " + data["prod_password"])
	condition = True
	while condition:
		verify = raw_input("Does the above information look correct (yes/no)? ")
		if verify == "yes":
			condition = False
			return
		elif verify == "no":
			condition = False
			prod_setup(data)
		else:
			print("Please type yes or no.\n")
	config.write_json(data)

def test_setup(data):
		data["test_subreddit"] = raw_input("What is the test subreddit's name? ")
		condition = True
		while condition:
			prod2test = raw_input("Do you want to use the same username and password for test as prod (yes/no)? ")
			if prod2test == "yes":
				data["test_username"] == data["prod_username"]
				data["test_password"] == data["prod_password"]
				condition = False
			elif prod2test == "no":
				data["test_username"] = raw_input("What is the test username? ")
				data["test_password"] = raw_input("What is the test password? ")
				condition = False
			else:
				print("You did not enter a valid answer.\n")
		print("Test Subreddit: " + data["test_subreddit"])
		print("Test Username: " + data["test_username"])
		print("Test Password: " + data["test_password"])
		condition = True
		while condition:
			verify = raw_input("Does the above information look correct (yes/no)? ")
			if verify == "yes":
				condition = False
				return
			elif verify == "no":
				condition = False
				test_setup(data)
			else:
				print("Please type yes or no.\n")
