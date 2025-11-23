import os
import requests
import json
from pathlib import Path

# --- CONFIGURATION ---
API_URL = "http://localhost:8080/api/v1/analysis/submit"
# Scan the parent directory (project root)
TARGET_DIRECTORY = "../" 
# File extensions to analyze
EXTENSIONS_TO_SCAN = {'.java', '.js', '.py', '.ts', '.tf'}
# Directories to ignore (performance & noise reduction)
IGNORE_DIRS = {'node_modules', '.git', 'target', 'dist', 'venv', '__pycache__', '.angular', '.vscode', '.idea'}

def scan_directory(path):
    """
    Walks through the directory tree and triggers analysis for supported files.
    """
    abs_path = os.path.abspath(path)
    print(f"🛡️  Starting Security Scan at: {abs_path}\n")
    
    files_found = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(path):
        # Modify 'dirs' in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            file_extension = Path(file).suffix
            
            if file_extension in EXTENSIONS_TO_SCAN:
                file_path = os.path.join(root, file)
                # Calls the analysis function for each file
                analyze_file(file_path)
                files_found += 1

    print(f"\n✅ Scan Complete!")
    print(f"📂 Total files analyzed: {files_found}")

def analyze_file(file_path):
    """
    Reads a file and sends it to the GDPR Agent API.
    """
    print(f"🔍 Scanning: {file_path} ...", end=" ", flush=True)
    
    try:
        # Attempt to read file with utf-8 encoding
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()

        # Skip empty files
        if not code_content.strip():
            print("⏩ (Skipped - Empty)")
            return

        # Payload for the Java Backend
        payload = {
            "javaCode": code_content,
            "language": "en" # Default report language: English
        }
        
        # Send POST request
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ SAFE / REVIEWED")
                    save_report(file_path, result.get('message'))
                else:
                    print(f"❌ FAILURE: {result.get('message')}")
            else:
                print(f"❌ HTTP ERROR {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR (Is Backend running on port 8080?)")

    except Exception as e:
        print(f"⚠️ Read Error: {e}")

def save_report(file_path, report_content):
    """
    Saves the AI analysis report to a markdown file.
    """
    output_dir = "audit_reports" # Folder name in English
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a safe filename replacing slashes/dots
    safe_filename = os.path.basename(file_path).replace('.', '_') + "_report.md"
    save_path = os.path.join(output_dir, safe_filename)
    
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ Security Audit Report: {file_path}\n\n")
            f.write(report_content)
    except Exception as e:
        print(f"Error saving report: {e}")

# Entry point (Must be at the bottom)
if __name__ == "__main__":
    scan_directory(TARGET_DIRECTORY)