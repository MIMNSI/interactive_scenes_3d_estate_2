import os
import sys

# --- Configuration ---
# 1. SET YOUR DIRECTORY PATH HERE
#    Use '.' to represent the same directory where you run the script.
#    Or use an absolute path like 'C:/Users/YourName/Desktop/MyWebFiles'
TARGET_DIRECTORY = '.' 
# ---------------------


def modify_html_files_in_directory(directory_path):
    """
    Scans a directory for HTML files and adds a CSS rule to hide the #viewButton.
    """
    print(f"📂 Starting scan in directory: {os.path.abspath(directory_path)}\n")
    
    # The exact text we want to find in the CSS block
    text_to_find = '#viewButton {'
    
    # The text we will replace it with (includes the new rule and keeps indentation)
    # The '      ' spaces are for clean formatting in your HTML file.
    text_to_replace = '#viewButton {\n      display: none;'
    
    modified_count = 0
    processed_count = 0
    
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"❌ Error: Directory not found at '{directory_path}'")
        return

    # Loop through all files in the given directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.html'):
            processed_count += 1
            file_path = os.path.join(directory_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Check if the style exists and hasn't already been modified
                if text_to_find in content:
                    # Replace only the first occurrence to be safe
                    new_content = content.replace(text_to_find, text_to_replace, 1)
                    
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    print(f"✅ Modified: {filename}")
                    modified_count += 1
                elif 'display: none;' in content and '#viewButton' in content:
                    print(f" M Skipped:  {filename} (already contains the rule)")
                else:
                    print(f" M Skipped:  {filename} (style '#viewButton' not found)")

            except Exception as e:
                print(f"❗️ Error processing {filename}: {e}")

    print("\n---")
    print("✨ Script finished!")
    print(f"Total HTML files found: {processed_count}")
    print(f"Files modified: {modified_count}")


# --- Run the script ---
if __name__ == "__main__":
    modify_html_files_in_directory(TARGET_DIRECTORY)