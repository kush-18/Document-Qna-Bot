# 📄 Document QnA Bot

A PDF Question Answering chatbot built using **Python, LangChain, Google Gemini, FAISS, and Streamlit**.

The application allows users to upload a PDF and ask questions about its content. It uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information from the document and provide context-aware answers using Google Gemini.

---

## 🚀 Features

- 📄 Upload PDF documents
- 📖 Extract text from PDFs
- ✂️ Split documents into smaller chunks
- 🧠 Generate embeddings using Google Gemini
- 🔎 Semantic similarity search using FAISS
- 🤖 Answer questions using Gemini
- 💬 Conversational chat interface
- 🧾 Maintain conversation history
- 🔄 Rewrite follow-up questions into standalone questions
- ⚡ Cache the vector store using Streamlit
- 🗑️ Clear chat history

---

## 🏗️ RAG Pipeline

```text
PDF Upload
     ↓
PyPDFLoader
     ↓
Document Text
     ↓
Recursive Character Text Splitter
     ↓
Text Chunks
     ↓
Gemini Embeddings
     ↓
FAISS Vector Store
     ↓
User Question
     ↓
Conversation History
     ↓
Question Rewriting
     ↓
Similarity Search
     ↓
Relevant PDF Chunks
     ↓
Gemini LLM
     ↓
Generated Answer
