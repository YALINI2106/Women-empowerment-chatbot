
**👩 Women Empowerment Chatbot (RAG AI Assistant)**

An AI-powered chatbot built using Streamlit, Ollama, ChromaDB, and Python that helps users get reliable information about women empowerment topics using a Retrieval-Augmented Generation (RAG) system.

**🚀 Features**

💬 AI chatbot with streaming responses
📚 Uses PDF-based knowledge base
🔍 Semantic search with ChromaDB
🧠 RAG-based response generation (context-aware answers)
📄 View retrieved knowledge sources
🎨 Simple and clean Streamlit UI

**🛠️ Tech Stack**

Streamlit (Frontend UI)
Ollama (LLM + Embeddings)
ChromaDB (Vector Database)
PyPDF (PDF processing)
Python

**⚙️ Setup Instructions**

1️⃣ Clone the repository
git clone https://github.com/YALINI2106/Women-empowerment-chatbot.git
cd Women-empowerment-chatbot
2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Install Ollama models
ollama pull llama3
ollama pull nomic-embed-text
5️⃣ Run the app
streamlit run app.py

**📌 How it works**

PDFs are loaded from data/ folder
Text is split into chunks
Each chunk is converted into embeddings
Stored in ChromaDB vector database
User query is embedded and matched with stored data
Relevant context is sent to LLM (LLaMA3)
AI generates grounded response

**💡 Example Questions**

What scholarships are available for women?
What government schemes support women?
How can women start businesses?
What are safety helplines for women?

**⚠️ Note
**
The chatbot only answers based on the provided knowledge base.
If no relevant context is found, it will respond appropriately.
