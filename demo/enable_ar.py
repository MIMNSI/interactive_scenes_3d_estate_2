import os
import re

# --- 1. Configuration ---
# Place this script in the same folder as your HTML files,
# or change the FOLDER_PATH to the correct location.
FOLDER_PATH = '.'

# --- 2. Define the Regex Pattern and Replacement ---

# This pattern finds the specific if/else block and uses capture groups
# to isolate the line we want to comment out.
# It's designed to handle variations in the scene name.
find_pattern = re.compile(
    # Part 1: Capture everything from "if (isAndroid)" up to the line we want to change.
    # The `.*?` is a non-greedy match for any characters, including newlines.
    r"(if \(isAndroid\) \{.*?//window\.location\.href = intent;\s*\n)"
    
    # Part 2: Capture the indentation (whitespace) of the target line.
    r"(\s*)"
    
    # Part 3: Capture the content of the target line, allowing any scene name.
    r"(window\.location\.href = 'xr\.html\?scene=.*?&xr=ar';)"
    
    # Part 4: Capture the rest of the code block until its final closing brace.
    r"(.*?\s*\})",
    
    # Use re.DOTALL to make '.' match newline characters.
    flags=re.DOTALL
)

# The replacement string uses backreferences (\1, \2, etc.) to rebuild the block.
# We insert "//" before the original line's content (\3) to comment it out.
replacement_pattern = r"\1\2//\3\4"


# --- 3. Main script logic ---

def run_batch_comment(folder_path):
    """
    Scans a folder for .html files and comments out a specific line using regex.
    """
    print(f"🔍 Starting scan in folder: '{os.path.abspath(folder_path)}'")
    
    try:
        all_files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"❌ ERROR: The folder '{folder_path}' was not found.")
        print("Please check the FOLDER_PATH variable at the top of the script.")
        return

    html_files = [f for f in all_files if f.lower().endswith('.html')]
    
    if not html_files:
        print("No HTML files found in the specified folder.")
        return

    files_modified = 0
    print(f"Found {len(html_files)} HTML file(s) to check.")

    for filename in html_files:
        file_path = os.path.join(folder_path, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                original_content = file.read()

            # Use re.subn() to perform the find-and-replace operation.
            # It returns the new content and the number of substitutions made.
            new_content, num_substitutions = find_pattern.subn(replacement_pattern, original_content)
            
            # If a substitution was made, write the new content back to the file.
            if num_substitutions > 0:
                print(f"  -> Found match in '{filename}'. Commenting line and updating file...")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                files_modified += 1

        except Exception as e:
            print(f"  -> ❌ An error occurred while processing {filename}: {e}")

    print("\n--- ✨ All Done! ---")
    print(f"Files scanned: {len(html_files)}")
    print(f"Files modified: {files_modified}")


# --- 4. Run the script ---
if __name__ == "__main__":
    print("--- Script to Comment Out a Specific Line in HTML Files ---")
    input("❗️ **IMPORTANT**: Have you backed up your files? This script will modify them in place. Press Enter to continue...")
    run_batch_comment(FOLDER_PATH)