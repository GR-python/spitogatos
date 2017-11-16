from tkinter import *

root=Tk()
canvas1=Canvas(root,width=600, height=400)
canvas1.pack()
canvas1.create_line(0,0,600,200)
canvas1.create_line(0,400,600,200, fill='red')
canvas1.create_rectangle(100,100,400,200, fill='#00ff00', line='#ff0000')

root.mainloop()