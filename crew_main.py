"""
CrewAI-based HR Document Q&A System
Uses agents to handle file management, document processing, and Q&A
"""

import os
from dotenv import load_dotenv
from crewai import Crew
from agents import file_reader_agent, file_extractor_agent, qa_agent
from tasks import save_paths_task, extract_chunks_task, qa_task

load_dotenv()


def main():
    """Main function to run the CrewAI workflow."""
    
    print("\n" + "="*70)
    print("CREWAI HR DOCUMENT Q&A SYSTEM")
    print("="*70)
    print("Agents will handle: File management -> Document processing -> Q&A")
    
    # Check API key - required
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GEMINI_API_KEY is required!")
        print("  Please set GEMINI_API_KEY in your .env file")
        print("  The system cannot run without a valid API key.")
        print("\nExiting...")
        return
    
    print("\n[+] GEMINI_API_KEY configured")
    print("\n" + "="*70)
    
    while True:
        print("\n" + "-"*70)
        print("MAIN MENU")
        print("-"*70)
        print("1. Process documents (agents workflow)")
        print("2. Ask question (QA agent)")
        print("3. Exit")
        print("-"*70)
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\n" + "="*70)
            print("STEP 1: Provide file paths")
            print("="*70)
            
            print("\nHow many documents? (2-30): ", end="")
            try:
                num_files = int(input().strip())
                if not 2 <= num_files <= 30:
                    print("[-] Please enter a number between 2 and 30")
                    continue
            except ValueError:
                print("[-] Invalid number")
                continue
            
            file_paths = []
            for i in range(num_files):
                file_path = input(f"Enter path for document {i+1}: ").strip()
                if file_path:
                    file_paths.append(file_path)
            
            if not file_paths:
                print("[-] No file paths provided")
                continue
            
            # Prepare input for agents
            paths_text = "\n".join(file_paths)
            
            # Create crew with file processing workflow (both agents run automatically)
            crew = Crew(
                agents=[file_reader_agent, file_extractor_agent],
                tasks=[save_paths_task, extract_chunks_task],
                verbose=False  # Disable verbose output
            )
            
            print("\n[Agent 1] Saving file paths to files.json...")
            print("[Agent 2] Processing documents and storing in ChromaDB...")
            
            try:
                result = crew.kickoff(inputs={"paths_text": paths_text})
                print("\n" + "="*70)
                print("✅ Document processing complete!")
                print("="*70)
                print(f"Result: {result}")
            except Exception as e:
                print(f"\n❌ Error during processing: {e}")
        
        elif choice == "2":
            print("\n" + "="*70)
            print("ASK A QUESTION")
            print("="*70)
            
            question = input("\nYour question: ").strip()
            if not question:
                continue
            
            # Create crew with QA agent
            crew = Crew(
                agents=[qa_agent],
                tasks=[qa_task],
                verbose=False  # Disable verbose output
            )
            
            print("\n[QA Agent] Searching ChromaDB and generating answer...")
            
            try:
                result = crew.kickoff(inputs={"question": question})
                print("\n" + "="*70)
                print("ANSWER:")
                print("="*70)
                print(result)
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif choice == "3":
            print("\n[+] Cleaning up and exiting...")
            
            # Clean up ChromaDB
            try:
                from tools.chroma_tools import chroma_manager
                chroma_manager.reset()
                print("[+] ChromaDB cleared")
            except Exception as e:
                print(f"[-] Could not clear ChromaDB: {e}")
            
            # Delete files.json
            try:
                if os.path.exists("files.json"):
                    os.remove("files.json")
                    print("[+] files.json deleted")
            except Exception as e:
                print(f"[-] Could not delete files.json: {e}")
            
            print("[+] Goodbye!")
            break
        
        else:
            print("[-] Invalid choice")


if __name__ == "__main__":
    main()
