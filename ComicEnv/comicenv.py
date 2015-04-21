import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmes
import tkinter.filedialog as fileDialog
import sqlite3
import datetime
import time
import csv

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S")) 

def popupmsg(msg):
    # Creates a popup message
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=30, padx=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def confirmExit():
    # Exits the program
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
        helpmenu.add_command(label="About ComicEnv", command=lambda: popupmsg("""
ComicEnv - Copyright 2015

      By Andrew Edwards
Contact: SilvinLight@Gmail.com

Covered under the MIT license"""))
        helpmenu.add_separator()
        helpmenu.add_command(label="Help", command=lambda: popupmsg("Need help? Call Me!"))
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

        # Create Treeview to hold information
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

        # Add button for search
        searchButton = ttk.Button(self, text="Search", command=self.onFilter)
        # Add Entry for search
        self.searchEntry = ttk.Entry(self)
        self.searchEntry.delete(0, last="end")

        # Add Clear button
        clearButton = ttk.Button(self, text="Clear", command=self.clearCmd)

        # Add Navigation button
        newButton = ttk.Button(self, text="New Product", command=lambda: controller.show_frame(NewProduct))

        # Add import button
        importButton = ttk.Button(self, text="Import CSV", command=self.importCmd)

        # Pack the widgets
        self.tree.pack(fill="both", expand=True)
        searchButton.pack(side="left", padx=4, pady=2)
        self.searchEntry.pack(side="left", padx=4, pady=2)
        newButton.pack(side="left", padx=4, pady=2)
        importButton.pack(side="left", padx=4, pady=2)
        clearButton.pack(side="left", padx=4, pady=2)

    def onFilter(self):
        """Filter Callback"""
        searchField = self.searchEntry.get()
        self.filter(searchField)

    def filter(self, sf):
        """Returns filtered values to treeview"""
        try:
            conn = sqlite3.connect("ComicEnv.db")
            c = conn.cursor()
            c.execute("SELECT title, quantity, price, date FROM cdata WHERE title=?", (sf,))
            # title should have a default value to return everything.
            returnedRows = c.fetchall()
            for row in returnedRows:
                pass #Not sure what to put here
            conn.close()
        except:
            popupmsg("Error: filter module error")
        finally:
            if conn:
                conn.close()
        # This is most likely broken. Has not been tested.

    def clearCmd(self):
        """ Clears the treeview"""
        self.tree.delete(*self.tree.get_children())

    def importCmd(self):
        """Import a .csv file and store it in the db"""
        self.fileName = fileDialog.askopenfilename(filetypes = (("Spread Sheet Files", "*.csv"),
                                                   ("All Files", "*.*")))


class LastRecord(tk.Frame):
    """Update an existing record"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(padx=10, pady=10)


class NewProduct(tk.Frame):
    """New product entry."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Add Labels
        tLabel = ttk.Label(self, text="Title: ", font=NORM_FONT).grid(row=0, padx=5, pady=5)
        qLabel = ttk.Label(self, text="Quantity: ", font=NORM_FONT).grid(row=1, padx=5, pady=5)
        pLabel = ttk.Label(self, text="Price: $", font=NORM_FONT).grid(row=2, padx=5, pady=5)

        # Add Entry
        self.te = ttk.Entry(self)
        self.qe = ttk.Entry(self)
        self.pe = ttk.Entry(self)

        # Add Buttons
        saveButton = ttk.Button(self, text="Save", command=self.onSave)
        cancelButton = ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(Overview))
        clearButton =  ttk.Button(self, text="Clear", command=self.clearCmd)

        # Pack the widgets
        cancelButton.grid(row=4, column=1, padx=2)
        clearButton.grid(row=4, column=2, padx=2)
        saveButton.grid(row=4, padx=2)

        self.te.grid(row=0, column=1, padx=5, pady=5)
        self.qe.grid(row=1, column=1, padx=5, pady=5)
        self.pe.grid(row=2, column=1, padx=5, pady=5)

    def clearCmd(self):
        """Clear the entry widgets"""
        self.te.delete(0, 'end')
        self.qe.delete(0, 'end')
        self.pe.delete(0, 'end')

    def onSave(self):
        # Checks if title entry is blank
        if not self.te.get():
            popupmsg("Oops, it looks like your book is missing it's title!")
        else:
            # Gets the user input
            title = self.te.get()
            quantity = self.qe.get()
            price = self.pe.get()
            self.save(title, quantity, price)

    def save(self, title, quantity, price):
        # Saves the user input to the database
        try:
            conn = sqlite3.connect("ComicEnv.db")
            c = conn.cursor()
            c.execute("INSERT INTO cdata(unix, datestamp, title, quantity, price) VALUES (?,?,?,?,?)",
                      (time.time(), date, title, quantity, price))
            conn.commit()
            conn.close()
            self.clearCmd()
            popupmsg("Success!")
        except:
            popupmsg("Error: save error")
        finally:
            if conn:
                conn.close()
        

app = ComicEnv()
app.minsize(450, 270)
if "nt" == os.name:
    app.wm_iconbitmap(bitmap = "comicenv.ico")
else:
    pass
#need to turn the icon into a xbm file for Linux compatibility
app.title("ComicEnv")
app.mainloop()
