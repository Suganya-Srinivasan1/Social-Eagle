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
    You are a helpful AI assistant,
    User says = {user_input}
    Your response:
    """
)

chain1 = prompt1 | llm1 | StrOutputParser() 

if __name__ == "__main__":
     user_input = input("Ask me anything")
     response1 = chain1.invoke(user_input)
     print ("AI says: ", response1)