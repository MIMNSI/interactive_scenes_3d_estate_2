import os
import re

def fix_html_files(list_filename="list.txt"):
    """
    Reads a list of HTML filenames, finds and removes a specific
    duplicate line of JavaScript, and saves the changes in place.

    Args:
        list_filename (str): The name of the text file containing the list of HTML files.
    """
    if not os.path.exists(list_filename):
        print(f"Error: The file '{list_filename}' was not found in the current directory.")
        return

    with open(list_filename, 'r') as f:
        html_files = [line.strip() for line in f if line.strip().endswith('.html')]

    print(f"Found {len(html_files)} files to process.")
    
    modified_count = 0
    for html_filename in html_files:
        if not os.path.exists(html_filename):
            print(f"Warning: Skipping '{html_filename}' as it was not found.")
            continue

        try:
            with open(html_filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Define the exact duplicate line to find
            duplicate_line = '   const modelViewer = document.querySelector("#ar-model-viewer");'
            
            # Create the block of two identical lines to search for
            block_to_find = f"{duplicate_line}\n{duplicate_line}"

            # Replace the block of two lines with just a single instance
            # This ensures we only act when there's an actual duplicate
            new_content, count = content.replace(block_to_find, duplicate_line, 1), 0
            if new_content != content:
                count = 1

            if count > 0:
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Successfully fixed duplicate line in '{html_filename}'.")
                modified_count += 1
            else:
                print(f"No duplicate line found in '{html_filename}'. File was not changed.")

        except Exception as e:
            print(f"Error processing file '{html_filename}': {e}")

    print(f"\nProcessing complete. Fixed {modified_count} out of {len(html_files)} files found.")

if __name__ == "__main__":
    fix_html_files()