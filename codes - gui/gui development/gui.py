from tkinter import *
 
root = Tk()


root.geometry("800x400")


frame = Frame(root)
frame.pack()
 
leftframe = Frame(root)
leftframe.pack(side=LEFT)
 
rightframe = Frame(root)
rightframe.pack(side=RIGHT)
 
label = Label(frame, text = "Test Automation")
label.pack()


def button1():
    print("hello")

button1 = Button(leftframe, text = "Button1", command=button1)
button1.pack(padx = 3, pady = 4)
button2 = Button(rightframe, text = "Button2")
button2.pack(padx = 3, pady = 3)
button3 = Button(leftframe, text = "Button3")
button3.pack(padx = 3, pady = 3)
 
root.title("Test Automation")
root.mainloop()