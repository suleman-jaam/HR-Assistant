# HR Document Q&A System

An advanced interactive Q&A system for HR documents using CrewAI, ChromaDB, and Google Gemini AI.

## Features

- 🤖 **Multi-Agent System** - Powered by CrewAI with specialized agents
- 🔍 **Semantic Search** - ChromaDB with Google Gemini embeddings
- 📚 **Multi-Document Support** - Process 2-30 documents simultaneously
- 💬 **Intelligent Q&A** - Context-aware answers using Gemini 2.0 Flash

- 📄 **Multiple Formats** - Supports PDF, DOCX, and TXT files

## Architecture

### Agents
1. **File Reader Agent** - Collects and validates file paths
2. **File Extractor Agent** - Processes documents and stores chunks in ChromaDB
3. **QA Agent** - Answers questions using retrieved document chunks

### Technology Stack
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: Google Generative AI Embeddings (with local fallback)
- **Vector Database**: ChromaDB
- **Framework**: CrewAI
- **Document Processing**: PyPDF2, python-docx
- **Semantic Search**: sentence-transformers

## Installation

### Prerequisites
- Python 3.10+
- Google Gemini API key

### Setup

1. **Clone the repository**
```bash
cd HR_Model
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your-gemini-api-key-here
LLM_MODEL=gemini-2.0-flash
LLM_TEMPERATURE=0.2
```



## Usage

### Option 1: Agent-Based Workflow (Recommended)

Use `crew_main.py` for full agent-based automation:

```bash
python crew_main.py
```

**Features:**
- Agents handle all tasks (file management, processing, Q&A)
- Automatic `files.json` updates via file_reader_agent
- ChromaDB storage via file_extractor_agent
- Q&A via qa_agent

**Menu Options:**
1. **Process documents** - Agents save paths to files.json and process documents
2. **Ask question** - QA agent answers using ChromaDB
3. **Exit**

### Option 2: Direct Processing

Use `main.py` for direct document processing without agents:

```bash
python main.py
```

**Features:**
- Direct file processing (no agent workflow)
- Manual file path input
- Voice I/O support (optional)

**Menu Options:**
1. **Load documents** - Directly process files
2. **Ask question (type)** - Type your question
3. **Ask question (voice)** - Use voice input
4. **List loaded documents**
5. **Exit**

### Example Workflow

```
1. Select option 1 to load documents
2. Enter the number of documents (e.g., 3)
3. Provide file paths for each document
4. Select option 2 to ask questions
5. Type your HR-related question
6. View the answer and optional source information
```

## Project Structure

```
HR_Model/
├── .env                    # Environment variables (API keys)
├── agents.py              # CrewAI agent definitions
├── tasks.py               # CrewAI task definitions
├── main.py                # Main interactive application
├── requirements.txt       # Python dependencies
├── files.json             # File paths manifest

├── chroma_db/             # ChromaDB persistent storage
├── models/                # Local embedding models
├── test_data/             # Sample test files
└── tools/
    ├── chroma_tools.py           # ChromaDB manager
    ├── file_extractor_tools.py   # Document processing
    ├── file_reader_tools.py      # File path management
    └── qa_tools.py               # Question answering logic
```

## Configuration

### Chunk Size
Default chunk size is 500 characters. To modify:
- Edit `FileProcessor(chunk_size=500)` in `tools/file_extractor_tools.py`

### LLM Temperature
Default temperature is 0.2. To modify:
- Edit `temperature=0.2` in `agents.py`
- Or set `LLM_TEMPERATURE` in `.env`

### Embedding Function
The system uses Google Gemini embeddings. `GEMINI_API_KEY` is required for the system to function.

## API Costs

- **Gemini 2.0 Flash**: Free tier available
- **Gemini Embeddings**: Free tier with daily limits
- Check [Google AI Studio](https://ai.google.dev/) for current pricing

## Troubleshooting

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify the API key is correctly set in `.env`

### "Quota exceeded for embeddings"
- You've hit the free tier limit for Gemini embeddings
- System will automatically fall back to local embeddings
- Or wait for quota reset (usually daily)

### "ChromaDB embedding function conflict"
- Delete the `chroma_db` folder to reset the database
- This happens when switching between embedding functions

### Voice I/O not working
- Ensure optional dependencies are installed: `sounddevice`, `vosk`, `pyttsx3`
- Download Vosk model to `models/vosk-model-small-en-us-0.15`

## Development

### Adding New Document Types
Extend `FileProcessor.read_file()` in `tools/file_extractor_tools.py`

### Customizing Prompts
Modify the prompt template in `MultiDocumentQASystem.answer_question()` in `main.py`

### Adding New Agents
1. Define agent in `agents.py`
2. Create corresponding task in `tasks.py`
3. Add tools in `tools/` directory

## License

This project is for educational and internal use.

## Support

For issues or questions, please check:
- [CrewAI Documentation](https://docs.crewai.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)

## Acknowledgments

- Built with [CrewAI](https://www.crewai.com/)
- Powered by [Google Gemini](https://ai.google.dev/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)
