# Backend - Business Logic

This is the business logic layer of the IntelligentInsightAnalyzer application.

## Structure

```
backend/
├── src/
│   ├── config/          # Configuration settings (AppConfig)
│   ├── services/        # Service layer (AnalyzerService, PDF handling)
│   ├── components/      # UI components (render functions for Streamlit)
│   └── utils/           # Core utilities (LLM, data analysis, memory, PDF handler)
└── requirements.txt     # Backend-only dependencies
```

## Dependencies

- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `openai` - LLM API client
- `openpyxl` - Excel file reading
- `PyPDF2` - PDF text extraction
- `python-dotenv` - Environment variables

## Module Overview

### config/
- `settings.py` - Centralized configuration (API keys, models, constants)

### services/
- `analyzer_service.py` - Main service orchestrating all operations
  - Data loading (CSV, Excel)
  - PDF document handling
  - Chat responses
  - Data quality metrics

### components/
- `advanced_analysis.py` - Multiple analysis types (Group, Temporal, Distribution, etc.)
- `charts.py` - Chart rendering
- `chat_interface.py` - Chat UI
- `data_explorer.py` - Data exploration UI
- `data_quality.py` - Data quality display
- `theme_toggle.py` - Theme switching

### utils/
- `analysis_engine.py` - Data analysis operations (grouping, filtering, aggregation)
- `analysis_templates.py` - Pre-built analysis templates
- `data_analyzer.py` - Data summary and statistics
- `llm.py` - OpenAI API wrapper with streaming
- `memory.py` - Conversation memory management
- `pdf_handler.py` - PDF text extraction
- `theme.py` - Theme definitions

## How it works

1. Frontend (Streamlit) imports backend modules
2. Frontend creates AnalyzerService instance
3. Frontend calls backend methods for:
   - Loading data
   - Running analyses
   - Streaming AI responses
   - Processing PDFs
4. Backend returns results to frontend for display
