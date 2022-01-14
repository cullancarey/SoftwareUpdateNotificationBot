import requests
import tweepy
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
from db import *
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
load_dotenv()

def compare_lists(release_list, db_list, conn, release_statments, slack_client, twitter_client):
	no_updates_msg = f'{datetime.now()} \nNo new releases at this time. \n#iOS #macOS #tvOS #watchOS #apple'
	iOS_msg = f'{datetime.now()} \niOS release available! \n{release_statments[0]} \n#iOS #apple'
	macOS_msg = f'{datetime.now()} \nmacOS release available! \n{release_statments[1]} \n#macOS #apple'
	tv_os_msg = f'{datetime.now()} \ntvOS release available! \n{release_statments[2]} \n#tvOS #apple'
	watchOS_msg = f'{datetime.now()} \nwatchOS release available! \n{release_statments[3]} \n#watchOS #apple'
	if release_list == db_list:
		send_slack_message(slack_client, no_updates_msg)
		twitter_client.update_status(no_updates_msg)
	if release_list[0] != db_list[0]:
		send_slack_message(slack_client, iOS_msg)
		twitter_client.update_status(iOS_msg)
		db.sql_insert(conn, release_list)
	if release_list[1] != db_list[1]:
		send_slack_message(slack_client, macOS_msg)
		twitter_client.update_status(macOS_msg)
		db.sql_insert(conn, release_list)
	if release_list[2] != db_list[2]:
		send_slack_message(slack_client, tv_os_msg)
		twitter_client.update_status(tv_os_msg)
		db.sql_insert(conn, release_list)
	if release_list[3] != db_list[3]:
		send_slack_message(slack_client, watchOS_msg)
		twitter_client.update_status(watchOS_msg)
		db.sql_insert(conn, release_list)

def send_slack_message(client, message):
	try:
	    response = client.chat_postMessage(channel='#softwareupdatenotificationbot', text=f"{message}")
	except SlackApiError as e:
	    # You will get a SlackApiError if "ok" is False
	    assert e.response["ok"] is False
	    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
	    client.chat_postMessage(channel='#softwareupdatenotificationbot', text=f"Got an error: {e.response['error']}")

URL = "https://support.apple.com/en-us/HT201222"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("li")
release_statments = []
for i in results:
	if "The latest version" in i.text:
		s = i.text.replace(" ", " ")
		group = re.search("^.*?[.!?](?:\\s|$)(?!.*?\\))", s)
		group = group.group(0)
		release_statments.append(group)

releases = []
for i in release_statments:
	y = re.findall(r'[\d\.]+', i)
	for x in y:
		print(x)
		releases.append(x[0:-1])

#Sets Slack client
slack_client = WebClient(token=os.environ['SLACK_BOT_USER_OAUTH'])

#Set Twitter client 
CLIENT_ID = os.environ['API_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CLIENT_SECRET = os.environ['SECRET_KEY']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(f"{CLIENT_ID}", f"{CLIENT_SECRET}")
auth.set_access_token(f"{ACCESS_TOKEN}", f"{ACCESS_TOKEN_SECRET}")

# Create API object
twitter_client = tweepy.API(auth)

#Create db and make sure 
#'releases' table exists
db = database()
conn = db.sql_connection()
# db.drop_table(conn)
db.sql_create_table_if_not_exists(conn)

#Check if release is up to date
row_list = db.sql_select(conn)
for i in row_list:
	row_list = list(i)
row_list = row_list[1:5]
print(f"DB list: {row_list}")
print(f"Website list: {releases}")
if row_list:
	db.sql_select(conn)
else:
	db.sql_insert(conn, releases)
	print(db.sql_select(conn))
# releases = [15.2, 12.1, 15.2, 8.3]
compare_lists(releases, row_list, conn, release_statments, slack_client, twitter_client)

