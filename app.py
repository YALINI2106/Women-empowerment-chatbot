import streamlit as st
import ollama
import chromadb
import os
from pypdf import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Women Empowerment AI Assistant",
    page_icon="👩",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
.main {
    background-color: #fdf7ff;
}

.stTextInput > div > div > input {
    border-radius: 10px;
    border: 2px solid #d946ef;
    padding: 10px;
}

.stButton button {
    background-color: #d946ef;
    color: white;
    border-radius: 10px;
}

.chat-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f3e8ff;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("👩 Women Empowerment AI Assistant")

st.markdown("""
Ask questions about:

- 🎓 Scholarships
- 🛡 Women Safety
- 🏛 Government Schemes
- 💼 Entrepreneurship
- 🧠 Mental Wellness
- 📚 Education & Career Guidance
""")

# ---------------- MODELS ----------------
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3"

# ---------------- CHROMADB ----------------
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="women_empowerment_collection"
)

# ---------------- PDF READER ----------------
def load_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {file_path}")
        st.error(e)
    return text

# ---------------- TEXT CHUNKING ----------------
def chunk_text(text, chunk_size=700):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size
    return chunks

# ---------------- PROCESS DATASET ----------------
@st.cache_resource
def process_all_pdfs():
    data_folder = "data"

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    pdf_files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]

    if len(pdf_files) == 0:
        st.warning("No PDF files found inside data folder.")
        return

    if collection.count() > 0:
        return

    progress_bar = st.progress(0)
    status_text = st.empty()

    all_chunks = []

    for pdf in pdf_files:
        pdf_path = os.path.join(data_folder, pdf)
        pdf_text = load_pdf(pdf_path)
        chunks = chunk_text(pdf_text)
        all_chunks.extend(chunks)

    for i, chunk in enumerate(all_chunks):
        status_text.text(f"Processing chunk {i+1}/{len(all_chunks)}")

        try:
            embedding = ollama.embed(
                model=EMBEDDING_MODEL,
                input=chunk
            )["embeddings"][0]

            collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[chunk]
            )

        except Exception as e:
            st.error(f"Embedding Error: {e}")

        progress_bar.progress((i + 1) / len(all_chunks))

    progress_bar.empty()
    status_text.empty()

# ---------------- RETRIEVAL ----------------
def retrieve_documents(query, top_k=5):
    try:
        query_embedding = ollama.embed(
            model=EMBEDDING_MODEL,
            input=query
        )["embeddings"][0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"][0]

    except Exception as e:
        st.error(f"Retrieval Error: {e}")
        return []

# ---------------- INIT DATA ----------------
with st.spinner("Loading Knowledge Base..."):
    process_all_pdfs()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📚 Knowledge Base")
    st.success(f"Stored Chunks: {collection.count()}")

    st.markdown("---")

    st.markdown("""
### 💡 Example Questions
- What scholarships are available for women?
- What is the women safety helpline?
- How can women start small businesses?
- What mental wellness support exists?
- Explain government schemes for women.
""")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "retrieved_docs" not in st.session_state:
    st.session_state.retrieved_docs = []

# ---------------- DISPLAY CHAT HISTORY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------
user_query = st.chat_input("Ask your question here...")

# ---------------- CHATBOT ----------------
if user_query:

    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    # ---------- RETRIEVE ----------
    retrieved_docs = retrieve_documents(user_query)
    st.session_state.retrieved_docs = retrieved_docs

    context = "\n".join(retrieved_docs)

    # ---------- PROMPT ----------
    system_prompt = f"""
You are a Women Empowerment AI Assistant.

Answer ONLY using the provided context.

If answer not found, say:
"I could not find relevant information in the knowledge base."

CONTEXT:
{context}
"""

    # ---------- AI RESPONSE ----------
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = ollama.chat(
                model=LANGUAGE_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                stream=True
            )

            for chunk in stream:
                token = chunk["message"]["content"]
                full_response += token
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error: {e}"
            st.error(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

# ---------------- RETRIEVED CONTEXT (SAFE) ----------------
with st.expander("📄 Retrieved Knowledge"):
    for i, doc in enumerate(st.session_state.retrieved_docs):
        st.markdown(f"### Context {i+1}")
        st.write(doc)
        st.markdown("---")