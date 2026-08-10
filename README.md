# 📄 Document QnA Bot

A PDF Question Answering chatbot built using **Python, LangChain, Google Gemini, FAISS, and Streamlit**.

The application allows users to upload a PDF and ask questions about its content. It uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information from the document and generate context-aware answers using Google Gemini.

---
## 📸 Screenshots

### PDF QnA Chatbot
### Question Answering

<img width="1469" height="885" alt="QAchat2" src="https://github.com/user-attachments/assets/9b0a04ab-2ab0-4917-a8b6-7869f4e2aa5f" />

<img width="1469" height="885" alt="QAchat1" src="https://github.com/user-attachments/assets/1632c234-45d1-4e66-bc25-af6e155ece34" />



## 🚀 Features

- 📄 Upload PDF documents
- 📖 Extract text from PDFs
- ✂️ Split documents into smaller chunks
- 🧠 Generate embeddings using Google Gemini
- 🔎 Semantic similarity search using FAISS
- 🤖 Generate answers using Gemini
- 💬 Conversational chat interface
- 🧾 Maintain conversation history
- 🔄 Rewrite follow-up questions into standalone questions
- ⚡ Cache the vector store using Streamlit
- 🗑️ Clear chat history

---

## ��️ RAG Architecture

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




