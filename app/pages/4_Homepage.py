import os
import sys
import json
import time
import pytz
import boto3
import dotenv
# import langchain
import streamlit as st


# Initial page configurations
st.set_page_config(page_title="Homepage", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display : none
        }
    </style>
    """,
    unsafe_allow_html = True
)


username = None

if 'username' not in st.session_state:
    username = 'mkpentapalli2k2@gmail.com'
    # st.header("You need to login again!!")
    # time.sleep(2)
    # st.switch_page("pages/1_Login.py")
else:
    username = st.session_state['username']
    # st.write(f"Username: {username}")


# Initial setup of the Homepage
st.sesion_state['use_history'] = False
dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")
bucket_name = os.getenv("S3_BUCKET_NAME")
local_files_path = "/workspace/LEARN_SMART/docs/"
os.makedirs(f"{local_files_path}", exist_ok = True)


# Function to get the current time
def get_current_time() -> str:
    try:
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone)
        return current_time.srftime("%Y-%m-%d_%H:%M:%S")
    except Exception as e:
        print("Error occurred when trying to get the current time!!")
        return "Today"



def check_folder_exists(bucket_name, prefix_folder):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket = bucket_name, Prefix = prefix_folder)
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].startswith(prefix_folder):
                return True
    return False




def list_folders_in_bucket(bucket_name, folder_prefix):
    s3 = boto3.client('s3')
    folders_obj = s3.list_objects_v2(Bucket = bucket_name, Prefix = folder_prefix, Delimiter = '/')
    directories = [prefix.get('Prefix').split('/')[-2] for prefix in folders_obj.get('CommonPrefixes', [])]
    return directories




def download_files_from_s3_folder(bucket_name, folder_prefix, local_directory):
    s3 = boto3.client('s3')
    files_list = s3.list_objects_v2(Bucket = bucket_name, Prefix = folder_prefix)
    st.write(files_list)
    for i in range(1, len(files_list['Contents'])):
        key = files_list['Contents'][i]["Key"]
        local_file_path = os.path.join(local_directory, key.split('/')[-1])
        s3.download_file(bucket_name, key, local_file_path)



# Specifying the columns for the chat history and current history.
prev_chats, cur_chat = st.columns(spec = [0.3,0.7], gap="small")


with prev_chats:
    # st.write(f"users/{username}/")
    if check_folder_exists(bucket_name, f"users/{username}/"):
        st.write("You have previous chats!!")
        folders_list = list_folders_in_bucket(bucket_name, f"users/{username}/")
        for folder_name in folders_list:
            if prev_chats.button(f'{folder_name}'):
                # st.write(f"{folder_name}")
                chat_folder = f"users/{username}/{folder_name}/"
                download_files_from_s3_folder(bucket_name, chat_folder, local_files_path)
                st.session_state['use_history'] = True
                # break
                st.write("Files have been downloaded")
    else:
        st.write("You don't have any previous chats!!")
        st.session_state['use_history'] = False

with cur_chat:
    if st.session_state['use_history']:
        # Display the previous chat
        # Chat
        # Update the json
    else:
        # Create a new json file
        # Chat
        # Update the json.
    # If end chat:
        # Get current time
        # if not st.session_stat['use_history']:
            # Create a new folder in s3 bucket.
        # Else:
            # Rename the folder with current datetime
    # Upload the files in the s3 bucket's folder
    

    st.header("Another cat")
    # st.image("https://static.streamlit.io/examples/cat.jpg")


