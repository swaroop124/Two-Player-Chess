import tkinter as tk
from tkinter.constants import X

def time_selector():
    root=tk.Tk()
    root.title("Time Selector")
    root.geometry("800x400")

    tk.Label(root,text="In which time format do you want to play the game?",font="Calibri 24 bold italic").pack()
    v = tk.StringVar(root, "1")
 
   
    values = {"3|0" : "3|0",
          "5|0" : "5|0",
          "5|5" : "5|5",
          "10|0" : "10|0",
          "10|10" : "10|10",
          "30|0":"30|0"}
 

    for (text, value) in values.items():
        tk.Radiobutton(root, text = text, variable = v,
                value = value, indicator = 0,
                background = "light blue",font="arial 11 bold").pack(fill = X, ipady = 5)

    tk.Button(root,text="Submit",command=root.destroy,font="Calibri 12 bold italic").pack(pady=10)
    tk.Label(root,text="Please note that the time displayed in the Game is in seconds",font="Calibri 10 bold italic").pack(pady=5)
    root.mainloop()  

    return v.get()
