import os
import shutil
import hashlib
from tkinter import Tk, filedialog

# Define the file extensions and corresponding target folders
extensions = {
    '.py': 'python-code',
    '.html': 'html-code',
    '.js': 'js-code',
    '.txt': 'txt-file',
    '.jpg': 'images',
    '.png': 'images',
    '.pdf': 'documents',
    '.docx': 'documents',
    '.xlsx': 'documents',
    '.mp3': 'audio',
    '.mp4': 'videos',
    '.zip': 'archives',
    '.rar': 'archives',
    '.csv': 'data',
    '.json': 'data',
    '.css': 'web-files',
    '.php': 'web-files',
    '.cpp': 'cpp-code',
    '.java': 'java-code',
}

def flag():
    """Display the welcome message."""
    print(f"""         
         *************************************
         *      Hello ,Welcome to Arranger    *
         *         Made by Nour Sallam       *
         *************************************
         
         [1] Auto-arrange files
         [2] Add specific key arrangement
         [3] Delete duplicated files
         [4] Exit
    """)

def choose_directory():
    """Open a dialog to choose a directory and return the selected path."""
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Source Directory")
    return directory

def autoArrange(source_dir):
    """Automatically arrange files into their respective folders based on extensions."""
    for file in os.listdir(source_dir):
        # Loop through the file extensions
        for ext, folder in extensions.items():
            if file.endswith(ext):
                # Create the folder if it doesn't exist
                target_folder = os.path.join(source_dir, folder)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                # Move the file to the corresponding folder
                shutil.move(os.path.join(source_dir, file), os.path.join(target_folder, file))
                print(f"Moved {file} to {folder}")
                break  # Exit the loop once the file is moved

def addSpecific(source_dir):
    """
    Arrange files containing a specific word into a folder named after that word.
    """
    if not source_dir:
        print("No directory selected. Returning to main menu.")
        return

    word = input("Enter the word you want to arrange for: ").strip()
    if not word:
        print("No word entered. Returning to main menu.")
        return

    # Create the target folder if it doesn't exist
    target_folder = os.path.join(source_dir, word)
    os.makedirs(target_folder, exist_ok=True)

    # Loop through files in the source directory
    moved_count = 0
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)
        
        # Skip if it's not a file (e.g., it's a directory)
        if not os.path.isfile(file_path):
            continue
        
        # Check if the file contains the specified word
        if word in file:
            # Move the file to the target folder
            try:
                shutil.move(file_path, os.path.join(target_folder, file))
                print(f"Moved {file} to {word} folder.")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {file}: {e}")

    if moved_count == 0:
        print(f"No files containing '{word}' were found.")
    else:
        print(f"Moved {moved_count} files to '{word}' folder.")

def calculate_file_hash(file_path):
    """Calculate the hash of a file's content."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def deleteDuplicates(source_dir):
    """Delete duplicate files in the specified directory."""
    hash_to_files = {}

    # Loop through all files in the directory
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)
        if os.path.isfile(file_path):  # Ensure it's a file (not a folder)
            file_hash = calculate_file_hash(file_path)
            if file_hash in hash_to_files:
                # If the hash already exists, it's a duplicate
                hash_to_files[file_hash].append(file_path)
            else:
                # Otherwise, add it to the dictionary
                hash_to_files[file_hash] = [file_path]

    # Delete duplicate files
    deleted_count = 0
    for file_hash, files in hash_to_files.items():
        if len(files) > 1:  # If there are duplicates
            print(f"Found {len(files)} duplicates for hash {file_hash}:")
            for file_path in files[1:]:  # Keep the first file, delete the rest
                os.remove(file_path)
                print(f"Deleted {file_path}")
                deleted_count += 1

    if deleted_count == 0:
        print("No duplicate files found.")
    else:
        print(f"Deleted {deleted_count} duplicate files.")

def main():
    """Main function to handle program flow."""
    while True:
        flag()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Auto-arrange files
            source_dir = choose_directory()
            if not source_dir:
                print("No directory selected. Returning to main menu.")
                continue
            autoArrange(source_dir)
        elif choice == '2':
            # Add specific key arrangement
            source_dir = choose_directory()
            if not source_dir:
                print("No directory selected. Returning to main menu.")
                continue
            addSpecific(source_dir)
        elif choice == '3':
            # Delete duplicated files
            source_dir = choose_directory()
            if not source_dir:
                print("No directory selected. Returning to main menu.")
                continue
            deleteDuplicates(source_dir)
        elif choice == '4':
            # Exit the program
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()