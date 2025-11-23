"""
Reset ChromaDB to use new embedding function.
Run this script once after switching from Gemini embeddings to local embeddings.
"""
import shutil
import os
import sys

chroma_dir = "chroma_db"

if os.path.exists(chroma_dir):
    print(f"[+] Deleting old ChromaDB directory: {chroma_dir}")
    try:
        shutil.rmtree(chroma_dir)
        print("[+] ChromaDB reset complete!")
        print("[+] You can now process documents with local embeddings (no API quota limits)")
    except PermissionError as e:
        print(f"\n[-] ERROR: {e}")
        print("\n[!] The ChromaDB database is currently in use.")
        print("[!] Please close any running Python processes (crew_main.py, etc.)")
        print("[!] Then run this script again, OR manually delete the 'chroma_db' folder")
        sys.exit(1)
else:
    print(f"[-] ChromaDB directory not found: {chroma_dir}")
    print("[+] No reset needed - ready to use local embeddings")

