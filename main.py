import streamlit as st
import requests

st.set_page_config(page_title="DocGenius", layout="wide")
st.title("📄 DocGenius - Intelligent PDF Chat")

# Session state setup — only set default once
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None  # Store user's unique collection name

# Cache the chat response to avoid duplicate calls during reruns
@st.cache_data(show_spinner=False)
def fetch_chat_response(messages, collection_name):
    try:
        payload = {
            "messages": messages,
            "collection_name": collection_name
        }
        response = requests.post(
            "https://docgenius-backend-voiu.onrender.com/chat", json=payload
        )
        if response.status_code == 200:
            return response.json().get("answer", "No response.")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# --------------------------
# 📁 Step 1: Upload PDF File
# --------------------------
if not st.session_state.uploaded:
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if st.button("Submit"):
        if uploaded_file:
            with st.spinner("Uploading..."):
                files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                try:
                    res = requests.post("https://docgenius-backend-voiu.onrender.com/upload", files=files)
                    if res.status_code == 200:
                        result = res.json()
                        collection_name = result.get("collection_name")
                        if collection_name:
                            st.session_state.collection_name = collection_name  # Save collection name
                            st.success("✅ PDF uploaded successfully.")
                            st.session_state.uploaded = True
                        else:
                            st.error("❌ Upload succeeded but no collection name returned.")
                    else:
                        st.error(f"❌ Upload failed: {res.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please select a PDF file before submitting.")

# ---------------------------------
# 💬 Step 2: Chat UI after Upload
# ---------------------------------
if st.session_state.uploaded:
    st.subheader("🗣️ Chat with your document")

    # Show previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input and response handling — only update session state inside this block
    prompt = st.chat_input("Ask something about the PDF...")
    if prompt:
        # Append user message once when prompt submitted
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # Get cached or new response from backend
        with st.spinner("Thinking..."):
            answer = fetch_chat_response(st.session_state.messages, st.session_state.collection_name)
            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # Optional reset button
    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.experimental_rerun()
