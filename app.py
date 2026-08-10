import os

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_community.vectorstores import FAISS


# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env")
    st.stop()


# -----------------------------
# Gemini LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)


# -----------------------------
# Gemini Embeddings
# -----------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("📄 PDF Question Answering Chatbot")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


# -----------------------------
# Create Vector Store
# -----------------------------

@st.cache_resource
def create_vectorstore(file_path):

    # Load PDF
    loader = PyPDFLoader(file_path)

    documents = loader.load()


    # Split PDF into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)


    # Create embeddings + FAISS
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore


# -----------------------------
# Process Uploaded PDF
# -----------------------------

if uploaded_file is not None:

    # Save uploaded PDF
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())


    # Create vector store
    with st.spinner("Processing PDF..."):

        vectorstore = create_vectorstore("temp.pdf")


    st.success("PDF processed successfully!")


    # -----------------------------
    # Initialize Chat History
    # -----------------------------

    if "messages" not in st.session_state:

        st.session_state.messages = []


    # -----------------------------
    # Display Chat History
    # -----------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])


    # -----------------------------
    # Chat Input
    # -----------------------------

    question = st.chat_input(
        "Ask a question about the PDF"
    )


    if question:

        # -----------------------------
        # Display User Question
        # -----------------------------

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })


        with st.chat_message("user"):

            st.write(question)


        # -----------------------------
        # Create Conversation History
        # -----------------------------

        chat_history = ""

        for message in st.session_state.messages[:-1]:

            chat_history += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )


        # -----------------------------
        # Rewrite Question
        # -----------------------------

        rewrite_prompt = f"""
Given the conversation history below, rewrite the
user's latest question so that it is completely
standalone.

If the question is already clear, keep it unchanged.

Conversation history:
{chat_history}

Latest question:
{question}

Standalone question:
"""


        rewritten_question = llm.invoke(
            rewrite_prompt
        ).content


        # -----------------------------
        # Similarity Search
        # -----------------------------

        relevant_docs = vectorstore.similarity_search(
            rewritten_question,
            k=4
        )


        # -----------------------------
        # Create Context
        # -----------------------------

        context = "\n\n".join(
            doc.page_content
            for doc in relevant_docs
        )


        # -----------------------------
        # Final Prompt
        # -----------------------------

        prompt = f"""
You are a helpful PDF question-answering assistant.

Answer the user's question using ONLY the provided
PDF context.

If the answer is not present in the PDF context,
say that you cannot find the answer in the document.

PDF Context:
{context}

Conversation History:
{chat_history}

User Question:
{question}
"""


        # -----------------------------
        # Generate Answer
        # -----------------------------

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = llm.invoke(prompt)

                answer = response.content

                st.write(answer)


        # -----------------------------
        # Save Assistant Response
        # -----------------------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


    # -----------------------------
    # Clear Chat
    # -----------------------------

    if st.session_state.messages:

        if st.button("Clear Chat"):

            st.session_state.messages = []

            st.rerun()