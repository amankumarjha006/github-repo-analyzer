# GitHub Repo Analyzer

A structured project containing a **Next.js frontend** and a **FastAPI backend**.

## Repository Structure

```
github-repo-analyzer/
├── frontend/             # Next.js Application (React 19, TypeScript, TailwindCSS v4)
├── backend/              # FastAPI Application (Python 3.14+, Pydantic v2)
│   ├── app/
│   │   └── main.py       # FastAPI Entry Point
│   ├── venv/             # Python Virtual Environment
│   └── requirements.txt  # Backend Dependencies
├── .gitignore            # Root gitignore rules
└── README.md             # Project documentation (this file)
```

---

## Getting Started

### Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment (Windows):
   ```powershell
   venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   > [!IMPORTANT]
   > Use the virtual environment's `uvicorn` explicitly to ensure all modules are loaded with the correct path configuration:
   ```powershell
   venv\Scripts\uvicorn app.main:app --reload
   ```
   The backend will be available at `http://127.0.0.1:8000`. You can access the auto-generated documentation at `http://127.0.0.1:8000/docs`.

---

### Frontend Setup (Next.js)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.
