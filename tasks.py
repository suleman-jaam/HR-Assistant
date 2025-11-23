from crewai import Task
from agents import file_reader_agent, file_extractor_agent, qa_agent

# Task 1: Save user-provided file paths to a JSON manifest (files.json)
save_paths_task = Task(
    description=(
        "Collect file paths from the input and save them into `files.json`.\n"
        "Input paths: {paths_text}\n"
        "Perform basic validation (exists, readable) and return the manifest path and a count of saved entries."
    ),
    expected_output="Path to the created `files.json` manifest and the number of saved file paths.",
    agent=file_reader_agent,
)

# Task 2: Read the manifest, validate and extract chunks from each listed file
extract_chunks_task = Task(
    description=(
        "Load `files.json`, validate each file path, read file content (PDF/DOCX/TXT or plain text), and split into ~500-character chunks.\n"
        "Store the extracted chunks into ChromaDB using the `extract_and_chunk_files` tool."
    ),
    expected_output="A summary of files processed and the total number of chunks stored in ChromaDB.",
    agent=file_extractor_agent,
)

# Task 3: Answer user questions based on document chunks from ChromaDB
qa_task = Task(
    description=(
        "Answer the user's question based only on document chunks retrieved from ChromaDB.\n"
        "Question: {question}\n\n"
        "Behavioral rules:\n"
        "- You can greet users like hi, how are you? etc...\n"
        "- Use `answer_question_simple` which will automatically query ChromaDB for relevant chunks.\n"
        "- Do NOT invent facts; if the answer is not present in the documents, state that clearly.\n"
        "- Provide concise, professional HR-style answers."
    ),
    expected_output="A concise, document-grounded answers with temperature 0.3",
    agent=qa_agent,
)
