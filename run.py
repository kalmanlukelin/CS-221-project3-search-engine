import Tkinter
import tkMessageBox
import os
import search
window = Tkinter.Tk()
window.title('my window')
window.geometry('400x200')

lq = Tkinter.Label(window,text='query')
lq.pack();
q = Tkinter.Entry(window) #query

q.pack()
ln = Tkinter.Label(window,text='num')
ln.pack();
n = Tkinter.Entry(window) #num
n.pack()
#res=search(sys.argv[1],sys.argv[2])

	#for r in res: print (r)
def helloCallBack():
	query=q.get()
	query=query.replace(' ','_')
	num=n.get()
	if(num.isdigit()==False):
		tkMessageBox.showinfo( "Warning", "Please type an Integer")
		return
	res = search.search(query,num)
	result = ""
	for r in res: result+=r+"\n"+"\n"
	tkMessageBox.showinfo( "Result", result)
	#os.system('python search.py as 5')
	#os.system('python search.py %s %s' %(query,num,))
   #
B = Tkinter.Button(window, text ="send", command = helloCallBack)
                  
B.pack()
window.mainloop()                 