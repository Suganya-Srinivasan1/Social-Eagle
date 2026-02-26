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
    You are an expert email writer, using the following bullet points, draft a professional,  
    {bullet_points}
    Make sure the email has a greeting, clear structure, and a closing
    """
)

chain1 = prompt1 | llm1 | StrOutputParser() 

#Streamlit UI
st.title("Smart email writer")
st.write("Enter key bullet points for your email below:")
bullet_points = st.text_area("Bullet points",height=200)

if st.button("Generate email"):
     if bullet_points.strip() == "":
        st.warning("Please enter some bullet points")
     else:
         email = chain1.invoke(bullet_points)   
         st.subheader = ("Dafted email")
         st.write(email)
  