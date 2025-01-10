import streamlit as st
from openai import OpenAI
import pandas as pd  # For handling CSV files if needed

# Show title and description.
st.title("💬 Vizier")
st.write(
    "This chatbot uses OpenAI's GPT-3.5 model to analyze documents and answer questions. "
    "Upload a document and ask questions about its contents. "
)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial system message
    st.session_state.messages.append({
        "role": "system",
        "content": "You are a helpful AI assistant. When provided with documents, you will analyze them and answer questions about their content."
    })

# Display existing chat messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# File upload widget in sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a document to analyze (optional)", type=["txt", "pdf"])

# Chat input
if prompt := st.chat_input("Ask a question"):
    # Get document content if file is uploaded
    document_content = None
    if uploaded_file:
        document_content = uploaded_file.getvalue().decode()
        
    # Create user message with document context if available
    user_message = prompt
    if document_content:
        user_message = f"Document content:\n{document_content}\n\nQuestion: {prompt}"
    
    # Add user message to chat history and display
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(prompt)  # Show only the question, not the document content
        
    # Generate assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
