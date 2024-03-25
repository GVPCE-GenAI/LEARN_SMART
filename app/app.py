import json
import os
import sys
import boto3
import streamlit as st

## We will be suing Titan Embeddings Model To generate Embedding

from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.chat_models import BedrockChat
from langchain.llms.bedrock import Bedrock

## Data Ingestion

import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Vector Embedding And Vector Store

from langchain_community.vectorstores import FAISS

## LLm Models
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

## Bedrock Clients
bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)


## Data ingestion
def data_ingestion():
    loader=PyPDFDirectoryLoader("data")
    documents=loader.load()

    # - in our testing Character split works better with this PDF data set
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,
                                                 chunk_overlap=1000)
    
    docs=text_splitter.split_documents(documents)
    if len(docs) == 0:
        st.warning("Empty File Uploaded!!, Upload a Valid Document")
        data_ingestion()
    # print(type(docs))
    print(len(docs))
    return docs

## Vector Embedding and vector store

def get_vector_store(docs):
    vectorstore_faiss=FAISS.from_documents(
        docs,
        bedrock_embeddings
    )
    vectorstore_faiss.save_local("faiss_index")

def get_claude_llm():
    ##create the Anthropic Model
    # llm=Bedrock(model_id="anthropic.claude-v2:1",client=bedrock,
    #             model_kwargs={'max_tokens_to_sample':512})
    llm=BedrockChat(model_id="anthropic.claude-3-haiku-20240307-v1:0",client=bedrock,
                model_kwargs={'max_tokens':100000})
    
    return llm

# def get_llama2_llm():
#     ##create the Anthropic Model
#     llm=Bedrock(model_id="meta.llama2-70b-chat-v1",client=bedrock,
#                 model_kwargs={'max_gen_len':512})
    
    return llm

# Human: Firstly, greet the user with a friendly or professional greeting if given a prompt of greeting. 
# Note that, you must only respond to a prompt when given by the user. 
# When asked about anything related to the document uploaded, use the following pieces of context to provide a concise answer to the question based on the prompt of the user and give an answer only as much is required and be specific. 
# If the prompt given by the user is not related to the document, do not give a response, rather tell that the prompt is not related to the document. 
# If there is any prompt of the user specifying something, then respond only with that information as much is present in the document. Do not give any response outside of the information mentioned in the document.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.

prompt_template = """

Human: Anything that is specified in the square brackets shouldn't be given as a response to the user. Rather, it is only for your own understanding.
Initially, you need to extract all the information and content from the document uploaded by the user. Then, you need to analyse the prompt provided by the user to understand the intent.
If the document is empty or doesn't contain any information, then give a response that the document doesn't provide any information and ask the user to upload a valid document.
Be more careful to only respond based on the details provided in the document, and not make assumptions or provide information that is not present. If the information is not present explicitly in the document then say that the document doesn't explicitly specify anything.
If you find that there are any spelling or grammatical mistakes in the prompt provided by the user, then respond in the following way: Giving a response to the question: [grammatically correct user's prompt]
Be more attentive to the details provided in the prompt and address the spelling error accordingly. Be sure to point out any spelling or grammatical mistakes in the user's prompt before providing the correct response.
Also, you need to bear in mind the context of the previous prompts of the user to answer any follow-up questions if necessary. 
You should only respond to as much asked by the user through the prompt, neither more nor less.
Initially, in your response be very brief with how you respond. Give more information if the user asks you to elaborate or expand on the information.
If the user greets you with a greeting, then greet the user back with a professional or friendly greeting depending on how the user greeted you. You need not greet the user after every prompt, but only greet if the user greets you first.
You should only respond to any context of the prompt within the scope of the document. Other than that, you can only respond to greetings or some casual questions. You should not give any response outside of the context of the document other than the casual questions through which the user wants to interact with you.
If the prompt is a question about the document, then you need to search for relevant information within the context of the document and generate a concise answer and respond to the prompt as much asked by the user, neither more nor less.
If the prompt requests specific information, you must retrieve the relevant details from the context and present them to the user.
If the user asks to summarize anything or any topic from the document, then you need to generate a concise summary highlighting key points. The summary length can be adjusted based on user specifications (if provided).
You must also perform question and answering with the user based on the interaction with the user through prompts.
If the user asks to explain something with the help of an example, then firstly you need to understand the topic related to the context clearly and come up with clear examples based on your understanding of the context and then present it to the user.
If the user asks to provide any references or citations, if they are present in the document, then provide it, if not, then say that the document doesn't specify any citations or references.
If the user asks you to expand upon a particular topic, then you need to first understand it clearly with respect to the information present in the document and then expand it accordingly based on the need of the user and upto a certain word limit(if provided).
If the prompt is not related to the uploaded document, then inform the user that the prompt cannot be answered based on the current document.
If you cannot find an answer within the document, acknowledge that you don't know the answer instead of making something up.
You should rely solely on the information present in the uploaded document.



<context>
{context}
</context

Question: {question}

Assistant:"""

# system_prompt = """You are an expert in the domains of Natural Language Processing, Langchain, Large Language Models, and Anthropic Claude Haiku, you need to answer the question from the user in a concise and relevant manner."""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

def get_response_llm(llm,vectorstore_faiss,query):
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore_faiss.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer=qa({"query":query})
    return answer['result']


def main():
    st.set_page_config("Chat PDF")
    
    st.header("Chat with PDF using AWS Bedrock💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    with st.sidebar:
        st.title("Update Or Create Vector Store:")
        
        if st.button("Vectors Update"):
            with st.spinner("Processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("Done")

    if st.button("Claude Output"):
        with st.spinner("Processing..."):
            # Assuming you're using a function or method to load the pickle file
            faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)

            llm=get_claude_llm()
            
            #faiss_index = get_vector_store(docs)
            st.write(get_response_llm(llm,faiss_index,user_question))
            st.success("Done")

    # if st.button("Llama2 Output"):
    #     with st.spinner("Processing..."):
    #         faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings)
    #         llm=get_llama2_llm()
            
    #         #faiss_index = get_vector_store(docs)
    #         st.write(get_response_llm(llm,faiss_index,user_question))
    #         st.success("Done")

if __name__ == "__main__":
    main()