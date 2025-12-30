import os
import shutil
import re

def consolidate():
    # Define paths relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir) # i18n/
    raw_dir = os.path.join(root_dir, "raw")
    cons_dir = os.path.join(root_dir, "consolidated")

    print(f"Source: {raw_dir}")
    print(f"Destination: {cons_dir}")

    # 1. Clean and recreate the consolidated directory
    if os.path.exists(cons_dir):
        print("Cleaning existing consolidated directory...")
        shutil.rmtree(cons_dir)
    os.makedirs(cons_dir)

    # 2. Identify export directories and sort them by date (oldest first)
    # Assumes folder naming convention: YYYY-MM-DD_project_...
    if not os.path.exists(raw_dir):
        print("Error: 'raw' directory not found.")
        return

    exports = sorted([d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))])
    
    if not exports:
        print("No export directories found.")
        return

    print(f"Found {len(exports)} incremental exports. Merging in order...")

    total_files_processed = 0

    # 3. Process each export
    for export_name in exports:
        export_path = os.path.join(raw_dir, export_name)
        print(f"Processing: {export_name}")
        
        # Walk through the export directory
        for root, dirs, files in os.walk(export_path):
            for file in files:
                src_path = os.path.join(root, file)
                
                # Calculate relative path from the export root
                # Structure is typically: raw/EXPORT_NAME/LOCALE/PREFIX/path/to/content
                rel_path = os.path.relpath(src_path, export_path)
                parts = rel_path.split(os.sep)

                # We expect at least: LOCALE + PREFIX + CONTENT_FILE
                if len(parts) < 3:
                    # Skip top-level files or unexpected structures
                    continue

                locale = parts[0]
                # parts[1] is the "prefix" (e.g., 'outline', '0outline') which we want to discard
                content_path_parts = parts[2:] 
                
                # Reconstruct the target path
                # Target: i18n/consolidated/LOCALE/path/to/content
                
                # Handle filename transformations
                filename = content_path_parts[-1]
                
                if filename.endswith(".md.html"):
                    # Keep .md.html extension as requested.
                    pass
                elif filename.endswith(".html"):
                     # Generic HTML files.
                     pass
                elif filename.endswith(".arb"):
                    # Skip .arb files as they are complex resource bundles 
                    # and mostly relate to layout/skeleton config (e.g. _book.yaml).
                    continue
                else:
                    # Skip other file types if any (e.g., system files)
                    continue

                # Construct destination path
                dest_path = os.path.join(cons_dir, locale, *content_path_parts)
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Copy/Overwrite the file
                shutil.copy2(src_path, dest_path)
                total_files_processed += 1

    print("-" * 30)
    print(f"Consolidation complete.")
    print(f"Total files processed: {total_files_processed}")
    print(f"Output directory: {cons_dir}")

if __name__ == "__main__":
    consolidate()
