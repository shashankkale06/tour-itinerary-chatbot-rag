import streamlit as st
import os
import fitz  
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
rag_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# === PDF Handling ===
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# === Chunking Text ===
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# === Retrieve Top Chunks ===
def retrieve_top_chunks(query, chunks, k=3):
    vect = TfidfVectorizer().fit(chunks + [query])
    vectors = vect.transform(chunks + [query])
    similarities = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    top_indices = similarities.argsort()[-k:][::-1]
    return [chunks[i] for i in top_indices]

# === Generate Answer with Context ===
def generate_rag_response(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""
You are a helpful **travel itinerary assistant**. Only answer questions related to tourism, travel, sightseeing, planning trips, or city guides.

If the user's query or the context is unrelated to travel, politely respond with:
"Sorry! The document or query does not appear to be related to tourism or travel."

Context:
{context}

User Query:
{query}

Answer:
"""
    response = rag_model.generate_content(prompt)
    return response.text.strip()

# === Initialize session chat history ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Streamlit UI ===
st.set_page_config(page_title="Tour Itinerary Chatbot", layout="wide")
st.title("🌍 Tour Itinerary Chatbot")

uploaded_pdf = st.file_uploader("Upload a travel brochure, itinerary PDF, or guide:", type="pdf")

if uploaded_pdf:
    text = extract_text_from_pdf(uploaded_pdf)
    chunks = chunk_text(text)
    st.success(f"✅ Extracted and chunked into {len(chunks)} sections.")

    with st.form("query_form", clear_on_submit=True):
        query = st.text_input("Ask your travel question:")
        submitted = st.form_submit_button("Submit")

    if submitted and query:
        top_chunks = retrieve_top_chunks(query, chunks)
        with st.spinner("Generating response..."):
            answer = generate_rag_response(query, top_chunks)

        # Save conversation to history
        st.session_state.chat_history.append(("You", query))
        st.session_state.chat_history.append(("Bot", answer))

# === Display chat history ===
if st.session_state.chat_history:
    st.markdown("### 🕓 Chat History")
    for role, message in st.session_state.chat_history:
        align = "right" if role == "You" else "left"
        color = "#1a73e8" if role == "You" else "#34a853"
        st.markdown(f"""
            <div style='text-align:{align}; color:{color}; padding:5px; margin-bottom:8px;'>
                <b>{role}:</b> {message}
            </div>
        """, unsafe_allow_html=True)

# === Clear chat button ===
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
