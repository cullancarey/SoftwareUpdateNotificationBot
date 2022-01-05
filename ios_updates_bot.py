import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
from db import *
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
load_dotenv()

def compare_lists(release_list, db_list, conn, release_statments, client):
	if release_list == db_list:
		send_slack_message(client, 'No new releases at this time.')
	if release_list[0] != db_list[0]:
		send_slack_message(client, f'iOS release available! \n{release_statments[0]}')
		db.sql_insert(conn, release_list)
	if release_list[1] != db_list[1]:
		send_slack_message(client, f'macOS release available! \n{release_statments[1]}')
		db.sql_insert(conn, release_list)
	if release_list[2] != db_list[2]:
		send_slack_message(client, f'tvOS release available! \n{release_statments[2]}')
		db.sql_insert(conn, release_list)
	if release_list[3] != db_list[3]:
		send_slack_message(client, f'watchOS release available! \n{release_statments[3]}')
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
		group = re.search("^.*?[.!?](?:\\s|$)(?!.*\\))", s)
		group = group.group(0)
		release_statments.append(group)

releases = []
for i in release_statments:
	x = re.findall(r'\d+\.\d+', i)
	for l in x:
		releases.append(float(l))

#Sets Slack client
client = WebClient(token=os.environ['SLACK_BOT_USER_OAUTH'])

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
print(row_list)
print(releases)
if row_list:
	db.sql_select(conn)
else:
	db.sql_insert(conn, releases)
	# print(db.sql_select(conn))
# releases = [15.2, 12.1, 15.2, 8.3]
compare_lists(releases, row_list, conn, release_statments, client)

