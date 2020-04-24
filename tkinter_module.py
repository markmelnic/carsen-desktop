
from backup_module import *
from search_module import *
from checker_module import *
from remover_module import *

import os
import threading as th
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkfont

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
            st.close()
            
        window_show = int(settings[1])
        win_size = str(settings[3].strip("\n"))
        win_resizeability = int(settings[5])
        
        # change settings
        #self.geometry(win_size)
        if win_resizeability == 0:
            self.resizable(0, 0)
    
        '''
        # tk options
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family='Montserrat')
        self.configure(bg='#fff')
        '''
        
        self._frame = None
        self.switch_frame(SearchPage)
            
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

        
def navMenu(self, master, nr):
    navmenu = Frame(self)
    navmenu.config(height = 50, width = 600)
    navmenu.grid(row = 0, column = 0,sticky="new")
    
    
    navf = tkfont.Font(family='Montserrat' ,size=16 ,weight="bold")
    # nav search button
    searchIcon = PhotoImage(file="./resources/icons/search.png")
    searchIcon = searchIcon.subsample(8,8) 
    navSearchButton = Button(navmenu, image = searchIcon, text = 'Search', compound = LEFT, bg='#fff',command=lambda: master.switch_frame(SearchPage))
    if nr == 1:
        navSearchButton.config(relief=SUNKEN)
    navSearchButton['font'] = navf
    navSearchButton.image = searchIcon
    navSearchButton.grid(row=10, column=10)
    navSearchButton.config(width=150, height=50)
    
    # nav track button
    trackIcon = PhotoImage(file="./resources/icons/radar.png")
    trackIcon = trackIcon.subsample(8,8) 
    navTrackButton = Button(navmenu, image = trackIcon, text = 'Track', compound = LEFT, bg='#fff',command=lambda: master.switch_frame(TrackPage))
    if nr == 2:
        navTrackButton.config(relief=SUNKEN)
    navTrackButton['font'] = navf
    navTrackButton.image = trackIcon
    navTrackButton.grid(row=10, column=20)
    navTrackButton.config(width=150, height=50)
    
    # nav favorites button
    favoIcon = PhotoImage(file="./resources/icons/favorites.png")
    favoIcon = favoIcon.subsample(6,6) 
    navFavoButton = Button(navmenu, image = favoIcon, text = 'Favorites', compound = LEFT, bg='#fff')
    navFavoButton['font'] = navf
    navFavoButton.image = favoIcon
    navFavoButton.grid(row=10, column=30)
    navFavoButton.config(width=150, height=50)
    
    # nav settings button
    settingsIcon = PhotoImage(file="./resources/icons/settings.png")
    settingsIcon = settingsIcon.subsample(8,8) 
    navSettingsButton = Button(navmenu, image = settingsIcon, text = 'Settings', compound = LEFT, bg='#fff')
    navSettingsButton['font'] = navf
    navSettingsButton.image = settingsIcon
    navSettingsButton.grid(row=10, column= 40)
    navSettingsButton.config(width=150, height=50)
        
        
class SearchPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        nr = 1
        navMenu(self, master, nr)
    # ========== MAIN CONTENT
        titlef = tkfont.Font(family='Montserrat' ,size=16)
        labelf = tkfont.Font(family='Montserrat' ,size=12)
        
        mainc = ttk.Frame(self)
        mainc.config(width = 600, height = 700)
        mainc.grid(row = 20, column = 0,sticky="new")
        
        title = ttk.Label(mainc, text = "Index a new search")
        title.grid(row = 10, column = 10, columnspan = 40,padx=(10,10), pady=(5,5))
        title['font'] = titlef
        
        '''
        # Vehicle type radio button
        vehTypeTxt = ttk.Label(mainc, text="Vehicle type:",justify = RIGHT)
        vehTypeTxt['font'] = labelf
        vehTypeTxt.grid(row=20,column=50,padx=(10,10), pady=(5,5), sticky = 'e')
        
        vehs = ["sedan", "suv"]
        images = [PhotoImage(file="./resources/vehicles/sedan.png"),PhotoImage(file="./resources/vehicles/suv.png")]
        
        cbs = [1,2]
        for i in range(len(vehs)):
            cbs[i] = Checkbutton(mainc,text = vehs[i], image = images[i],indicatoron=False,onvalue=1, offvalue=0,compound='top',bg='#fff')
            cbs[i].image = images[i]
            cbs[i]['font'] = titlef
            cbs[i].grid(row=(30+i*10),column=50, padx=5,pady=5) 
        '''
        
        # manufacturer
        makeTxt = ttk.Label(mainc, text="Car manufacturer:")
        makeTxt['font'] = labelf
        makeTxt.grid(row=20,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        makeField = ttk.Entry(mainc)
        makeField.grid(row=20,column=20)
        

        # model
        modelTxt = ttk.Label(mainc, text="Car model:")
        modelTxt['font'] = labelf
        modelTxt.grid(row=30,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        modelField = ttk.Entry(mainc)
        modelField.grid(row=30,column=20)


        # price
        priceTxt = ttk.Label(mainc, text="Price range (EURO):")
        priceTxt['font'] = labelf
        priceTxt.grid(row=40,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldpriceTxtFrom = ttk.Entry(mainc)
        fieldpriceTxtFrom.grid(row=40,column=20)
        #to
        priceTxtTo = ttk.Label(mainc, text="to")
        priceTxtTo['font'] = labelf
        priceTxtTo.grid(row=40,column=30,padx=(10,10), pady=(5,5))
        fieldpriceTxtTo = ttk.Entry(mainc)
        fieldpriceTxtTo.grid(row=40,column=40)
        
        
        # mileage
        mileageTxt = ttk.Label(mainc, text="Mileage range (KM):")
        mileageTxt['font'] = labelf
        mileageTxt.grid(row=50,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldmileageTxtFrom = ttk.Entry(mainc)
        fieldmileageTxtFrom.grid(row=50,column=20)
        #to
        mileageTxtTo = ttk.Label(mainc, text="to")
        mileageTxtTo['font'] = labelf
        mileageTxtTo.grid(row=50,column=30,padx=(10,10), pady=(5,5))
        fieldmileageTxtTo = ttk.Entry(mainc)
        fieldmileageTxtTo.grid(row=50,column=40)
        
        
        # mileage
        regTxt = ttk.Label(mainc, text="Registration years:")
        regTxt['font'] = labelf
        regTxt.grid(row=60,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldregTxtFrom = ttk.Entry(mainc)
        fieldregTxtFrom.grid(row=60,column=20)
        #to
        regTxtTo = ttk.Label(mainc, text="to")
        regTxtTo['font'] = labelf
        regTxtTo.grid(row=60,column=30,padx=(10,10), pady=(5,5))
        fieldregTxtTo = ttk.Entry(mainc)
        fieldregTxtTo.grid(row=60,column=40)
        
        
        # search button
        srcButton = Button(mainc, text="Search!",bg='#5e5e5e', fg='#eae8e8')
        srcButton.grid(row=70,column=10,columnspan=40,padx=(10, 10),pady=(10, 10))
        srcButton['font'] = titlef

        
class TrackPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        nr = 2
        navMenu(self, master, nr)  
    # ========== MAIN CONTENT

        
'''
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
'''