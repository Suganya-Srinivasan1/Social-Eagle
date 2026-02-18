import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LLM, Embeddings, and Search
# Note: Ensure "gpt-4.1-nano" is a valid model name in your environment; usually it's "gpt-4o" or "gpt-3.5-turbo"
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4.1-nano", temperature=0)
openai_embed = OpenAIEmbeddings()
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

st.set_page_config(page_title="RAG + Web Search Chatbot")
st.title("PDF Assistant with Web Fallback")

uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if uploaded_file is not None:
    raw_text = ""
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

    if raw_text.strip():
        # 1. Chunking & Vector Store (Simplified for demo)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        vectorstore = FAISS.from_texts(chunks, openai_embed)
        vectorstore.save_local("My_first_VectorDB") # Save vector DB as local folder
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        query = st.text_input("Ask a question about the PDF (or anything else!)")
        
        if query:
            with st.spinner("Analyzing PDF and verifying context..."):
                # Retrieve context
                docs = retriever.invoke(query)
                context = "\n\n".join([doc.page_content for doc in docs])

                # Specialized Grader Prompt
                grader_prompt = f"""
                You are a specialized Retrieval Grader. 
                Assess if the CONTEXT is sufficient to answer the USER QUESTION.

                CONTEXT:
                ----------
                {context}
                ----------

                USER QUESTION: {query}

                STRICT INSTRUCTIONS:
                1. If the context is sufficient, provide the answer.
                2. If the context is missing info or irrelevant, start your response with: [TRIGGER_WEB_SEARCH]
                """

                # Get Grader Response
                grader_output = llm.invoke(grader_prompt).content

                if "[TRIGGER_WEB_SEARCH]" in grader_output:
                    st.info("🔍 PDF context is insufficient. Consulting the web...")
                    
                    # Web Search
                    search_result = search.run(query)
                    
                    # Final Synthesis
                    synthesis_prompt = f"""
                    The user asked: {query}
                    PDF Data: {context[:500]}... (truncated)
                    Web Data: {search_result}
                    Provide a comprehensive answer combining both.
                    """
                    final_answer = llm.invoke(synthesis_prompt).content
                    st.subheader("Answer (Augmented via Web)")
                    st.write(final_answer)
                else:
                    st.subheader("Answer (from PDF)")
                    st.write(grader_output)
    else:
        st.error("No text found in PDF.")