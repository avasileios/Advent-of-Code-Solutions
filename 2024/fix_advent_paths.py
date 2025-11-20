import os
import re

# Define the base directory where the Advent challenges are located
base_dir = r"C:\Users\vantonopoulos\OneDrive - Space Hellas SA\Documents\Advent\2024"

# Counter for files modified
files_modified = 0
files_checked = 0

# Walk through all subdirectories
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith('.py'):
            filepath = os.path.join(root, filename)
            files_checked += 1
            
            try:
                # Read the file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Pattern to match open() statements with various path formats
                # This will match patterns like:
                # open("Day-1-Challange/input.txt", ...)
                # open("input.txt", ...)
                # open('input.txt', ...)
                
                # Check if the file has an open() statement that needs fixing
                if 'open(' in content and 'input.txt' in content:
                    
                    # First, check if it already has the fix
                    if 'os.path.dirname(os.path.abspath(__file__))' not in content:
                        
                        # Add the import statement if not present
                        if 'import os' not in content:
                            content = 'import os\n' + content
                        
                        # Pattern to find open() statements with input.txt
                        # Matches: open("any/path/input.txt", "r") or open('input.txt', 'r')
                        pattern = r'open\(["\']([^"\']*input\.txt)["\'],\s*["\']r["\']\)'
                        
                        def replace_open(match):
                            # Create the new code with proper path handling
                            return ('open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '
                                   '"input.txt"), "r")')
                        
                        # Replace all occurrences
                        new_content = re.sub(pattern, replace_open, content)
                        
                        # Only write if something changed
                        if new_content != original_content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            files_modified += 1
                            print(f"✓ Fixed: {filename} in {os.path.basename(root)}")
                        
            except Exception as e:
                print(f"✗ Error processing {filepath}: {str(e)}")

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Files checked: {files_checked}")
print(f"  Files modified: {files_modified}")
print(f"{'='*60}")
print("\nAll done! Your scripts should now work from any directory.")
