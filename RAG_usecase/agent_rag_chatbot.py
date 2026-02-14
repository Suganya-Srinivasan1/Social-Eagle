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
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4.1-nano", temperature=0)
openai_embed = OpenAIEmbeddings()
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

# Page Config
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
        # 1. Chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        
        # 2. Vector Store
        vectorstore = FAISS.from_texts(chunks, openai_embed)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        # 3. Interaction
        query = st.text_input("Ask a question about the PDF (or anything else!)")
        
        if query:
            with st.spinner("Analyzing PDF and verifying context..."):
                # Retrieve relevant documents
                docs = retriever.invoke(query)
                context = "\n\n".join([doc.page_content for doc in docs])

                # Verifier Prompt
                # 2. Define the Refined_query (This was likely missing!)
                # We clean the user query to make it better for searching
                why_correction_needed = ""
                decision = ""
                response = ""
                Refined_query = query.strip()
                # Parse the reasoning and decision (Simple string parsing)
                lines = response.split('\n')
        

                for line in lines:
                    if line.startswith("REASONING:"):
                       why_correction_needed = line.replace("REASONING:", "").strip()
                    if line.startswith("DECISION:"):
                       decision = line.upper()
                    if line.startswith("REFINED_QUERY:"):
                       refined_query = line.replace("REFINED_QUERY:", "").strip()

                crag_prompt = f"""
                You are a helpful assistant. Use the following PDF context to answer the question.
                Core instruction: You are a corective RAG system that evaluates retrieved context quality and correct retrieval when necessary

                STEP1: context evaluation:
                Evaluate context:
                Rate the following retrieved context for given query:
                Query : {query}
                Retrieved context:{context}

                Evaluate criteria: 
                Relevance score(0-1)
                Completeness score(0-1)
                Accuracy score(0-1)
                Specificity score(0-1)

                Overall quality: [Excellent,Good,Fair,Poor]

                STEP2:Correction decision
                Corrective logic
                if overall quality is Poor or Fair
                -Action : retrieve again
                -New query : {Refined_query}
                -Reasoning : {why_correction_needed}
                if overall quality is Excellent or Good
                -Action: proceed with answer
                -confidence :[High,Medium,Low]

                STEP3:Response generation
                Response fomat:
                Context quality: [Excellent,Good,Fair,Poor]   
                Confidence level:[High,Medium,Low]
                Answer: {response}
                """
                crag_prompt1 = f"""

                You are a specialized Retrieval Grader. Your goal is to assess the relevance of a retrieved document to a user question.

                CONTEXT:
                ----------
                {context}
                ----------

                USER QUESTION: {query}

                EVALUATION STEPS:
                1. Does the CONTEXT contain enough information to provide a factual, complete answer to the USER QUESTION?
                2. If yes, output the answer immediately.
                3. If no, or if the context is only tangentially related, you MUST start your response with the exact token: [TRIGGER_WEB_SEARCH]

                Strict Rule: Do not hallucinate. If the information is missing from the CONTEXT, trigger the web search.
                """
                

                # Try to get answer from PDF
                #grader_response = llm.invoke(crag_prompt).content.strip()
                grader_response = llm.invoke(crag_prompt).content.split("Answer:")

                if "[TRIGGER_WEB_SEARCH]" in grader_response:
                    st.info("🔍 PDF context is insufficient or ambiguous. Consulting the web...")
                                
                    # Fallback to SerpApi
                    search_result = search.run(query)
                    
                    # Refine the web result with LLM
                    # Final Synthesis: Pass the PDF context (even if weak) + Web data
                    synthesis_prompt = f"""
                    The user asked: {query}
                    We found some local data: {context}
                    We found some web data: {search_result}
                    Combine these to provide a comprehensive answer.
                    """
                    
                    #summary_prompt = f"The user asked: {query}. The web search returned: {search_result}. Summarize this concisely."
                    #final_answer = llm.invoke(summary_prompt)
                    final_answer = llm.invoke(synthesis_prompt)
                    st.subheader("Answer (Augment via Web)")
                    st.write(final_answer.content)

                else:
                    st.subheader("Answer (from PDF)")
                    st.write(grader_response['result'])

    else:
        st.error("No text found in PDF.")