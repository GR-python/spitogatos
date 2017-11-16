from tkinter import *
from tkinter import messagebox
from crawl_functions import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(expand=1, fill=BOTH)
        self.init_window()
        self.populate_listbox1()

    def init_window(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        scrollbar1 = Scrollbar(self, orient=VERTICAL)
        self.lb1 = Listbox(self, yscrollcommand=scrollbar1.set)  ##
        self.lb1.grid(column=0, row=0, padx=10, pady=5, sticky=W + E + N + S)
        self.lb1.bind("<Return>", self.handler_lb1)
        scrollbar1.config(command=self.lb1.yview)
        scrollbar1.grid(column=1, row=0, sticky=N + S)

        scrollbar2 = Scrollbar(self, orient=VERTICAL)
        self.lb2 = Listbox(self, yscrollcommand=scrollbar2.set)  # .grid(row=30,column=30)##
        self.lb2.grid(column=2, row=0, padx=10, pady=5, sticky=W + E + N + S)
        self.lb2.bind("<Double-1>", self.handler_lb2)
        self.lb2.bind("<Return>", self.handler_lb2)
        scrollbar2.config(command=self.lb2.yview)
        scrollbar2.grid(column=3, row=0, sticky=N + S)

        searchButton = Button(self, text="Αναζητηση", command=self.populate_listbox2)
        searchButton.grid(column=0, row=1, sticky=W + E, padx=5, pady=5)

        quitButton = Button(self, text="Εξοδος", command=self.quit)
        quitButton.grid(row=1, column=2, sticky=E + W, padx=5, pady=5)  # 0.0 ei

        self.statusBar=Label(self, text=' ', border=2, relief=SUNKEN, anchor=W)
        self.statusBar.grid(row=2, column=0, columnspan=3, sticky=E+W, padx=5, pady=10, ipady=3, ipadx=3)

    def populate_listbox1(self):
        for sxoli in get_sxoles_spitogatos():
            self.lb1.insert(END, sxoli)

    def populate_listbox2(self):
        url_sxolis = self.lb1.get(self.lb1.curselection())[1]
        text, self.spitia = get_spitia_sxolis(url_sxolis)
        self.lb2.delete(0, END)
        for spiti in self.spitia:
            self.lb2.insert(END, spiti['description']+ ' ' +spiti['area']+' '+spiti['price'][7:]+'€')
        self.statusBar.config(text= self.lb1.get(self.lb1.curselection())[0]+' '+text)

    def handler_lb2(self, event):
        url = self.spitia[self.lb2.curselection()[0]]['url']
        details = get_details_per_house(url)
        messagebox.showinfo('hello', details)

    def handler_lb1(self, event):
        self.populate_listbox2()

    def change_status (self, event):
        self.statusBar.config(text=self.lb1.get(self.lb1.curselection())[0])

def create_menu(Window_object):
    menu=Menu(Window_object)
    Window_object.config(menu=menu)

    arxeio = Menu(menu)
    arxeio.add_command(label='Έξοδος', command=Window_object.quit)
    menu.add_cascade(label='Αρχείο', menu=arxeio)

    anazitisi=Menu(menu)
    anazitisi.add_command(label='Αναζήτηση', command=app.populate_listbox2)
    menu.add_cascade(label='Αναζήτηση', menu=anazitisi)

if __name__=='__main__':
    root =Tk()
    root.title("ΑΝΑΖΗΤΗΣΗ ΦΟΙΤΗΤΙΚΗΣ ΚΑΤΟΙΚΙΑΣ ΑΠΟ ΣΠΙΤΟΓΑΤΟ")
    app = Window(root)
    create_menu(root)
    root.mainloop()
