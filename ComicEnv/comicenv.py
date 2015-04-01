import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmes
import sqlite3
import time
import datetime

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S")) 

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=30, padx=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def confirmExit():
    confirm = tkmes.askquestion("Confirm Quit", "Are you sure you want to exit?")
    if confirm == 'yes':
        quit()

class ComicEnv(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Database", command=lambda: popupmsg("Not supported just yet"))
        filemenu.add_command(label="Change Database", command=lambda:popupmsg("Not supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=confirmExit)
        menubar.add_cascade(label="File", menu=filemenu)

        navmenu = tk.Menu(menubar, tearoff=0)
        navmenu.add_command(label="Overview", command=lambda: popupmsg('Not functioning yet.'))
        navmenu.add_command(label="Last Record", command=lambda: popupmsg('Not functioning yet'))
        navmenu.add_command(label="New Record", command=lambda: popupmsg('Not functioning yet'))
        menubar.add_cascade(label="Navigation", menu=navmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About ComicEnv", command=lambda: popupmsg("""ComicEnv - Copyright 2015
By Andrew Edwards
Contact: SilvinLight@Gmail.com

Covered under the MIT license"""))
        helpmenu.add_separator()
        helpmenu.add_command(label="Help", command=lambda: popupmsg("This should contain a help wiki"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (Overview, LastRecord, NewProduct):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nesw")

        self.show_frame(Overview)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Overview(tk.Frame):
    """Initial start page. Main hub of program."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.tree = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.config(command=self.tree.yview)
        self.tree.heading('#0', text='Title', anchor='w')

        
        self.tree["columns"]=("quantity", "price", "date")
        self.tree.column("quantity")
        self.tree.column("price")
        self.tree.column("date")
        self.tree.heading("quantity", text="Quant." )
        self.tree.heading("price", text="Price" )
        self.tree.heading("date", text="Date" )

        self.tree.pack()
        
        # Create a function for poplation of information from db

class LastRecord(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

class NewProduct(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)                

        tLabel = ttk.Label(self, text="Title: ", font=NORM_FONT).grid(row=0, padx=5, pady=5)
        qLabel = ttk.Label(self, text="Quantity: ", font=NORM_FONT).grid(row=1, padx=5, pady=5)
        pLabel = ttk.Label(self, text="Price: $", font=NORM_FONT).grid(row=2, padx=5, pady=5)
        self.te = ttk.Entry(self)
        self.te.grid(row=0, column=1, padx=5, pady=5)
        self.qe = ttk.Entry(self)
        self.qe.grid(row=1, column=1, padx=5, pady=5)
        self.pe = ttk.Entry(self)
        self.pe.grid(row=2, column=1, padx=5, pady=5)
        
        saveButton = ttk.Button(self, text="Save", command=self.on_save)
        saveButton.grid(row=4, padx=5)
        cancelButton = ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(Overview))
        cancelButton.grid(row=4, column=1, padx=5)

    def on_save(self):
        title = self.te.get()
        quantity = self.qe.get()
        price = self.pe.get()
        self.save(title, quantity, price)
        

    def save(self, title, quantity, price):
        conn = sqlite3.connect("ComicEnv.db")
        c = conn.cursor()
        c.execute("INSERT INTO cdata(unix, datestamp, title, quantity, price) VALUES (?,?,?,?,?)",
                  (time.time(), date, title, quantity, price))
        conn.commit()
        conn.close()
        # Add Confirmation of success. Return to Overviews
        

app = ComicEnv()
app.mainloop()
