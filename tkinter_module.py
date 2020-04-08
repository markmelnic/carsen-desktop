
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

# read settings
with open('settings.txt', mode='r') as st:
    settings = st.readlines()
    window_show = int(settings[1])
    st.close()
    win_size = str(settings[3].strip("\n"))
    win_resizeability = str(settings[5])

class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Mobile.de Bot")
        self.iconbitmap('icon.ico')

        # change settings
        self.geometry(win_size)
        if win_resizeability == 0:
            self.resizable(False, False)

        # progress bar
        class progressBar:
            progressbar = Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
            progressbar.place(x=0, y=700, width=1280)
            progressbar.start()

        # search
        class Search:
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

                srchThread = th.Thread(target=search, args = (maindir, srcInput))
                srchThread.start()

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
            priceTxt = Label(text="price range (EURO):")
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
            def chck():
                checker(maindir)

            # check button
            chckText = Label(text="Check existing files for changes")
            chckText.grid(row=0,column=2,columnspan=2,padx=(10, 10),pady=(10, 10))
            chckText['font'] = font.Font(family='Helvetica')
            chckText['font'] = font.Font(size=15)

            chckButton = Button(self, text="Check", command=chck)
            chckButton.grid(row=1,column=2,padx=(10, 10),pady=(5, 0))

        # remove
        class Remove:
            def rm():
                remover(maindir)

            # remove button
            removeText = Label(text="Stop tracking a search")
            removeText.grid(row=0,column=4,columnspan=2,padx=(10, 10),pady=(10, 10))
            removeText['font'] = font.Font(family='Helvetica')
            removeText['font'] = font.Font(size=15)

            removeButton = Button(self, text="Remove", command=rm)
            removeButton.grid(row=1,column=4,padx=(10, 10),pady=(5, 0))

        # backup
        class Backup:
            def bck():
                backup(maindir)

            # backup button
            backupText = Label(text="Backup existing searches")
            backupText.grid(row=0,column=6,columnspan=2,padx=(10, 10),pady=(10, 10))
            backupText['font'] = font.Font(family='Helvetica')
            backupText['font'] = font.Font(size=15)

            backupButton = Button(self, text="Backup", command=bck)
            backupButton.grid(row=1,column=6,padx=(10, 10),pady=(5, 0))