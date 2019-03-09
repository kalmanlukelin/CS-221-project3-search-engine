import Tkinter
from Tkinter import *

import tkMessageBox
import os
import search
import sys

import webbrowser

window = Tkinter.Tk()

window.title('my window')
window.geometry('1200x600')

lq = Tkinter.Label(window, text='Search Engine', fg='black', font=("Helvetica", 50, 'bold'))
lq.pack(pady=30);

q = Tkinter.Entry(window) #query
q.pack(ipadx = 150, ipady = 2)

# add numbers
'''
ln = Tkinter.Label(window,text='num')
ln.pack();
n = Tkinter.Entry(window) #num
n.pack()
'''

path="C:/Github/CS-221-project3-search-engine/database"
path=sys.argv[1]

def web_callback(url):
    webbrowser.open_new(url)

def helloCallBack():
    global links
    for l in links: l.destroy()
    links=[]

    query=q.get()
    query=query.replace(' ','_')

    '''
    num=n.get()
    if(num.isdigit()==False):
        tkMessageBox.showinfo( "Warning", "Please type an Integer")
        return
    '''
    
    res = search.search(path, query, 10)
    
    for r in res:
        print r

        link=Label(window, text=r[0], fg='black', font=("Helvetica", 12))
        link.pack()
        links.append(link)

        link=Label(window, text=r[1], fg="blue", cursor="hand2")
        link.pack(pady=(0,2))
        links.append(link)
        
    
global links
links=[]

B=Tkinter.Button(window, text ="Search", command = helloCallBack, font=("Helvetica", 10))     
B.pack(pady=20)

window.mainloop()                 