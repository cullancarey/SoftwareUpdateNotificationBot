# SoftwareUpdateNotificationBot

OVERVIEW:
Hello! This project was inspired because the "automatic updates" feature on my Apple iPhone does not seem to work as intended. I don't think it has ever automatically installed a new update on its own. I would have to manually check if a new release was available and then go update it myself. With this project, half of that manual work is taken care of. 

This project scrapes the Apple security updates website (https://support.apple.com/en-us/HT201222), parses it for the latest software updates, and then sends a slack message and tweet at set points in the day if a new update available or not. It uses sqlite3 as a datasource to keep track of what release is current. If it detects a new release, it will add that to the database. 

Please follow @UpdateApple_ to support!
