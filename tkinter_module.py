
from backup_module import *
from search_module import *
from checker_module import *
from remover_module import *

import os
import threading as th
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font


global maindir
maindir = os.getcwd()

class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Mobile.de Bot")
        self.iconbitmap('./resources/icon.ico')

        # read settings
        with open('./resources/settings.txt', mode='r') as st:
            settings = st.readlines()
            window_show = int(settings[1])
            st.close()
            win_size = str(settings[3].strip("\n"))
            win_resizeability = str(settings[5])

            # change settings
            self.geometry(win_size)
            if win_resizeability == 0:
                self.resizable(0, 0)

        # feedback text
        class Feedback:
            def working():
                global workingText
                workingText = Label(text="Working, please wait...",background ="yellow",font=("Helvetica", 16))
                workingText.grid(row=16,column=0,columnspan=2,padx=(10, 10),pady=(10, 10))

            def successful():
                try:
                    workingText.grid_remove()
                except:
                    None
                    
                global successfulText
                try:
                    successfulText.grid_remove()
                except:
                    None
                    
                successfulText = Label(text="Execution Successful",background ="light green",font=("Helvetica", 16))
                successfulText.grid(row=16,column=0,columnspan=2,padx=(10, 10),pady=(10, 10))
                time.sleep(10)
                successfulText.grid_remove()

        # search
        class Search:
            def threadder(workingText, thread):
                thread.join()
                tree = Remover.tree
                Remover.filesList(tree)
                Feedback.successful()


            def retrieve_inputs():
                srcInput = []
                srcInput.append(Search.makeField.get())
                srcInput.append(Search.modelField.get())
                srcInput.append(Search.fieldpriceTxtFrom.get())
                srcInput.append(Search.fieldpriceTxtTo.get())
                srcInput.append(Search.fieldregTxtFrom.get())
                srcInput.append(Search.fieldregTxtTo.get())
                srcInput.append(Search.fieldmileageTxtFrom.get())
                srcInput.append(Search.fieldmileageTxtTo.get())
                srcInput.append(Search.fieldpowerTxtFrom.get())
                srcInput.append(Search.fieldpowerTxtTo.get())

                threads = []
                srchThread = th.Thread(target=search, args = (maindir, srcInput))
                srchThread.start()

                Feedback.working()

                threads.append(srchThread)
                threadsThread = th.Thread(target=Search.threadder, args = (workingText, threads[0],))
                threadsThread.start()

            # search button
            srcButton = Button(self, text="Search",command=retrieve_inputs)
            srcButton.grid(row=15,column=0,columnspan = 2,padx=(10, 10),pady=(5, 0))

            srcText = Label(text="Create a new search")
            srcText.grid(row=0,column=0,columnspan = 2,padx=(10, 10),pady=(10, 10))
            srcText['font'] = font.Font(family='Helvetica')
            srcText['font'] = font.Font(size=15)


            # manufacturer
            makeTxt = Label(text="Car manufacturer")
            makeTxt.grid(row=1,column=0,padx=(10, 10),pady=(10, 10))
            makeField = Entry()
            makeField.grid(row=1,column=1,padx=(10, 10),pady=(10, 10))


            # model
            modelTxt = Label(text="Car model")
            modelTxt.grid(row=2,column=0,padx=(10, 10),pady=(10, 10))
            modelField = Entry()
            modelField.grid(row=2,column=1,padx=(10, 10),pady=(10, 10))


            # price
            priceTxt = Label(text="Price range (EURO):")
            priceTxt.grid(row=3,column=0,padx=(10, 5),pady=(10, 10))
            # from
            priceTxtFrom = Label(text="From")
            priceTxtFrom.grid(row=4,column=0,padx=(10, 5))
            fieldpriceTxtFrom = Entry()
            fieldpriceTxtFrom.grid(row=4,column=1,padx=(5, 5))
            #to
            priceTxtTo = Label(text="to")
            priceTxtTo.grid(row=5,column=0,padx=(5, 5))
            fieldpriceTxtTo = Entry()
            fieldpriceTxtTo.grid(row=5,column=1,padx=(5, 5))


            # reg
            regTxt = Label(text="Registration years range:")
            regTxt.grid(row=6,column=0,padx=(10, 5),pady=(10, 10))
            # from
            regTxtFrom = Label(text="From")
            regTxtFrom.grid(row=7,column=0,padx=(10, 5))
            fieldregTxtFrom = Entry()
            fieldregTxtFrom.grid(row=7,column=1,padx=(5, 5))
            #to
            regTxtTo = Label(text="to")
            regTxtTo.grid(row=8,column=0,padx=(5, 5))
            fieldregTxtTo = Entry()
            fieldregTxtTo.grid(row=8,column=1,padx=(5, 5))


            # mileage
            mileageTxt = Label(text="Mileage range (KM):")
            mileageTxt.grid(row=9,column=0,padx=(10, 5),pady=(10, 10))
            # from
            mileageTxtFrom = Label(text="From")
            mileageTxtFrom.grid(row=10,column=0,padx=(10, 5))
            fieldmileageTxtFrom = Entry()
            fieldmileageTxtFrom.grid(row=10,column=1,padx=(5, 5))
            #to
            mileageTxtTo = Label(text="to")
            mileageTxtTo.grid(row=11,column=0,padx=(5, 5))
            fieldmileageTxtTo = Entry()
            fieldmileageTxtTo.grid(row=11,column=1,padx=(5, 5))


            # power
            powerTxt = Label(text="Power range (HP):")
            powerTxt.grid(row=12,column=0,padx=(10, 5),pady=(10, 10))
            # from
            powerTxtFrom = Label(text="From")
            powerTxtFrom.grid(row=13,column=0,padx=(10, 5))
            fieldpowerTxtFrom = Entry()
            fieldpowerTxtFrom.grid(row=13,column=1,padx=(5, 5))
            #to
            powerTxtTo = Label(text="to")
            powerTxtTo.grid(row=14,column=0,padx=(5, 5))
            fieldpowerTxtTo = Entry()
            fieldpowerTxtTo.grid(row=14,column=1,padx=(5, 5))

        # check
        class Check:
            def chckThread(workingText, thread):
                thread.join()
                Check.printTable()
                Feedback.successful()

            def chck():
                chckerThread = th.Thread(target=checker, args=(maindir,))
                chckerThread.start()
                
                Feedback.working()
                
                threads = []
                threads.append(chckerThread)
                threadsThread = th.Thread(target=Check.chckThread, args = (workingText, threads[0],))
                threadsThread.start()
                
            def printTable():
                os.chdir(maindir)
                os.chdir("./csv files")
                with open("changesTemp.csv", mode="r", newline='') as changesFile:
                    changesReader = csv.reader(changesFile)
                    changes = list(changesReader)
                    changesFile.close()
                print(changes)
                for i in range(len(changes)):
                    col = "column"+str(i)
                    if int(changes[i][2]) > 0:
                        pr = "+" + str(changes[i][2])
                    else:
                        pr = changes[i][2]
                    ch_tree.insert('', 'end', col, text=changes[i][0], values=(int(changes[i][1]) + 1, pr))
                os.remove("changesTemp.csv")
                os.chdir(maindir)

            # check button
            chckText = Label(text="Check existing files for changes")
            chckText.grid(row=2,column=2,columnspan=2,padx=(10, 10),pady=(10, 10))
            chckText['font'] = font.Font(family='Helvetica')
            chckText['font'] = font.Font(size=15)

            chckButton = Button(self, text="Check", command=chck)
            chckButton.grid(row=3,column=2,columnspan=2,padx=(10, 10),pady=(5, 0))
            
            global ch_tree
            # tree
            ch_tree = Treeview()
            ch_tree["columns"]=("line","change")
            ch_tree.column("#0", width=200, minwidth=10)
            ch_tree.column("#1", width=100, minwidth=10)
            ch_tree.column("#2", width=100, minwidth=10)
            
            ch_tree.heading("#0",text="File",anchor=W)
            ch_tree.heading("#1", text="Line",anchor=W)
            ch_tree.heading("#2", text="Change",anchor=W)
            
            ch_tree.grid(row=4,column=2, columnspan=2,rowspan=10)

        # remove
        class Remover:
            def removeThread(items_to_remove):
                remover(maindir, items_to_remove)
                Feedback.successful()
                
            def rm():
                items_to_remove = tuple(Remover.tree.selection())
                print(items_to_remove, " - items to remove")
                
                chckerThread = th.Thread(target=Remover.removeThread, args = (items_to_remove,))
                chckerThread.start()
                for item in items_to_remove:
                    print("2")
                    Remover.tree.delete(item)

            def filesList(tree):
                try:
                    os.chdir(maindir)
                    files = []
                    with os.scandir("./csv files") as entries:
                        for entry in entries:
                            if entry.is_file():
                                files.append(entry.name)
                    for item in items_in_tree:
                        Remover.tree.delete(item)
                except:
                    None
                os.chdir(maindir)
                files = []
                with os.scandir("./csv files") as entries:
                    for entry in entries:
                        if entry.is_file():
                            files.append(entry.name)

                for i in range(len(files)):
                    try:
                        filename = str(files[i])
                        params = filename.split('_')
                        params = [p.replace('-', ' - ') for p in params]
                        params = [p.replace('.csv', '') for p in params]
                        params[1] = params[1].replace(' - ', ' ')
                        tree.insert('', 'end', files[i], text=params[0], values=(params[1],params[2],params[3],params[4],params[5]))
                    except:
                        None
                return tree

            removeDesc = Label(text="The dash (-) in columns price - power represents the search parameters\nby wich the ads have been indexed. They follow the format: from - to\n Exaple for registration: from 2012 - to 2018")
            removeDesc.grid(row=1,column=4, columnspan=2)
            removeDesc['font'] = font.Font(family='Helvetica')
            removeDesc['font'] = font.Font(size=13)
            
            tree = Treeview()
            tree["columns"]=("model","price","reg","mileage","power")
            tree.column("#0", width=100, minwidth=10)
            tree.column("#1", width=100, minwidth=10)
            tree.column("#2", width=100, minwidth=10)
            tree.column("#3", width=100, minwidth=10)
            tree.column("#4", width=100, minwidth=10)
            tree.column("#5", width=100, minwidth=10)
            
            tree.heading("#0",text="Make",anchor=W)
            tree.heading("#1", text="Model",anchor=W)
            tree.heading("#2", text="Price",anchor=W)
            tree.heading("#3", text="Registration",anchor=W)
            tree.heading("#4", text="Mileage",anchor=W)
            tree.heading("#5", text="Power",anchor=W)
            
            tree.grid(row=2,column=4, columnspan=2,rowspan=10)

            # remove button
            removeText = Label(text="Stop tracking a search")
            removeText.grid(row=0,column=4,padx=(10, 10))
            removeText['font'] = font.Font(family='Helvetica')
            removeText['font'] = font.Font(size=15)

            removeButton = Button(self, text="Remove", command=rm)
            removeButton.grid(row=0,column=5,padx=(10, 10))

            tree = filesList(tree)

        # backup
        class Backup:
            def backupthread():
                backup(maindir)
                Feedback.successful()

            def bck():
                bckupThread = th.Thread(target=Backup.backupthread)
                bckupThread.start()

            # backup button
            backupText = Label(text="Backup existing searches")
            backupText.grid(row=0,column=2,columnspan=2,padx=(10, 10),pady=(10, 10))
            backupText['font'] = font.Font(family='Helvetica')
            backupText['font'] = font.Font(size=15)

            backupButton = Button(self, text="Backup", command=bck)
            backupButton.grid(row=1,column=2,columnspan=2,padx=(10, 10),pady=(5, 0))