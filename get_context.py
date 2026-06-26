import os

# Define the project root and files to ignore
PROJECT_ROOT = os.getcwd()
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', '.angular', 'target'}
IGNORE_FILES = {'package-lock.json', '.DS_Store', 'pom.xml', 'build.gradle'}
OUTPUT_FILE = 'project_context_for_ai.txt'

def generate_context():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write("=== CODEGUARD AI - FULL PROJECT ARCHITECTURE ===\n\n")
        
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Filter directories in-place to prevent walking into ignored paths
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES:
                    continue
                    
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, PROJECT_ROOT)
                
                # Only read standard text/code files
                if file.endswith(('.ts', '.html', '.css', '.py', '.java', '.json', '.md', '.txt')):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"--- START OF FILE: {relative_path} ---\n")
                            outfile.write(infile.read())
                            outfile.write(f"\n--- END OF FILE: {relative_path} ---\n\n")
                    except Exception as e:
                        outfile.write(f"[ERROR READING FILE {relative_path}: {str(e)}]\n\n")

    print(f"Success! All code context saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_context()