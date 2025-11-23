import os
import logging
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools.file_reader_tools import save_file_paths
from tools.file_extractor_tools import extract_and_chunk_files
from tools.qa_tools import answer_question_simple

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize LLM from environment (no fallback to hard-coded key for security)
api_key = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=api_key or "dummy-key",  # Dummy key to prevent crash, but will fail at runtime
    temperature=0.2,
) if api_key else None



class LLMWrapper:
    """Wrapper around LLM for generation."""
    
    def __init__(self, llm_obj):
        self.llm = llm_obj
    
    def generate(self, prompt: str) -> str:
        """Generate response from LLM.
        
        Args:
            prompt: The input prompt
            
        Returns:
            Generated text
            
        Raises:
            ValueError: If LLM is not available or API call fails
        """
        if not self.llm:
            raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file.")
        
        try:
            # Try different methods
            if hasattr(self.llm, "call"):
                return str(self.llm.call(prompt))
            elif hasattr(self.llm, "generate"):
                return str(self.llm.generate(prompt))
            elif hasattr(self.llm, "invoke"):
                return str(self.llm.invoke(prompt))
        except Exception as e:
            logger.error("LLM API error: %s", e)
            raise ValueError(f"Failed to generate response. API Error: {str(e)}")
        
        raise ValueError("Could not generate response. LLM method not found.")



llm_wrapper = LLMWrapper(llm)

# File Reader Agent with tools for reading & store file paths
file_reader_agent = Agent(
    role="Get files & store paths",
    goal="Retrieve file paths from the user and save them to a JSON manifest",
    backstory=(
        "Collect file paths from user input (or UI) and save them to a JSON file named files.json. "
        "Validates basic path existence and writes a manifest for later extraction."
    ),
    tools=[save_file_paths],
    verbose=False,
    llm=llm,
)

# file reader & extractor agent
file_extractor_agent = Agent(
    role="File Reader & Extractor",
    goal=(
        "Load the JSON manifest (files.json), validate each path, read and chunk files, "
        "and write the extracted chunks into an output JSON (extracted_chunks.json)."
    ),
    backstory=(
        "Reads the file manifest created by the file_reader_agent, validates each entry, "
        "extracts content and creates chunked payloads suitable for semantic search and QA."
    ),
    tools=[extract_and_chunk_files],
    verbose=False,
    llm=llm,
)
# Question Answering Agent
qa_agent = Agent(
    role="Question Answering Agent",
    goal="Answer questions based on provided document chunks",
    backstory="An expert in understanding and answering questions based on HR text data. Uses provided chunks to give accurate, concise answers.",
    tools=[answer_question_simple],
    verbose=False,
    llm=llm,
    memory=True
)

