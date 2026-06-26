import streamlit as st
from pypdf import PdfReader
import google.genai as genai

# 1. App Title and Interface Configuration
st.set_page_config(page_title="Industrial Knowledge Brain", layout="wide")
st.title("🏭 Industrial Knowledge Intelligence Platform")
st.subheader("Expert Knowledge Copilot for Operations & Safety")

# 2. Sidebar Layout for Setup
with st.sidebar:
    st.header("Setup & Ingestion")
    # A password field to keep your API key hidden securely
    api_key = st.text_input("Enter Gemini API Key", type="password")
    # File uploader widget that lets you drop industrial documents
    uploaded_files = st.file_uploader("Upload Industrial Documents (PDFs)", type=["pdf"], accept_multiple_files=True)

# 3. Code logic to read the uploaded PDFs
document_context = ""
if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            document_context += page.extract_text() + "\n"
    st.sidebar.success(f"Loaded {len(uploaded_files)} document(s) successfully!")

# 4. Main Chat Input Box
user_query = st.text_input("Ask an operational, safety, or compliance question:")

# 5. Core AI Processing Logic
if user_query:
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar.")
    elif not document_context:
        st.warning("Please upload at least one PDF manual first.")
    else:
        with st.spinner("Searching records and generating expert response..."):
            try:
                # Initialize connection to Google Gemini
                client = genai.Client(api_key=api_key)
                
                # Instruction to force the AI to act like an industrial expert and use citations
                prompt = f"""
                You are an Expert Industrial Knowledge Assistant. Your job is to answer the User Query using ONLY the provided Document Context.
                If the answer cannot be found in the context, say "I cannot find this in the uploaded records."
                Always provide exact source citations or section mentions based on the text.
                
                Document Context:
                {document_context}
                
                User Query: {user_query}
                """
                
                # Request a response from the AI model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # Print output nicely onto the web page
                st.markdown("### 🤖 Expert Assistant Response")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")