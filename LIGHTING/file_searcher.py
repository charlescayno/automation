import os
import tkinter as tk
from tkinter import filedialog, ttk

def search_files():
    global folder_path
    if not use_previous_folder.get() or not folder_path:
        folder_path = filedialog.askdirectory()
        if folder_path:
            with open("last_folder.txt", "w") as f:
                f.write(folder_path)
    if not folder_path:
        return
    
    keyword = keyword_entry.get().lower()
    
    result_text.delete('1.0', tk.END)
    
    files_found = False
    
    for root, dirs, files in os.walk(folder_path):
        if keyword in root.lower():
            result_text.insert(tk.END, root + '\n')
        for file in files:
            if keyword in file.lower():
                file_path = os.path.join(root, file)
                result_text.insert(tk.END, file_path + '\n')
                files_found = True
    
    if not files_found:
        result_text.insert(tk.END, 'No files found.\n')

def on_search_button_click():
    search_files()

root = tk.Tk()
root.title('File Searcher')
root.configure(bg='black')
root.option_add('*foreground', 'white')
root.option_add('*background', 'black')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
root.geometry(f'{window_width}x{window_height}')

keyword_label = tk.Label(root, text='What are you looking for?', bg='black', fg='white', font=('Arial', 14, 'bold'))
keyword_label.pack(side=tk.TOP, padx=10, pady=10)
keyword_entry = tk.Entry(root, bg='gray')
keyword_entry.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

search_button = tk.Button(root, text='Search', command=on_search_button_click, bg='gray', fg='white')
search_button.pack(side=tk.TOP, padx=10, pady=10)

use_previous_folder = tk.BooleanVar(value=True)
previous_folder_checkbutton = ttk.Checkbutton(root, text='Use Previous Folder', variable=use_previous_folder, onvalue=True, offvalue=False, style='Dark.TCheckbutton')
previous_folder_checkbutton.pack(side=tk.TOP, padx=10, pady=10, anchor='w')

folder_path = None
try:
    with open("last_folder.txt", "r") as f:
        folder_path = f.read()
        if folder_path:
            browse_label = tk.Label(root, text=f"Last used folder: {folder_path}", bg='black')
            browse_label.pack(side=tk.TOP, padx=10, pady=10, anchor='w')
except FileNotFoundError:
    pass



browse_button = tk.Button(root, text='Browse', command=search_files, bg='gray', fg='white')
browse_button.pack(side=tk.TOP, padx=10, pady=10, anchor='w')

result_text = tk.Text(root, height=20, width=80, bg='black', fg='white')
result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

scroll_bar = tk.Scrollbar(result_text)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=result_text.yview)



root.bind('<Return>', search_files)
root.bind('<Escape>', lambda event: root.destroy())

root.mainloop()
