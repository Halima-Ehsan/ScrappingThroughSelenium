# ScrappingThroughSelenium

## Steps
- Accessing current Chrome profile in selenium
- Go to ChatGpt HomePage
- Scrapping titles for all the chat names from ChatGpt
- Fetching whole chats from ChatGpt (Use TemperMonkey Extension to export all chats)
- Write a function that reads/un-zip the extracted file and saves it in a folder.
- We will handle status to check if the chat has been saved or not. 
- Use SQLite with SQLAlchemy to store this data in a database. 
- Check each title to see if it already exists in the database. If the title isn't in the database, insert it and save the file in the folder otherwise skip it.

## Prerequisites
- Python 3.x installed on your system.
- Google Chrome browser installed.
- TemperMonkey extension installed in Chrome for exporting chats.

## Installation
- pip install selenium
- pip install SQLAlchemy