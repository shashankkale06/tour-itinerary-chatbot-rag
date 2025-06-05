# Tour Itinerary Chatbot

This project implements an **AI-powered chatbot** designed to assist users in answering travel-related questions using **Retrieval-Augmented Generation (RAG)**. The chatbot processes PDF documents (e.g., travel brochures, itineraries, city guides) to provide contextually accurate responses about tourist attractions, sightseeing recommendations, and more. The chatbot leverages **Google Gemini's generative capabilities** and **TF-IDF-based document retrieval** to answer queries efficiently.

## Features

- **PDF Upload**: Users can upload a travel-related PDF document (e.g., itinerary, travel guide).
- **Travel Query Answering**: Users can ask questions related to travel, and the bot will generate answers based on the content of the uploaded document.
- **Contextual Response Generation**: The chatbot uses **Retrieval-Augmented Generation (RAG)** by retrieving relevant document chunks and generating a response using **Google Gemini**.
- **Chat History**: The chatbot maintains a session-based chat history to allow users to view past queries and responses.
- **Polite Error Handling**: If the document content is not related to tourism, the bot responds with a polite message.

## Technologies Used

- **Google Gemini API**: Provides access to the large language model (LLM) for content generation and answering user queries.
- **Streamlit**: Framework used for building the user interface and enabling real-time interaction.
- **PyMuPDF (fitz)**: Library used for extracting text from uploaded PDF documents.
- **scikit-learn**: Provides **TF-IDF** vectorization for converting text into numeric vectors and **cosine similarity** for document retrieval.

## How It Works

1. **PDF Upload**: Users upload a PDF document (travel brochure, itinerary, or guide).
2. **Text Extraction**: The text from the PDF is extracted using **PyMuPDF (fitz)**.
3. **Text Chunking**: The extracted text is split into smaller chunks for more efficient processing.
4. **User Query**: Users enter their travel-related questions in the input field.
5. **Document Retrieval**: The chatbot uses **TF-IDF** and **cosine similarity** to retrieve the most relevant document chunks based on the user's query.
6. **Answer Generation**: The **Google Gemini API** generates an answer using the retrieved context and the user's question.
7. **Display Results**: The generated answer is shown to the user, along with the context from the document that was used to generate the answer.
8. **Chat History**: The chatbot maintains a session-based chat history to track the interaction.

## Installation

To run this chatbot locally, follow these steps:

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/tour-itinerary-chatbot-rag.git
cd tour-itinerary-chatbot-rag
