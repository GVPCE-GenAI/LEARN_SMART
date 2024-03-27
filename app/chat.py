import os
import sys
import json
import boto3
import dotenv
from langchain.llms.bedrock import Bedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock
from langchain_community.chat_models import BedrockChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")
USER_REGION = os.getenv("USER_POOL_REGION")

bedrock = boto3.client(service_name = "bedrock-runtime", region_name = USER_REGION)
bedrock_embeddings = BedrockEmbeddings(model_id = "amazon.titan-embed-text-v1", client = bedrock)

def data_ingestion(directory):
    loader = PyPDFDirectoryLoader(directory)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000,
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



def get_claude_output():
    llm = BedrockChat(model_id = "anthropic.claude-3-haiku-20240307-v1:0", client = bedrock, model_kwargs = {'max_tokens' : 150000})
    return llm



prompt_template = """
Human: Anything that is specified in the square brackets shouldn't be given as a response to the user. Rather, it is only for your own understanding. Also, you need not display the square brackets in your response, it is only for your understanding.
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