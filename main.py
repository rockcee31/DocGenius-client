import streamlit as st
import requests

st.set_page_config(page_title="DocGenius", layout="wide")
st.title("📄 DocGenius - Intelligent PDF Chat")

# Session state setup
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "messages" not in st.session_state:
    st.session_state.messages = []

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
                        st.success("✅ PDF uploaded successfully.")
                        st.session_state.uploaded = True
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

    # Chat input
    if prompt := st.chat_input("Ask something about the PDF..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post("https://docgenius-backend-voiu.onrender.com/chat", json={"messages": st.session_state.messages})
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No response.")
                    else:
                        answer = f"Error: {response.status_code}"
                except Exception as e:
                    answer = f"Error: {str(e)}"

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # Optional reset button
    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.experimental_rerun()
