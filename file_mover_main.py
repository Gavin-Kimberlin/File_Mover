from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import os
import sqlite3
import time
import shutil

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("File Mover")
        self.minsize(500, 150)
        self.sourceButton()
        self.destinationButton()
        self.source_directory = tk.Entry(self.master,text='',width=50)
        self.source_directory.grid(row=0,column=1,rowspan=1,columnspan=3,padx=15,pady=22)
        self.destination_directory = tk.Entry(self.master,text='',width=50)
        self.destination_directory.grid(row=1,column=1,rowspan=1,columnspan=3,padx=15,pady=12)
 
 
 
    def sourceButton(self):
        self.source_button = ttk.Button(self.master, text = "Browse A Source Directory",command = self.sourceFileDialog)
        self.source_button.grid(column=0,row=0,padx=15,pady=20)
 
 
    def sourceFileDialog(self):
 
        self.sourcedirectoryname = filedialog.askdirectory(initialdir =  "/", title = "Select A Source Directory")
        self.label = ttk.Label(self.master, text = "")
        self.source_directory.insert(0,self.sourcedirectoryname)
        if len(self.destination_directory.get()) > 0 and len(self.source_directory.get()) > 0:
            self.swaptxt()

    def destinationButton(self):
        self.destination_button = ttk.Button(self.master, text = "Browse A Destination Directory",command=self.destinationFileDialog)
        self.destination_button.grid(column=0,row=1,padx=15,pady=10)
 
 
    def destinationFileDialog(self):
 
        self.destinationdirectoryname = filedialog.askdirectory(initialdir =  "/", title = "Select A Destination Directory")
        self.label = ttk.Label(self.master, text = "")
        self.destination_directory.insert(0,self.destinationdirectoryname)
        if len(self.destination_directory.get()) > 0 and len(self.source_directory.get()) > 0:
            self.swaptxt()

        
    def swaptxt(self):
        self.swaptxt_button = ttk.Button(self.master,text="Transfer txt Files",command=self.kill_window)
        self.swaptxt_button.grid(column=2,row=2)


    def kill_window(self):
        source_dir_list = os.listdir(self.sourcedirectoryname)
        destination_dir_list = os.listdir(self.destinationdirectoryname)
        self.source_directory.destroy()
        self.destination_directory.destroy()
        self.source_button.destroy()
        self.destination_button.destroy()
        self.swaptxt_button.destroy()
        self.iterate_source()


    def iterate_source(self):
        self.source_files = []
        self.file_names = []
        self.destination_files = []
        self.file_mtime = []
        for f in os.listdir(self.sourcedirectoryname):
            if f.endswith('.txt'):
                self.file_names.append(f)
                
                spath = self.sourcedirectoryname + "/"
                source = os.path.join(spath,f)
                self.source_files.append(source)
                
                dpath = self.destinationdirectoryname + "/"
                destination = os.path.join(dpath,f)
                self.destination_files.append(destination)

                dest = shutil.move(source,destination)                

                modtime = time.ctime(os.path.getmtime(os.path.join(dpath,f)))
                self.file_mtime.append(modtime)

                msg = "File {} was moved from {} to {} and was last modified on {} \n".format(f,spath,dpath,modtime)
                print(msg)
        
        self.create_db()


    def create_db(self):
        conn = sqlite3.connect('txt_files.db')
        with conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE if not exists tbl_files( \
                ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                col_fileName TEXT, \
                col_modTime TEXT \
                );")
            conn.commit()
        conn.close()
        self.txt_to_db()

        
    def txt_to_db(self):
        txtFile = self.file_names
        mtime = self.file_mtime
        i = 0
        while i < len(txtFile):
            currentTxt = txtFile[i]
            currentMtime = mtime[i]
            conn = sqlite3.connect('txt_files.db')
            with conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tbl_files(col_fileName, col_modTime) VALUES (?,?)", \
                               (currentTxt, currentMtime))
                conn.commit()
            conn.close()
            i += 1

        



if __name__ == "__main__":
    root = Root()
    root.mainloop()
    
