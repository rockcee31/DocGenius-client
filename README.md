📘 DocGenius Frontend
DocGenius is a smart PDF-based AI assistant. Upload a PDF, ask questions about its content, and get contextual, page-linked answers – powered by LangChain, OpenAI, and Qdrant.

This is the frontend for the DocGenius project.
The backend is built using FastAPI and is required to run this frontend.

🚀 Features
Upload PDF documents

Ask questions about the uploaded content

Get AI-generated answers with page references

Clean, interactive chat interface

🛠️ Tech Stack
React (Vite or CRA)

Tailwind CSS (or your preferred CSS framework)

Axios for API calls

FastAPI backend (not included here – see backend repo)

📦 Installation
Clone this repository

bash
Copy
Edit
git clone https://github.com/yourusername/docgenius-frontend.git
cd docgenius-frontend
Install dependencies

bash
Copy
Edit
npm install
Set up environment variables

Create a .env file in the root:

env
Copy
Edit
VITE_API_BASE_URL=http://localhost:8000
Adjust the port if your FastAPI backend runs elsewhere.

🧪 Run Locally
bash
Copy
Edit
npm run dev
Open http://localhost:5173 in your browser.

🧩 Folder Structure
bash
Copy
Edit
docgenius-frontend/
├── src/
│   ├── components/
│   │   ├── FileUpload.jsx
│   │   └── ChatBox.jsx
│   ├── App.jsx
│   └── main.jsx
├── public/
├── .env
└── README.md
📤 API Endpoints (used by frontend)
POST /upload – Upload PDF (multipart/form-data)

POST /chat – Send messages as JSON:

json
Copy
Edit
{
  "messages": [
    { "role": "user", "content": "What is this PDF about?" }
  ]
}
🧠 Future Improvements
Chat history persistence

Drag-and-drop upload

Better error handling

Dark mode UI

🤝 Contribution
Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

