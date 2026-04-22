import os

def search_files():
    global folder_path
    if not folder_path or not os.path.exists(folder_path):
        folder_path = input("Enter folder path: ")
        with open("last_folder.txt", "w") as f:
            f.write(folder_path)
    else:
        print(f"Searching in folder: {folder_path}")
    
    keyword = input("Enter keyword: ").lower()
    print()
    
    files_found = False
    
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            if keyword in dir.lower():
                dir_path = os.path.join(root, dir)
                print("|   " * (root.count(os.sep) - folder_path.count(os.sep)) + "|-- " + dir + os.sep)
        for file in files:
            if keyword in file.lower():
                file_path = os.path.join(root, file)
                print("|   " * (root.count(os.sep) - folder_path.count(os.sep)) + "|-- " + file + " - " + file_path)
                files_found = True
    
    if not files_found:
        print('No files found.')
    
    print()
    search_again = input("Search again? Enter keyword or press n to exit: ").lower()
    if search_again != 'n':
        search_files()

if __name__ == '__main__':
    change_folder = input("Do you want to change the default folder? (y/n) ").lower()
    if change_folder == 'y':
        folder_path = None
    else:
        folder_path = None
        try:
            with open("last_folder.txt", "r") as f:
                folder_path = f.read()
        except FileNotFoundError:
            pass
    
    search_files()
