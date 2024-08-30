# Main Script
from functions import setup_driver, extract_and_print_titles, setup_database, view_chats_table, automate_chat_export

if __name__ == "__main__":

    driver = setup_driver()
    extract_and_print_titles(driver)

    session = setup_database()

    zip_folder_path = './zipfolder'
    unzip_folder_path = './extracted_files'
    
    automate_chat_export(zip_folder_path, unzip_folder_path, session)

    view_chats_table(session)

