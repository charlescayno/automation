import tkinter as tk
root = tk.Tk()
root.geometry('400x200')

def button_command():
    text = entry1.get()
    print(text)
    return None

entry1 = tk.Entry(root, width = 20)
entry1.pack()

tk.Button(root, text = "Button", command=button_command).pack()

root.mainloop()
