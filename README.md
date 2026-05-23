👩 Women Empowerment AI Assistant

An AI-powered Retrieval-Augmented Generation (RAG) chatbot built using Streamlit, Ollama, and ChromaDB.
It helps users get reliable information about women empowerment topics like scholarships, safety, government schemes, entrepreneurship, mental wellness, and education.

🚀 Features
📚 Upload and process PDF-based knowledge base
🧠 Semantic search using embeddings (Ollama + ChromaDB)
💬 AI chatbot with streaming responses (LLaMA3)
🔎 Context-aware answers using RAG pipeline
📄 View retrieved knowledge sources
🎨 Clean and styled Streamlit UI
💾 Persistent vector database storage
🏗️ Tech Stack
Frontend: Streamlit
LLM: Ollama (LLaMA3)
Embeddings: nomic-embed-text
Vector DB: ChromaDB
PDF Processing: PyPDF
Language: Python
📁 Project Structure
project/
│── app.py
│── data/
│     ├── file1.pdf
│     ├── file2.pdf
│── chroma_db/
│── requirements.txt
│── README.md
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/women-empowerment-ai.git
cd women-empowerment-ai
2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Install & setup Ollama
Install Ollama: https://ollama.com
Pull required models:
ollama pull llama3
ollama pull nomic-embed-text
5️⃣ Add PDF files

Place your datasets inside:

data/
6️⃣ Run the app
streamlit run app.py
💡 How It Works
PDFs are loaded from data/ folder
Text is split into chunks
Each chunk is converted into embeddings using Ollama
Stored in ChromaDB vector database
User query is embedded and matched with relevant chunks
Context is sent to LLaMA3 model
AI generates response based only on retrieved context
📌 Example Questions
What scholarships are available for women?
How can women start small businesses?
What are government schemes for women?
What is the women safety helpline number?
What mental wellness support is available?
⚠️ Rules of the Assistant
Answers ONLY from provided knowledge base
No hallucinated or fake information

If no context is found → returns:

"I could not find relevant information in the knowledge base."

📄 Dependencies

Create a requirements.txt:

streamlit
ollama
chromadb
pypdf
🧠 Future Improvements
Multi-language support
Web scraping for dynamic data
User authentication system
Better chunking strategy (semantic splitting)
Advanced UI dashboard
