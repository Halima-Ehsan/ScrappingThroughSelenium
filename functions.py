# chat_functions
import os
import time
import zipfile
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    option = Options()
    option.add_experimental_option("debuggerAddress", "localhost:9988")
    driver = webdriver.Chrome(options=option)
    driver.get("https://chat.openai.com")
    return driver

def extract_and_print_titles(driver):
    try:
        wait = WebDriverWait(driver, 10)
        chat_list = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[1]/div[1]/div/div/div/nav/div[2]/div[3]/div/div/ol")))

        chat_titles = driver.find_elements(By.XPATH, "//*[@id='__next']/div[1]/div[1]/div/div/div/nav/div[2]/div[3]/div/div/ol/li/div/a")
        print("Titles of all the Chats:")
        for titles in chat_titles:
            print(titles.text)

    finally:
        driver.quit()

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    is_saved = Column(Boolean, default=False)

def setup_database(db_path='sqlite:///chats.db'):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def read_and_save_chat(json_data, session):
    chat_id = json_data.get('id')
    title = json_data.get('title')
    existing_chat = session.query(Chat).filter_by(title=title).first()
    
    if existing_chat:
        print(f"Chat '{title}' already exists in the database.")
        return

    new_chat = Chat(title=title, is_saved=True)
    session.add(new_chat)
    session.commit()
    print(f"Chat '{title}' saved successfully.")

def extract_zip_file(zip_file_path, extract_to_folder):
    if not os.path.exists(extract_to_folder):
        os.makedirs(extract_to_folder)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)
        print(f"Files extracted to: {extract_to_folder}")

def process_chat_files(folder_path, session):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                read_and_save_chat(json_data, session)


def automate_chat_export(zip_folder_path, unzip_folder_path, db_session):
    zip_file_name = None
    while zip_file_name is None:
        for file in os.listdir(zip_folder_path):
            if file.endswith('.zip'):
                zip_file_name = file
                break
        time.sleep(5) 

    # Extract the zip file
    zip_file_path = os.path.join(zip_folder_path, zip_file_name)
    extract_zip_file(zip_file_path, unzip_folder_path)
    
    # Process the extracted JSON files
    process_chat_files(unzip_folder_path, db_session)

#Function to view database table
def view_chats_table(session, db_path='sqlite:///chats.db'):
    chats = session.query(Chat).all()
    print("DataBase Table:")
    for chat in chats:
        print(f"ID: {chat.id}, Title: {chat.title}, Is Saved: {chat.is_saved}")