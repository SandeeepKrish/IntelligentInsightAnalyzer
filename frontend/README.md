# Frontend - Streamlit UI

This is the user interface layer of the IntelligentInsightAnalyzer application.

## Structure

```
frontend/
├── app.py              # Main Streamlit application entry point
├── .streamlit/         # Streamlit configuration
│   ├── config.toml     # Theme and display settings
│   └── secrets.toml    # API keys (local only, not committed)
└── requirements.txt    # Frontend-only dependencies
```

## Dependencies

- `streamlit` - Web UI framework
- `plotly` - Interactive charts
- `python-dotenv` - Environment variables

## Running

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

The app will start at `http://localhost:8501`

## How it works

1. User opens Streamlit app in browser
2. Frontend imports backend modules from `../backend/src`
3. User uploads files, sees charts, chats with AI
4. All UI is rendered by Streamlit
5. All logic calls are made to backend services
