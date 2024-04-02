import os
import sys
import json
import time
import pytz
import boto3
import shutil
import dotenv
import streamlit as st
from datetime import datetime
from langchain.llms.bedrock import Bedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock
from langchain_community.chat_models import BedrockChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader


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
    st.header("You need to login again!!")
    time.sleep(2)
    st.switch_page("pages/1_Login.py")
else:
    username = st.session_state['username']


# Initial setup of the Homepage                    
dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")
bucket_name = os.getenv("S3_BUCKET_NAME")
docs_path = "/workspace/LEARN_SMART/app/docs/"                  # Make docs directory
os.makedirs(f"{docs_path}", exist_ok = True)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "aws_folder_name" not in st.session_state:
    st.session_state.aws_folder_name = []
st.session_state.docs = None
st.session_state.use_history = False
uploaded_file = False
bedrock=boto3.client(service_name="bedrock-runtime", region_name = os.getenv("USER_POOL_REGION"))
bedrock_embeddings = BedrockEmbeddings(model_id = "amazon.titan-embed-text-v1", client = bedrock)



# Function to get the current time
def get_current_time() -> str:
    try:
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone)
        return current_time.strftime("%Y-%m-%d_%H:%M:%S")
    except Exception as e:
        print(f"Error occurred when trying to get the current time!!{e}")
        return None



# Function to check if a folder exists in an AWS s3 bucket
def check_folder_exists(bucket_name, prefix_folder):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket = bucket_name, Prefix = prefix_folder)
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].startswith(prefix_folder):
                return True
    return False



# List all the folders in an AWS s3 bucket
def list_folders_in_bucket(bucket_name, folder_prefix):
    s3 = boto3.client('s3')
    folders_obj = s3.list_objects_v2(Bucket = bucket_name, Prefix = folder_prefix, Delimiter = '/')
    directories = [prefix.get('Prefix').split('/')[-2] for prefix in folders_obj.get('CommonPrefixes', [])]
    return directories



# Download all the files from an AWS bucket to local folder
def download_files_from_s3_folder(bucket_name, folder_prefix, local_directory):
    s3 = boto3.client('s3')
    files_list = s3.list_objects_v2(Bucket = bucket_name, Prefix = folder_prefix)
    for i in range(len(files_list['Contents'])):
        key = files_list['Contents'][i]["Key"]
        local_file_path = os.path.join(local_directory, key.split('/')[-1])
        s3.download_file(bucket_name, key, local_file_path)



# Append chat messages in the streamlit session state
def append_message(container, role, content):
    container.session_state.chat_history.append({"role": role, "content": content})


# Get history of the previous chats
def get_history():
    with open(f"{docs_path}chat.json", "r") as file:
        json_data = json.load(file)
    st.session_state.chat_history = json_data



# Delete all files in a given local directory
def del_files_in_docs(directory = docs_path):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Couldn't remove the file: {filename}, Exception: {e}")


# Check a pdf's size
def check_pdf_size(directory):
    max_size = 20 * 1024 * 1024
    filesize = os.path.getsize(directory)
    return filesize <= max_size


def data_ingestion(directory):
    loader = PyPDFDirectoryLoader(directory)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 25000,
                                                    chunk_overlap = 1000)
    docs = text_splitter.split_documents(documents)
    if len(docs) == 0:
        return None, False
    return docs, True



def get_vector_store(directory, docs):
    vectorstore_faiss = FAISS.from_documents(
        docs,
        bedrock_embeddings
    )
    vectorstore_faiss.save_local(directory)


def get_claude_llm():
    llm = BedrockChat(model_id = "anthropic.claude-3-haiku-20240307-v1:0", client = bedrock, model_kwargs = {'max_tokens' : 20000})
    return llm


prompt_template = """
Main task: You are someone who understands the given context and then responds to the user's queries accordingly.
Tasks:
1. Consider everything that is in XML tag with the name 'context' as the context given by the user.
2. You should only answer user's questions based on the provided context. So, if context is missing for user's question, simply reply that there is no context on the question asked.
3. When asked for summarization, give a brief summary in bullet points; make is short and clear but not too exagerated. Do not copy paste the given context.
4. When normal questions are asked, give short answers with facts that are existing in the context, but don't give too long answers.
5. When factual questions are asked, do not hallucinate but only consider the context given.
6. And, when there are mistakes in the user's question (either grammatically or based on meaning), consider the correct quesion.
7. When asked to elaborate on a specific topic, give an example. But make sure that the example is easy-to-understand with not much technical jargon.
8. You also need to highlight key points for any questions asked.
<context>
{context}
</context>
Question: {question}
Assistant:"""



PROMPT = PromptTemplate(
    template = prompt_template, input_variables = ["context", "question"]
)



def get_response_llm(llm, vectorstore_faiss, query):
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = vectorstore_faiss.as_retriever(
            search_type = "similarity", search_kwargs = {"k" : 5}
        ),
        return_source_documents = True,
        chain_type_kwargs = {"prompt": PROMPT}
    )
    answer = qa({"query" : query})
    return answer['result']



def delete_folder(folder_name):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket = bucket_name, Prefix = folder_name)
    deletion_objects = {'Objects' : []}
    for page in pages:
        for item in page.get('Contents', []):
            deletion_objects['Objects'].append({'Key' : item['Key']})
        if deletion_objects['Objects']:
            client.delete_objects(Bucket = bucket_name, Delete = deletion_objects)
            deletion_objects['Objects'] = []
    client.delete_object(Bucket = bucket_name, Key = folder_name)



def upload_folder_to_s3_folder(local_folder_name, folder_path, target_folder_path):
    client = boto3.client('s3')
    local_folder_name += '/'
    client.put_object(Bucket = bucket_name, Key = target_folder_path, Body = "")
    s3_folder_key = os.path.join(target_folder_path+local_folder_name, os.path.basename(folder_path))
    for filename in os.listdir(folder_path):
        s3_object_key = os.path.join(s3_folder_key, filename)
        upload_file = os.path.join(folder_path, filename)
        client.upload_file(upload_file, bucket_name, s3_object_key)


# Specifying the columns for the chat history and current history.
prev_chats, cur_chat = st.columns(spec = [0.2,0.8], gap="small")


# Container for previous chats
with prev_chats:
    st.header("Previous chats:")
    if check_folder_exists(bucket_name, f"users/{username}/"):
        folders_list = list_folders_in_bucket(bucket_name, f"users/{username}/")
        folders_list.sort(reverse = True)
        aws_folder = None
        for folder_name in folders_list:
            if prev_chats.button(f'{folder_name}'):
                chat_folder = f"users/{username}/{folder_name}/"
                st.session_state.aws_folder_name.append(chat_folder)
                download_files_from_s3_folder(bucket_name, chat_folder, docs_path)
                st.session_state.use_history = True
                get_history()
    else:
        st.header("You have no previous chats.")


# Container for current chats
with cur_chat:
    st.header("Chat with PDF using Learn Smart :sunglasses:")  
    if st.session_state.chat_history != []:
        if uploaded_file == False:
            st.session_state.use_history = True
        else:
            st.session_state.use_history = False
    elif uploaded_file == False:
        st.write("Upload your pdf file (maximum filesize is 20Mb):")
        uploaded_file = st.file_uploader(label = "Pdf-file", type = 'pdf', help = "Upload only pdf files!", label_visibility = "collapsed")
        css = '''
        <style>
            [data-testid='stFileUploader']{
                width: max-content;
            }
            [data-testid='stFileUploader']{
                padding: 0;
                float: middle;
            }
            [data-testid='stFileUploader'] section > input + div {
                display : none;
            }
            [data-testid='stFileUploader'] section + div {
                float: middle;
                padding-top: 0;
            }
            </style>
        '''
        st.markdown(css, unsafe_allow_html = True)
        if uploaded_file is not None:
            if st.button("Upload PDF"):
                del_files_in_docs()
                with open(f"{docs_path}chat.json", "w") as file:
                    pass
                st.session_state.chat_history = []
                filename = uploaded_file.name
                with open(os.path.join(docs_path,filename), "wb") as f:
                    f.write(uploaded_file.getvalue())
                if(check_pdf_size(os.path.join(docs_path,filename))):
                    st.session_state.docs, val = data_ingestion(docs_path)
                    if val == False:
                        del_files_in_docs()
                        st.warning("File is empty!!!, remove the file and try again!!")
                    else:
                        with st.spinner("Processing embeddings...."):
                            get_vector_store(docs_path, st.session_state.docs)
                else:
                    del_files_in_docs()
                    st.warning("File size is not within 20MB, remove the file and try again!!")
        st.session_state.use_history = False
        uploaded_file = True


    if st.button("End Chat and Signout"):
        if st.session_state.chat_history == []:
            st.switch_page("pages/5_Signout.py")
        with open(f"{docs_path}chat.json", "w") as file:
            json.dump(st.session_state.chat_history, file)
        current_datetime = get_current_time()
        if st.session_state.use_history == True and st.session_state.aws_folder_name != []:
            delete_folder(f"{st.session_state.aws_folder_name[-1]}")

        app_folder = "/workspace/LEARN_SMART/app/"
        new_folder_path = app_folder+f"{current_datetime}/"
        os.rename(app_folder+"docs/", new_folder_path)


        upload_folder_to_s3_folder(current_datetime, new_folder_path, f"users/{username}/")
        st.warning("You will now be signing out!!")
        if os.path.isdir(new_folder_path):
            del_files_in_docs(new_folder_path)
            shutil.rmtree(new_folder_path)
        time.sleep(3)
        st.session_state.username = ""
        st.session_state.chat_history = []
        st.session_state.aws_folder_name = []
        st.session_state.use_history = False
        st.switch_page("pages/5_Signout.py") 


    if prompt := st.chat_input("User prompt: ", max_chars = 500):
        li = []
        li.append({"role":"user", "content":prompt})
        index = FAISS.load_local(docs_path, bedrock_embeddings, allow_dangerous_deserialization = True)
        llm = get_claude_llm()
        response = get_response_llm(llm, index, prompt)
        li.append({"role":"assistant", "content":response})
        st.session_state.chat_history.append(li)

    for message in reversed(st.session_state.chat_history):
        for i in range(2):
            st.chat_message(message[i]['role']).markdown(message[i]['content'])
