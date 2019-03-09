import Tkinter
from Tkinter import *

import tkMessageBox
import os
import search
import sys

import webbrowser

window = Tkinter.Tk()
window.title('my window')
window.geometry('600x400')

lt = Tkinter.Label(window, text='Search Engine', fg='black', font=("Helvetica", 50, 'bold'))
lt.pack(pady=30);

lq = Tkinter.Label(window,text='keywords')
lq.pack(pady=5);

q = Tkinter.Entry(window) #query
q.pack()

ln = Tkinter.Label(window,text='numbers')
ln.pack(pady=5);

n = Tkinter.Entry(window) #num
n.pack()

# path="C:/Github/CS-221-project3-search-engine/database"
path=sys.argv[1]

    #for r in res: print (r)
def helloCallBack():
    query=q.get()
    query=query.replace(' ','_')
    num=n.get()
    if(num.isdigit()==False):
        tkMessageBox.showinfo( "Warning", "Please type an Integer")
        return
    res = search.search(path, query, num)
    result = ""
    for r in res:
        print r[1] 
        result+=r[1]+"\n"+"\n"
    tkMessageBox.showinfo( "Result", result)

   #
B = Tkinter.Button(window, text ="search", command = helloCallBack)         
B.pack(pady=10)

window.mainloop()                 