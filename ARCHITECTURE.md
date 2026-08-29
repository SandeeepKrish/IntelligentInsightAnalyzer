# Project Architecture

## Overview

IntelligentInsightAnalyzer is structured with a clear separation between **Frontend** (Streamlit UI) and **Backend** (Business Logic).

```
IntelligentInsightAnalyzer/
│
├── frontend/                 # User Interface Layer
│   ├── app.py               # Entry point (Streamlit app)
│   ├── .streamlit/          # Streamlit config
│   └── requirements.txt      # UI dependencies
│
├── backend/                  # Business Logic Layer
│   ├── src/
│   │   ├── config/          # Configuration
│   │   ├── services/        # Service orchestration
│   │   ├── components/      # UI render functions
│   │   └── utils/           # Core utilities
│   └── requirements.txt      # Logic dependencies
│
├── requirements.txt          # Combined dependencies
├── .env                      # Environment variables (API keys)
├── .streamlit/              # Streamlit settings
└── README.md                # Project documentation
```

## Architecture Layers

### Frontend (Streamlit)
**Responsibility:** User interface and interaction

- Renders pages and tabs
- Handles file uploads
- Displays charts and tables
- Manages theme (light/dark)
- Orchestrates user interactions

**Technologies:**
- Streamlit (web framework)
- Plotly (interactive charts)
- Session state (persistence)

**Entry Point:** `frontend/app.py`

```bash
cd frontend
streamlit run app.py
```

### Backend (Business Logic)
**Responsibility:** Data processing, analysis, and AI interaction

- Load and process CSV/Excel/PDF files
- Run data analysis operations
- Manage conversation history
- Call OpenAI API for AI responses
- Extract statistics and metrics

**Technologies:**
- Pandas (data manipulation)
- OpenAI (LLM API)
- PyPDF2 (PDF extraction)

**Main Service:** `backend/src/services/analyzer_service.py`

## Data Flow

```
User Input (Frontend)
    ↓
Streamlit App (Frontend)
    ↓
AnalyzerService (Backend)
    ↓
Utility Functions (Backend)
    ↓
OpenAI API / Data Analysis
    ↓
Results (Backend)
    ↓
Display (Frontend)
    ↓
User Output
```

## Running the Project

### Option 1: Run Frontend Only (Recommended)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Install All Dependencies
```bash
pip install -r requirements.txt
cd frontend
streamlit run app.py
```

## File Organization

### Frontend Files
- UI components and Streamlit configuration
- Session state management
- Chart rendering calls

### Backend Files
- Data processing logic
- Analysis algorithms
- External API interactions (OpenAI)
- File handling (CSV, Excel, PDF)

## Benefits of This Structure

✅ **Separation of Concerns** - UI logic separate from business logic  
✅ **Scalability** - Easy to add more frontend or backend features  
✅ **Testing** - Backend can be tested independently  
✅ **Maintainability** - Clear file organization and responsibilities  
✅ **Reusability** - Backend can be used by other frontends (e.g., web, mobile)  
✅ **Dependency Management** - Frontend and backend have independent requirements  

## Environment Variables

Create `.env` file in project root:

```
OPENAI_API_KEY=sk-proj-your-key-here
```

## Configuration

Streamlit config: `frontend/.streamlit/config.toml`
App config: `backend/src/config/settings.py`
