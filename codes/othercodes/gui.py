# python program demonstrating 
# Combobox widget using tkinter 


import tkinter as tk 
from tkinter import ttk 

# Creating tkinter window 
window = tk.Tk() 
window.title('Automation') 
window.geometry('500x250') 

# label text for title 
ttk.Label(window, text = "Automation Tests", 
		background = 'green', foreground ="white", 
		font = ("Calibri", 15)).grid(row = 0, column = 1) 

# label 
ttk.Label(window, text = "Select Test:", 
		font = ("Calibri", 10)).grid(column = 0, 
		row = 5, padx = 10, pady = 25) 

# Combobox creation 
n = tk.StringVar() 
testselection = ttk.Combobox(window, width = 27, textvariable = n) 

# Adding combobox drop down list 
testselection['values'] = (' Output Startup Waveforms', 
						' Output Bench Ripple Waveforms') 

testselection.grid(column = 1, row = 5) 
testselection.current()



window.mainloop()