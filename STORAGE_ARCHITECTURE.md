# 🏗️ Storage Architecture Diagram

## File Upload & Storage Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER UPLOADS FILE                           │
│                                                                  │
│    Excel/CSV file   OR    PDF file                              │
│    (sales.csv)            (report.pdf)                          │
└────────────────┬───────────────────────────┬────────────────────┘
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌──────────────────┐
        │ Streamlit       │         │ Streamlit        │
        │ file_uploader() │         │ file_uploader()  │
        │                 │         │                  │
        │ Returns: bytes  │         │ Returns: bytes   │
        └────────┬────────┘         └────────┬─────────┘
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌──────────────────┐
        │ pd.read_csv()   │         │ PDFHandler       │
        │ pd.read_excel() │         │ .extract_text()  │
        │                 │         │ .get_metadata()  │
        │ Returns:        │         │                  │
        │ DataFrame       │         │ Returns:         │
        │ (1000 rows)     │         │ text + metadata  │
        └────────┬────────┘         └────────┬─────────┘
                 │                           │
                 ▼                           ▼
    ┌──────────────────────────┬───────────────────────────┐
    │                          │                           │
    │  Store in RAM            │  Store in RAM             │
    │  AnalyzerService         │  AnalyzerService          │
    │                          │                           │
    │  self.current_dataframe  │  self.pdf_documents = {   │
    │  ├─ 5 MB                 │    "report.pdf": {        │
    │  │  (DataFrame in RAM)   │      "content": bytes,    │
    │  │                       │      "text": string,      │
    │  └─ Stays in RAM         │      "metadata": {...}    │
    │     for session          │    }                      │
    │                          │  }                        │
    │  self.data_context       │                           │
    │  ├─ 50 KB                │  self.current_pdf         │
    │  │  (Summary text)       │  = "report.pdf"           │
    │  └─ Used for AI          │                           │
    │     analysis             │  Stays in RAM             │
    │                          │  for session              │
    └──────────────────────────┴───────────────────────────┘
                              │
                              ▼
                   ┌────────────────────┐
                   │  SESSION DURATION  │
                   │                    │
                   │  User can chat,    │
                   │  analyze, query    │
                   │  the uploaded      │
                   │  files             │
                   │                    │
                   │ ← Data stays in ← 
                   │   RAM until...     │
                   └────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌──────────────┐        ┌──────────────┐
        │ User presses │        │ Browser      │
        │ Clear button │        │ refreshes    │
        │              │        │              │
        │ Call:        │        │ Session ends │
        │ service.     │        │              │
        │ clear_pdfs() │        │ Session      │
        │              │        │ destroyed    │
        └────────┬─────┘        └────────┬─────┘
                 │                       │
                 └───────────┬───────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │ RAM MEMORY CLEARED  │
                    │                     │
                    │ All data deleted    │
                    │ Not on disk         │
                    │ Nothing to recover  │
                    └─────────────────────┘
```

---

## Memory Storage Structure

```
┌──────────────────────────────────────────────────────────────────┐
│                  STREAMLIT SESSION STATE                         │
│                  (Server RAM Memory)                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  st.session_state:                                               │
│  ├── file_loaded (bool)                                          │
│  └── theme (string)                                              │
│                                                                  │
│  AnalyzerService instance:                                       │
│  ├── current_dataframe (pandas.DataFrame)                        │
│  │   ├── 1000 rows × 5 columns ← Your Excel/CSV data            │
│  │   ├── Data types: int, float, string                          │
│  │   └── Size: ~5 MB                                             │
│  │                                                                │
│  ├── data_context (string)                                       │
│  │   ├── Dataset summary for AI                                  │
│  │   ├── Row count, column stats                                 │
│  │   ├── Sample data                                             │
│  │   └── Size: ~50 KB                                            │
│  │                                                                │
│  ├── pdf_documents (dict)                                        │
│  │   ├── "report.pdf": {                                         │
│  │   │   ├── "content": bytes (3 MB)                             │
│  │   │   ├── "text": string (500 KB)                             │
│  │   │   └── "metadata": dict (1 KB)                             │
│  │   ├── "analysis.pdf": { ... }                                 │
│  │   └── ...                                                      │
│  │                                                                │
│  ├── current_pdf (string)                                        │
│  │   └── "report.pdf" ← Currently selected                       │
│  │                                                                │
│  ├── conversation_memory:                                        │
│  │   ├── messages (list of 20 dicts)                             │
│  │   ├── [{role, content, timestamp}, ...]                       │
│  │   ├── max_messages: 20                                        │
│  │   └── Size: ~100 KB                                           │
│  │                                                                │
│  ├── llm (StreamingLLM instance)                                 │
│  │   └── Lightweight API wrapper                                 │
│  │                                                                │
│  └── data_analyzer (DataAnalyzer instance)                       │
│      └── Lightweight analysis helper                             │
│                                                                  │
│  TOTAL RAM USAGE: ~9 MB                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Location Timeline

```
Timeline of a typical session:

15:00:00 ┌─ User opens app
         │  RAM: ~1 MB (empty service instance)
         │
15:00:30 ├─ User uploads sales.csv (5 MB file)
         │  RAM: ~6 MB (DataFrame loaded)
         │       service.current_dataframe = pandas.DataFrame(...)
         │       service.data_context = "Dataset summary..."
         │
15:01:00 ├─ User uploads report.pdf (3 MB file)
         │  RAM: ~9 MB (DataFrame + PDF text extracted)
         │       service.pdf_documents["report.pdf"] = {content, text, metadata}
         │       service.current_pdf = "report.pdf"
         │
15:02:00 ├─ User asks: "What's in this PDF?"
         │  RAM: ~9.1 MB (+ small message in memory)
         │       service.conversation_memory.messages = [{...}, {...}]
         │
15:05:00 ├─ User analyzes data (5 messages in chat)
         │  RAM: ~9.2 MB (messages accumulating)
         │       service.conversation_memory.messages = [{...}, {...}, ...]
         │
15:10:00 ├─ User clicks "Clear Data File"
         │  RAM: ~3 MB (DataFrame removed)
         │       service.current_dataframe = None
         │       service.data_context = ""
         │
15:15:00 ├─ User clicks "Clear All PDFs"
         │  RAM: ~1 MB (PDFs removed)
         │       service.pdf_documents = {}
         │       service.current_pdf = None
         │
15:20:00 ├─ User closes browser
         │  RAM: 0 MB (session terminated, OS reclaims memory)
         │       ALL data deleted
         │       Nothing on disk
         │

QUESTION: "Where did the data go?"
ANSWER:   "It was only in RAM, which is now freed for other uses"
```

---

## Comparison: Excel vs PDF Storage

```
┌─────────────────┬──────────────────┬──────────────────┐
│ Aspect          │ Excel/CSV        │ PDF              │
├─────────────────┼──────────────────┼──────────────────┤
│ Upload Method   │ file_uploader()  │ file_uploader()  │
│                 │                  │                  │
│ Processing      │ pd.read_csv()    │ PyPDF2.extract() │
│                 │ pd.read_excel()  │                  │
│                 │                  │                  │
│ Storage Key     │ current_         │ pdf_documents    │
│                 │ dataframe        │ [filename]       │
│                 │                  │                  │
│ Storage Value   │ pandas.          │ {content,        │
│                 │ DataFrame        │  text,           │
│                 │                  │  metadata}       │
│                 │                  │                  │
│ Access Method   │ service.         │ service.         │
│                 │ get_dataframe()  │ get_pdf_text()   │
│                 │                  │ get_pdf_names()  │
│                 │                  │                  │
│ Chat Usage      │ Full data as     │ 3000 chars max   │
│                 │ context          │ of text          │
│                 │                  │                  │
│ Clear Method    │ Clear Data File  │ Clear All PDFs   │
│                 │ button           │ button           │
│                 │                  │                  │
│ Storage         │ RAM (memory)     │ RAM (memory)     │
│ Location        │                  │                  │
│                 │ Deleted on:      │ Deleted on:      │
│                 │ - Clear button   │ - Clear button   │
│                 │ - Page refresh   │ - Page refresh   │
│                 │ - Browser close  │ - Browser close  │
│                 │                  │                  │
│ Saved to Disk?  │ NO               │ NO               │
└─────────────────┴──────────────────┴──────────────────┘
```

---

## Code Reference Points

### Excel/CSV Storage:
```
File: src/services/analyzer_service.py

Line 76-77:  Instance variables
  self.current_dataframe = None
  self.data_context = ""

Line 79-90:  Load method
  def load_data(self, filename: str, file_data: bytes) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_data))  ← Loaded into RAM
    else:
        df = pd.read_excel(io.BytesIO(file_data))  ← Loaded into RAM
    
    self.current_dataframe = df  ← Stored here
    self.data_context = self.data_analyzer.get_data_summary(df)  ← Summary
```

### PDF Storage:
```
File: src/services/analyzer_service.py

Line 77:     Instance variable
  self.pdf_documents = {}

Line 209-248: Load method
  def load_pdf(self, filename: str, file_data: bytes):
    metadata = PDFHandler.get_pdf_metadata(file_data)
    text = PDFHandler.extract_text_from_pdf(file_data)
    
    self.pdf_documents[filename] = {  ← Stored here in RAM
        "content": file_data,         ← Original bytes
        "text": text,                 ← Extracted text
        "metadata": metadata          ← Metadata dict
    }
```

### Conversation Storage:
```
File: src/utils/memory.py

Line 32:     Instance variable
  self.messages: List[Dict[str, str]] = []

Line 40-51:  Add message method
  def add_message(self, role: str, content: str) -> None:
    self.messages.append({  ← Stored in RAM
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    
    if len(self.messages) > self.max_messages:
        self.messages = self.messages[-self.max_messages:]  ← Auto cleanup
```

---

## Summary Table

| Question | Answer |
|----------|--------|
| **Where is my Excel file?** | In RAM (memory) as `service.current_dataframe` |
| **Where is my PDF file?** | In RAM as `service.pdf_documents["filename"]` |
| **Where is my conversation?** | In RAM as `service.conversation_memory.messages` |
| **Is it on my hard drive?** | NO - only in RAM |
| **Can I see it in file explorer?** | NO - no files created on disk |
| **What happens when I refresh?** | All data deleted from RAM, session restarts |
| **What if I close the browser?** | All data deleted, session ended |
| **Can I recover it?** | NO - not saved anywhere |
| **How much RAM is used?** | ~9 MB typical (file size dependent) |
| **Is it encrypted?** | Only SSL if using HTTPS deployment |
| **Can other users see it?** | NO - each user has isolated session |
| **How long does it stay?** | Only during active session |

---

For more details, see: FILE_STORAGE_GUIDE.md
