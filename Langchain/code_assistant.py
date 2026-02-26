import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import RetrievalQA
import os

load_dotenv()

llm1 = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4.1-nano", temperature=0)

prompt1 = ChatPromptTemplate.from_template(
    """
    You are an expert email writer, using the following bullet points, draft a professional 
    {code_task}
    Provide clean, well-commented code and explaination as needed
    """
)

chain1 = prompt1 | llm1 | StrOutputParser() 

#Streamlit UI
st.title("Code Assistant")
code_task = st.text_area("Describe your coding task:")

if st.button("Generate code"):
     if code_task.strip() == "":
        st.warning("Please enter a task description")
     else:
         response = chain1.invoke(code_task)   
         st.subheader = ("Assistant response")
         st.code(response,language='python')
  