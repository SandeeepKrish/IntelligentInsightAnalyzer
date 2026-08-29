# 🔬 IntelligentInsightAnalyzer

A professional-grade data analysis application with AI-powered multi-turn conversations, powered by OpenAI and Streamlit.

## ✨ Features

- 🤖 **Multi-turn AI Conversations** - Ask follow-up questions with full context awareness
- 💬 **Streaming Responses** - See AI answers appear in real-time
- 📚 **Conversation Memory** - AI remembers previous questions in the session
- 📊 **Data Exploration** - Preview datasets and analyze distributions
- 🧹 **Data Quality** - Comprehensive data health metrics and column analysis
- 📈 **Custom Charts** - Create 5 different visualization types
- 🏗️ **Professional Architecture** - Clean separation of concerns with config, services, and components

## 🏗️ Project Structure

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
## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-...your-api-key...
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Architecture Overview

### **config/ - Configuration**
- **settings.py**: Centralized app configuration
  - OpenAI model settings
  - Conversation parameters
  - UI configuration
  - System prompts

### **services/ - Business Logic**
- **analyzer_service.py**: Main orchestrator
  - Data loading and preprocessing
  - Conversation management
  - LLM interaction
  - Data analysis operations

### **components/ - UI Components**
Each component is a reusable Streamlit function:
- **chat_interface.py**: Multi-turn chat with streaming
- **data_explorer.py**: Dataset preview and distribution analysis
- **data_quality.py**: Quality metrics and insights
- **charts.py**: 5 chart types (Pie, Bar, Scatter, Line, Box)

### **utils/ - Core Utilities**
- **memory.py**: Conversation context management
- **llm.py**: Streaming LLM interface
- **data_analyzer.py**: Data profiling and statistics

### **app.py - Entry Point**
Minimal (~140 lines) that:
- Initializes Streamlit
- Creates AnalyzerService
- Renders components in tabs
- Handles sidebar file upload

## 💬 Usage Examples

### Uploading Data
1. Click the file uploader in the sidebar
2. Select a CSV or Excel file
3. Wait for data to load (shows row count, columns, quality score)

### Asking Questions
1. Go to the "AI Chat" tab
2. Type your question about the data
3. AI responds with specific insights from your dataset
4. Ask follow-up questions - AI remembers context!

### Example Questions
- "What's the average sales value?"
- "Which region has the most customers?"
- "Show me the distribution of customer ages"
- "What's the data quality score?"
- "List unique products in the dataset"

### Creating Visualizations
1. Go to the "Charts" tab
2. Select chart type
3. Choose columns for your visualization
4. Chart renders immediately

## 🔧 Configuration

Edit `src/config/settings.py` to customize:

```python
# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 1000

# Conversation Settings
MAX_CONVERSATION_MESSAGES = 20
RECENT_CONTEXT_WINDOW = 6

# UI Settings
CHART_TYPES = ["Pie Chart", "Bar Chart", "Scatter Plot", "Line Chart", "Box Plot"]
```

## 📦 Dependencies

- **streamlit** - Web UI framework
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **plotly** - Interactive charts
- **openai** - OpenAI API client
- **python-dotenv** - Environment configuration

## 🔐 Security

- API key stored locally in `.env` (never committed)
- `.gitignore` prevents secret leakage
- `.env.example` shows configuration template
- No API keys in code

## 🎨 UI/UX

### ChatGPT-style Interface
- Conversation history displayed above
- Input field at the bottom
- Real-time streaming responses
- Clear user/assistant distinction

### Multi-tab Design
- **💬 AI Chat** - Main conversation interface
- **📊 Data Explorer** - Dataset preview and analysis
- **🧹 Data Quality** - Data health metrics
- **📈 Charts** - Custom visualizations

## 🔄 Data Flow

```
User Upload
    ↓
AnalyzerService.load_data()
    ↓
Service prepares data context
    ↓
User asks question
    ↓
ConversationMemory stores message
    ↓
StreamingLLM generates response
    ↓
Response streamed to UI in real-time
    ↓
Response stored in memory
```

## 📝 Example: Adding a New Component

1. Create `src/components/new_feature.py`:

```python
import streamlit as st
from services import AnalyzerService

def render_new_feature(service: AnalyzerService):
    st.subheader("New Feature")
    # Your component code here
```

2. Add to `src/components/__init__.py`:

```python
from .new_feature import render_new_feature
__all__ = [..., "render_new_feature"]
```

3. Use in `app.py`:

```python
with tab_new:
    render_new_feature(service)
```

## 🚀 Future Enhancements

- [ ] Advanced SQL generation from natural language
- [ ] Anomaly detection in data
- [ ] Time series forecasting
- [ ] PDF/PPT report generation
- [ ] Multi-file joins and analysis
- [ ] User authentication
- [ ] Database persistence
- [ ] Custom model fine-tuning

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Support

For issues or questions, please check:
1. Ensure `.env` file has valid `OPENAI_API_KEY`
2. Check that dependencies are installed: `pip install -r requirements.txt`
3. Verify data file is in supported format (CSV/Excel)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [OpenAI](https://openai.com)
- Data visualization with [Plotly](https://plotly.com)

---

**Version**: 2.0.0  
**Last Updated**: August 2026
