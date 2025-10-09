import os
import re

def modify_html_files(list_filename="list.txt"):
    """
    Reads a list of HTML filenames, finds a specific <script type="module"> block,
    replaces its content with a new template, and saves the changes in place.

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

            # The scene name is the filename without the '.html' extension
            scene_name = html_filename.replace('.html', '')

            # Define the new inner content for the script block
            # The {scene_name} will be dynamically inserted
            replacement_script_content = f"""
   const modelViewer = document.querySelector("#ar-model-viewer");
      const arButton = document.querySelector("#viewButton");
      const isAndroid = /android/i.test(navigator.userAgent);
      modelViewer.addEventListener('load', () => {{
        if (modelViewer.canActivateAR) {{ arButton.style.display = 'block'; }}
      }});
      arButton.addEventListener('click', () => {{
        if (isAndroid) {{
          //const absoluteSrc = new URL(modelViewer.src, window.location.href).href;
          //const intent = `intent://arvr.google.com/scene-viewer/1.0?file=${{absoluteSrc}}&mode=ar_only#Intent;scheme=https;package=com.google.ar.core;action=android.intent.action.VIEW;S.browser_fallback_url=${{encodeURIComponent(window.location.href)}};end;`;
          //window.location.href = intent;
          //window.location.href = 'xr.html?scene={scene_name}&xr=ar';
        }} else {{
          modelViewer.activateAR();
          //alert('AR is coming soon to iPhones. Please use an Android device for now.');

        }}
      }});
  """

            # This regex finds the specific <script type="module"> tag that contains the model-viewer logic
            # and replaces everything between the opening and closing tags.
            target_block_regex = re.compile(
                r'(<script type="module">\s*const modelViewer = document\.querySelector\("#ar-model-viewer"\);)[\s\S]*?(<\/script>)',
                re.DOTALL
            )
            
            # Construct the full replacement, keeping the original script tags
            full_replacement = f'\\1{replacement_script_content}\\2'

            # Perform the substitution
            new_content, count = target_block_regex.subn(full_replacement, content)

            if count > 0:
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Successfully modified '{html_filename}'.")
                modified_count += 1
            else:
                print(f"Warning: Could not find the target <script> block in '{html_filename}'. File was not changed.")

        except Exception as e:
            print(f"Error processing file '{html_filename}': {e}")

    print(f"\nProcessing complete. Modified {modified_count} out of {len(html_files)} files found.")

if __name__ == "__main__":
    modify_html_files()