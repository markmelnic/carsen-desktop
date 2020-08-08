
from backup_module import *
from search_module import *
from checker_module import *
from remover_module import *

import os
import csv
import json
import operator
import webbrowser
import threading as th

from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkfont

global maindir
maindir = os.getcwd()

        
def navMenu(self, master, nr):
    navmenu = Frame(self)
    navmenu.config(height = 50, width = 600)
    navmenu.grid(row = 0, column = 0,sticky="new")
    
    
    navf = tkfont.Font(family='Montserrat' ,size=16 ,weight="bold")
    # nav search button
    searchIcon = PhotoImage(file="./resources/icons/search.png")
    searchIcon = searchIcon.subsample(8,8) 
    navSearchButton = Button(navmenu, image = searchIcon, text = 'Search', compound = LEFT, bg='#fff', command=lambda: master.switch_frame(SearchPage))
    if nr == 1:
        navSearchButton.config(relief=SUNKEN)
    navSearchButton['font'] = navf
    navSearchButton.image = searchIcon
    navSearchButton.grid(row=10, column=10)
    navSearchButton.config(width=150, height=50)
    
    # nav track button
    trackIcon = PhotoImage(file="./resources/icons/radar.png")
    trackIcon = trackIcon.subsample(8,8) 
    navTrackButton = Button(navmenu, image = trackIcon, text = 'Track', compound = LEFT, bg='#fff', command=lambda: master.switch_frame(TrackPage))
    if nr == 2:
        navTrackButton.config(relief=SUNKEN)
    navTrackButton['font'] = navf
    navTrackButton.image = trackIcon
    navTrackButton.grid(row=10, column=20)
    navTrackButton.config(width=150, height=50)
    
    # nav favorites button
    favoIcon = PhotoImage(file="./resources/icons/favorites.png")
    favoIcon = favoIcon.subsample(6,6) 
    navFavoButton = Button(navmenu, image = favoIcon, text = 'Favorites', compound = LEFT, bg='#fff', command=lambda: master.switch_frame(FavoritesPage))
    if nr == 3:
        navFavoButton.config(relief=SUNKEN)
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


class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("CARSEN - A car tracking software")
        self.iconbitmap('./resources/icon.ico')
        # read settings
        with open('./resources/settings.json', mode='r') as st:
            settings = st.read()
            settings = (json.loads(settings))
            settings = settings['settings'][0]
            st.close()

        print(settings)
        # change settings
        self.geometry(settings["window_geometry"])
        win_res = settings["window_resizeability"].split(',')
        self.resizable(win_res[0], win_res[1])
    
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

        
class SearchPage(Frame):
        
    def __init__(self, master):
        Frame.__init__(self, master)
        
        def srcThread(thread):
            thread.join()
            master.switch_frame(TrackPage)
        
        def retrieve_inputs():
            srcInput = []
            srcInput.append(makeField.get())
            srcInput.append(modelField.get())
            srcInput.append(fieldpriceTxtFrom.get())
            srcInput.append(fieldpriceTxtTo.get())
            srcInput.append(fieldregTxtFrom.get())
            srcInput.append(fieldregTxtTo.get())
            srcInput.append(fieldmileageTxtFrom.get())
            srcInput.append(fieldmileageTxtTo.get())
            srcInput.append(fieldpowerTxtFrom.get())
            srcInput.append(fieldpowerTxtTo.get())

            threads = []
            srchThread = th.Thread(target=search, args = (maindir, srcInput))
            srchThread.start()
            threads = []
            threads.append(srchThread)
            threadsThread = th.Thread(target=srcThread, args = (threads[0],))
            threadsThread.start()
                    
        nr = 1
        navMenu(self, master, nr)
    # ========== MAIN CONTENT
        titlef = tkfont.Font(family='Montserrat' ,size=16, weight='bold')
        labelf = tkfont.Font(family='Montserrat' ,size=12)
        
        mainc = ttk.Frame(self)
        mainc.config(width = 600, height = 700)
        mainc.grid(row = 20, column = 0,sticky="new")
        
        title = ttk.Label(mainc, text = "Index a new search")
        title.grid(row = 10, column = 10, columnspan = 40,padx=(10,10), pady=(5,5))
        title['font'] = titlef
        
        '''
        # Vehicle type radio button
        vehTypeTxt = ttk.Label(mainc, text="Vehicle types:",justify = RIGHT)
        vehTypeTxt['font'] = labelf
        vehTypeTxt.grid(row=20,column=50,padx=(10,10), pady=(5,5), sticky = 'e')
        
        vehs = ["Sedan", "SUV","Estate car","Coupe/Sports car","Cabriolet/Roadster","Small/City Car"]
        images = [PhotoImage(file="./resources/vehicles/sedan.png"),PhotoImage(file="./resources/vehicles/suv.png")]
        
        cbs = [1,2,3,4,5,6]
        for i in range(len(vehs)):
            cbs[i] = Checkbutton(mainc,text = vehs[i], image = images[i],indicatoron=False,onvalue=1, offvalue=0,compound='right',bg='#fff')
            cbs[i].image = images[i]
            cbs[i]['font'] = titlef
            cbs[i].grid(row=(30+i*10),column=50, padx=5,pady=5) 
        '''
        
        # manufacturer
        makeTxt = ttk.Label(mainc, text="Car manufacturer:")
        makeTxt['font'] = labelf
        makeTxt.grid(row=20,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        
        makeField = ttk.Combobox(mainc, width = 17) 
        makeField.grid(row=20,column=20)
        
        os.chdir(maindir)
        os.chdir("./resources")
        with open("makes.json", 'r', encoding="utf-8", newline='') as mjson:
            data = mjson.read()
            makes_dict = (json.loads(data))
            makes_dict = makes_dict['makes']
            mjson.close()
            os.chdir(maindir)
            
        makes = []
        for i in range(len(makes_dict)):
            if i == 0:
                makes.append("Any")
            else:
                makes.append(makes_dict[i]['n'])
        # adding combobox drop down list 
        makeField['values'] = tuple(makes)
        makeField.current(0)

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
        
        
        # registration
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
        
        
        # engine power
        powerTxt = ttk.Label(mainc, text="Engine power (HP):")
        powerTxt['font'] = labelf
        powerTxt.grid(row=70,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldpowerTxtFrom = ttk.Entry(mainc)
        fieldpowerTxtFrom.grid(row=70,column=20)
        #to
        powerTxtTo = ttk.Label(mainc, text="to")
        powerTxtTo['font'] = labelf
        powerTxtTo.grid(row=70,column=30,padx=(10,10), pady=(5,5))
        fieldpowerTxtTo = ttk.Entry(mainc)
        fieldpowerTxtTo.grid(row=70,column=40)
        
        
        # search button
        srcButton = Button(mainc, text="Search!",bg='#5e5e5e', fg='#eae8e8', command=retrieve_inputs)
        srcButton.grid(row=80,column=10,columnspan=40,padx=(10, 10),pady=(10, 10))
        srcButton['font'] = titlef

        
class TrackPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        nr = 2
        navMenu(self, master, nr)  
        
        def chck():
            chckerThread = th.Thread(target=checker, args=(maindir,))
            chckerThread.start()
            threads = []
            threads.append(chckerThread)
            threadsThread = th.Thread(target=chckThread, args = (threads[0],))
            threadsThread.start()
            
        def chckThread(thread):
            thread.join()
            printTable()
            master.switch_frame(TrackPage)
            
        def printTable():
            os.chdir(maindir)
            os.chdir("./csv files")
            with open("changesTemp.csv", mode="r", newline='') as changesFile:
                changesReader = csv.reader(changesFile)
                changes = list(changesReader)
                changesFile.close()
            for i in range(len(changes)):
                col = "column"+str(i)
                if int(changes[i][0]) > 0:
                    pr = "+" + str(changes[i][0])
                else:
                    pr = changes[i][0]
                changesTree.insert('', 'end', text=changes[i][0], values=(changes[i][2], changes[i][3], changes[i][4], changes[i][5], changes[i][6], changes[i][1]))
            os.chdir(maindir)
            
        # main content frame
        mainc = ttk.Frame(self)
        mainc.config(width = 600, height = 700)
        mainc.grid(row = 20, column = 0,sticky="new",pady=5)
        
    # ========== SIDE BUTTONS
        # styles
        titlef = tkfont.Font(family='Montserrat' ,size=16, weight = "bold")
        labelf = tkfont.Font(family='Montserrat' ,size=12, weight = "bold")
        
        ntbkStyle = ttk.Style()
        ntbkStyle.configure('TNotebook.Tab', font=('Montserrat','11','bold'), padding=(10, 3, 10, 2))        
        
        #verify icon
        trVerifyIcon = PhotoImage(file="./resources/icons/verify.png")
        trVerifyIcon = trVerifyIcon.subsample(6,6) 
        trVerifyButton = Button(mainc, image = trVerifyIcon,compound = LEFT, bg='#fff', command = chck)
        trVerifyButton.image = trVerifyIcon
        trVerifyButton.grid(row=10, column=20,padx=10)
        trVerifyButton.config(width=50, height=50)
        
        
        # browse button
        def browseSelected():
            trees = [changesTree]
            for tree in adsTrees:
                trees.append(tree)
                
            for tree in trees:
                selectedItem = tuple(tree.selection())
                for item in selectedItem:
                    item = tree.item(item)
                    try:
                        link = item['values'][5]
                        webbrowser.open(link)
                    except:
                        None
            master.switch_frame(TrackPage)
                
        trBrowseIcon = PhotoImage(file="./resources/icons/browse.png")
        trBrowseIcon = trBrowseIcon.subsample(6,6) 
        trBrowseButton = Button(mainc, image = trBrowseIcon,compound = LEFT, bg='#fff',command = browseSelected)
        trBrowseButton.image = trBrowseIcon
        trBrowseButton.grid(row=11, column=20,padx=10)
        trBrowseButton.config(width=50, height=50)
        
        
        # add to favorites button
        def addtoFavs():
            trees = [changesTree]
            for tree in adsTrees:
                trees.append(tree)
                
            items = []
            for tree in trees:
                selectedItem = tuple(tree.selection())
                for item in selectedItem:
                    item = tree.item(item)
                    if tree == changesTree:
                        temp = item
                        temp['text'] = item['values'][0]
                        temp['values'][0] = item['values'][1]
                        temp['values'][1] = item['values'][2]
                        temp['values'][2] = item['values'][3]
                        temp['values'][3] = item['values'][4]
                        temp['values'][4] = 0
                        temp['values'][5] = item['values'][5]
                        item = temp
                        items.append(item)
                    else:
                        try:
                            items.append(item)
                        except Exception as e:
                            print(e)
                            print("no items found")
                            None
                  
            os.chdir("./csv files")      
            with open("favorites.csv", mode='a', newline='') as favsFile:
                csvWriter = csv.writer(favsFile)
                for item in items:
                    csvWriter.writerow([item['values'][5], item['text'], item['values'][0], item['values'][1], item['values'][2], item['values'][3]])
                favsFile.close()
            os.chdir(maindir)
            
            master.switch_frame(FavoritesPage)
            
        trAddtofavIcon = PhotoImage(file="./resources/icons/add_to_favorites.png")
        trAddtofavIcon = trAddtofavIcon.subsample(6,6) 
        trAddtofavButton = Button(mainc, image = trAddtofavIcon,compound = LEFT, bg='#fff',command=addtoFavs)
        trAddtofavButton.image = trAddtofavIcon
        trAddtofavButton.grid(row=12, column=20,padx=10)
        trAddtofavButton.config(width=50, height=50)


        # remove file function
        def removeFile():
            try:
                file_to_remove = files[notebk.index("current")]
                print(file_to_remove, " to remov")
                remover(maindir, file_to_remove)
                master.switch_frame(TrackPage)
            except:
                print("No file(tab) to remove")
                
        # remove file button 
        trRmIcon = PhotoImage(file="./resources/icons/trash.png")
        trRmIcon = trRmIcon.subsample(6,6) 
        trRmButton = Button(mainc, image = trRmIcon,compound = LEFT, bg='#fff', command=removeFile)
        trRmButton.image = trRmIcon
        trRmButton.grid(row=29, column=20,padx=10)
        trRmButton.config(width=50, height=50)
        
    # ========== NOTEBOOK
        # get all files in './csv files'
        with os.scandir("./csv files") as entries:
            files_to_ignore = ["<DirEntry 'changesTemp.csv'>", "<DirEntry 'changesTimestamp.txt'>", "<DirEntry 'favorites.csv'>", "<DirEntry 'favchangesTimestamp.txt'>", "<DirEntry 'favchangesTemp.csv'>"]
            files = []
            for entry in entries:
                if entry.is_file():
                    if not str(entry) in files_to_ignore:
                            files.append(entry.name)
           
        tabs = []   
        adsTrees = []  
        for i in range(len(files)):    
            tabs.append(i)
            adsTrees.append(i)
        
        # create the notebook
        notebk = ttk.Notebook(mainc,width=540, height=450)
        notebk.grid(row=10,column=10,rowspan=20,padx=5)
        for i in range(len(tabs)):
            tabs[i] = ttk.Frame(notebk, width = 400, height = 400, relief = SUNKEN)
            title = files[i].split("_")
            if title[0] == '':
                title = ("any make, any model").upper()
            elif title[1] == '':
                title = (title[0] + ", any model").upper()
            elif title[0] == '' and title[1] == '':
                title = ("any make, " + title[1].replace("-", " ")).upper()
            else:
                title = (title[0] + " " + title[1].replace("-", " ")).upper()
            notebk.add(tabs[i], text = title)
            
            # get content in csv file
            os.chdir("./csv files")
            with open(files[i], mode="r", newline='') as csvFile:
                csvReader = csv.reader(csvFile)
                try:
                    data = sorted(csvReader, reverse=True, key = operator.itemgetter(6))
                    data.pop(0)
                except Exception as e:
                    print(e)
                    print("Scores not found")
                    data = list(csvReader)
                csvFile.close()
            os.chdir(maindir)
            
            # nr of ads label
            ads_nrTxt = str(len(data)) + " ads"
            parameters = files[i].split("_")
            
            # price parameters
            parPrice = parameters[2].split('-')
            if parPrice[0] != '' or parPrice[1] != '':
                if parPrice[0] == '':
                    parPrice = " | Price: > " + parPrice[1]
                elif parPrice[1] == '':
                    parPrice = ' | Price: < ' + parPrice[0]
                elif parPrice[0] == parPrice[1]:
                    parPrice = ' | Price: ' + parPrice[0]
                else:
                    parPrice = ' | Price: ' + parPrice[0] + ' - ' + parPrice[1]
                ads_nrTxt = ads_nrTxt + parPrice
            
            # mileage parameters
            parMileage = parameters[4].split('-')
            if parMileage[0] != '' or parMileage[1] != '':
                if parMileage[0] == '':
                    parMileage = " | Mileage: > " + parMileage[1]
                elif parMileage[1] == '':
                    parMileage = ' | Mileage: < ' + parMileage[0]
                elif parMileage[0] == parMileage[1]:
                    parMileage = ' | Mileage: ' + parMileage[0]
                else:
                    parMileage = ' | Mileage: ' + parMileage[0] + ' - ' + parMileage[1]
                ads_nrTxt = ads_nrTxt + parMileage
            
            # registration parameters
            parReg = parameters[3].split('-')
            if parReg[0] != '' or parReg[1] != '':
                if parReg[0] == '':
                    parReg = " | Reg: > " + parReg[1]
                elif parReg[1] == '':
                    parReg = ' | Reg: < ' + parReg[0]
                elif parReg[0] == parReg[1]:
                    parReg = ' | Reg: ' + parReg[0]
                else:
                    parReg = ' | Reg: ' + parReg[0] + ' - ' + parReg[1]
                ads_nrTxt = ads_nrTxt + parReg
            
            
            ads_nr = Label(tabs[i], text = ads_nrTxt)
            ads_nr.grid(row=10,column=0, padx=5)
            ads_nr['font'] = labelf
            
            # generate treeview
            adsTrees[i] = ttk.Treeview(tabs[i], height=20)
            adsTrees[i]["columns"]=("Registration","Price","Mileage","Power","Score")
            adsTrees[i].column("#0", width=280, minwidth=140,anchor=W)
            adsTrees[i].column("#2", width=60, minwidth=60,anchor=CENTER)
            adsTrees[i].column("#1", width=40, minwidth=40,anchor=CENTER)
            adsTrees[i].column("#3", width=70, minwidth=70,anchor=CENTER)
            adsTrees[i].column("#4", width=45, minwidth=45,anchor=CENTER)
            adsTrees[i].column("#5", width=45, minwidth=45,anchor=CENTER)
            
            adsTrees[i].heading("#0",text="Title", anchor=CENTER)
            adsTrees[i].heading("#1", text="Year", anchor=CENTER)
            adsTrees[i].heading("#2", text="Price", anchor=CENTER)
            adsTrees[i].heading("#3", text="Mileage", anchor=CENTER)
            adsTrees[i].heading("#4", text="Power", anchor=CENTER)
            adsTrees[i].heading("#5", text="Score", anchor=CENTER)
            
            adsTrees[i].grid(row=20,column=0, columnspan=2,rowspan=10)
            # insert data
            for d in data:
                adsTrees[i].insert('', 'end', text=d[1], values=(d[2],d[3],d[4],d[5],d[6],d[0]))
                
    # =========== CHANGES TREE

        # changes title
        os.chdir("./csv files")
        try:
            with open("changesTimestamp.txt", mode="r") as timestampFile:
                timetxt = timestampFile.readlines() 
                if timetxt[0] == '':
                    timetxt = ['']
                timestampFile.close()
        except:
            with open("changesTimestamp.txt", mode="w") as timestampFile:
                timetxt = ['']
                timestampFile.close()
        os.chdir(maindir)
        chl = Label(mainc, text="Changes " + timetxt[0])
        chl['font'] = titlef
        chl.grid(row=32,column=10,padx=5)
        
        # generate treeview
        changesTree = ttk.Treeview(mainc, height=5)
        changesTree["columns"]=("Title","Registration","Price","Mileage","Power")
        changesTree.column("#0", width=80, minwidth=70,anchor=W)
        changesTree.column("#1", width=210, minwidth=60,anchor=CENTER)
        changesTree.column("#2", width=65, minwidth=40,anchor=CENTER)
        changesTree.column("#3", width=55, minwidth=70,anchor=CENTER)
        changesTree.column("#4", width=70, minwidth=45,anchor=CENTER)
        changesTree.column("#5", width=60, minwidth=45,anchor=CENTER)
        
        changesTree.heading("#0", text="Value", anchor=CENTER)
        changesTree.heading("#1",text="Title", anchor=CENTER)
        changesTree.heading("#2", text="Year", anchor=CENTER)
        changesTree.heading("#3", text="Price", anchor=CENTER)
        changesTree.heading("#4", text="Mileage", anchor=CENTER)
        changesTree.heading("#5", text="Power", anchor=CENTER)
        
        changesTree.grid(row=40,column=10,padx=5)
        
        os.chdir("./csv files")
        try:
            with open("changesTemp.csv", mode="r", newline='') as changesFile:
                changesReader = csv.reader(changesFile)
                changes = list(changesReader)
                changesFile.close()
        except:
            with open("changesTemp.csv", mode="w", newline='') as changesFile:
                print("initiating temporary changes file")
                changes = []
                changesFile.close()
        os.chdir(maindir)
        for i in range(len(changes)):
            changesTree.insert('', 'end', text=changes[i][0], values=(changes[i][2], changes[i][3], changes[i][4], changes[i][5], changes[i][6], changes[i][1]))


class FavoritesPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        nr = 3
        navMenu(self, master, nr)  
        
    # ========== MAIN CONTENT
        def chck():
            chckerThread = th.Thread(target=favoritesChecker, args=(maindir,))
            chckerThread.start()
            threads = []
            threads.append(chckerThread)
            threadsThread = th.Thread(target=chckThread, args = (threads[0],))
            threadsThread.start()
            
        def chckThread(thread):
            thread.join()
            printTable()
            master.switch_frame(FavoritesPage)
            
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
                if int(changes[i][0]) > 0:
                    pr = "+" + str(changes[i][0])
                else:
                    pr = changes[i][0]
                changesTree.insert('', 'end', text=changes[i][0], values=(changes[i][2], changes[i][3], changes[i][4], changes[i][5], changes[i][6], changes[i][1]))
            os.chdir(maindir)
    
        
        # styles
        titlef = tkfont.Font(family='Montserrat' ,size=16, weight = "bold")
        labelf = tkfont.Font(family='Montserrat' ,size=12)
        
        ntbkStyle = ttk.Style()
        ntbkStyle.configure('TNotebook.Tab', font=('Montserrat','11','bold'), padding=(10, 3, 10, 2))

        # main content frame
        mainc = ttk.Frame(self)
        mainc.config(width = 600, height = 700)
        mainc.grid(row = 20, column = 0,sticky="new",pady=5)
        
        #verify icon         
        favVerifyIcon = PhotoImage(file="./resources/icons/verify.png")
        favVerifyIcon = favVerifyIcon.subsample(6,6) 
        favVerifyButton = Button(mainc, image = favVerifyIcon,compound = LEFT, bg='#fff', command=chck)
        favVerifyButton.image = favVerifyIcon
        favVerifyButton.grid(row=10, column=20,padx=10)
        favVerifyButton.config(width=50, height=50)
        
        # browse button
        def browseSelected():                
            selectedItem = tuple(favoritesTree.selection())
            for item in selectedItem:
                item = favoritesTree.item(item)
                try:
                    link = item['values'][4]
                    webbrowser.open(link)
                except:
                    None
            master.switch_frame(FavoritesPage)
                
        favBrowseIcon = PhotoImage(file="./resources/icons/browse.png")
        favBrowseIcon = favBrowseIcon.subsample(6,6) 
        favBrowseButton = Button(mainc, image = favBrowseIcon,compound = LEFT, bg='#fff',command = browseSelected)
        favBrowseButton.image = favBrowseIcon
        favBrowseButton.grid(row=11, column=20,padx=10)
        favBrowseButton.config(width=50, height=50)
        
        # remove listing button
        def removeListing():
            selectedItem = list(favoritesTree.selection())
            
            links_to_remove = []
            for item in selectedItem:
                item = favoritesTree.item(item)
                links_to_remove.append(str(item['values'][4]))
            
            os.chdir("./csv files")
            with open("favorites.csv", mode="r", newline='') as favsFile:
                csvReader = csv.reader(favsFile)
                data = list(csvReader)
                favsFile.close()
            os.chdir(maindir)
    
            data_new = [] 
            for i in range(len(data)):
                if not str(data[i][0]) in links_to_remove:
                    data_new.append(data[i])
                        
            os.chdir("./csv files")      
            with open("favorites.csv", mode='w', newline='') as favsFile:
                csvWriter = csv.writer(favsFile)
                for d in data_new:
                    csvWriter.writerow([d[0], d[1], d[2], d[3], d[4], d[5]])
                favsFile.close()
            os.chdir(maindir)
            master.switch_frame(FavoritesPage)
        
        favRmIcon = PhotoImage(file="./resources/icons/remove.png")
        favRmIcon = favRmIcon.subsample(6,6) 
        favRmButton = Button(mainc, image = favRmIcon,compound = LEFT, bg='#fff', command = removeListing)
        favRmButton.image = favRmIcon
        favRmButton.grid(row=29, column=20,padx=10)
        favRmButton.config(width=50, height=50)
        
    # =========== FAVORITES TREE
    
        # get content in csv file
        os.chdir("./csv files")
        try:
            with open("favorites.csv", mode="r", newline='') as favsFile:
                csvReader = csv.reader(favsFile)
                data = list(csvReader)
                favsFile.close()
        except:
            with open("favorites.csv", mode="w", newline='') as favsFile:
                print("Favorites file not found, initiating file")
                favsFile.close()
        os.chdir(maindir)
        
        # generate treeview
        favoritesTree = ttk.Treeview(mainc, height=23)
        favoritesTree["columns"]=("Registration","Price","Mileage","Power")
        favoritesTree.column("#0", width=260, minwidth=140,anchor=W)
        favoritesTree.column("#2", width=80, minwidth=60,anchor=CENTER)
        favoritesTree.column("#1", width=60, minwidth=40,anchor=CENTER)
        favoritesTree.column("#3", width=80, minwidth=70,anchor=CENTER)
        favoritesTree.column("#4", width=60, minwidth=45,anchor=CENTER)
        
        favoritesTree.heading("#0",text="Title", anchor=CENTER)
        favoritesTree.heading("#1", text="Year", anchor=CENTER)
        favoritesTree.heading("#2", text="Price", anchor=CENTER)
        favoritesTree.heading("#3", text="Mileage", anchor=CENTER)
        favoritesTree.heading("#4", text="Power", anchor=CENTER)
        
        favoritesTree.grid(row=10,column=10, columnspan=10,rowspan=20, padx=5)
        
        # insert data
        try:
            for d in data:
                favoritesTree.insert('', 'end', text=d[1], values=(d[2],d[3],d[4],d[5],d[0]))     
        except:
            print("Favorites file is empty")  
            
    # =========== CHANGES TREE
    
        # changes title
        os.chdir("./csv files")
        try:
            with open("changesTimestamp.txt", mode="r") as timestampFile:
                timetxt = timestampFile.readlines() 
                if timetxt[0] == '':
                    timetxt = ['']
                timestampFile.close()
        except:
            with open("changesTimestamp.txt", mode="w") as timestampFile:
                timetxt = ['']
                timestampFile.close()
        os.chdir(maindir)
        chl = Label(mainc, text="Changes " + timetxt[0])
        chl['font'] = titlef
        chl.grid(row=32,column=10,padx=5)
        
        # generate treeview
        changesTree = ttk.Treeview(mainc, height=5)
        changesTree["columns"]=("Title","Registration","Price","Mileage","Power")
        changesTree.column("#0", width=80, minwidth=70,anchor=W)
        changesTree.column("#1", width=210, minwidth=60,anchor=CENTER)
        changesTree.column("#2", width=65, minwidth=40,anchor=CENTER)
        changesTree.column("#3", width=55, minwidth=70,anchor=CENTER)
        changesTree.column("#4", width=70, minwidth=45,anchor=CENTER)
        changesTree.column("#5", width=60, minwidth=45,anchor=CENTER)
        
        changesTree.heading("#0", text="Value", anchor=CENTER)
        changesTree.heading("#1",text="Title", anchor=CENTER)
        changesTree.heading("#2", text="Year", anchor=CENTER)
        changesTree.heading("#3", text="Price", anchor=CENTER)
        changesTree.heading("#4", text="Mileage", anchor=CENTER)
        changesTree.heading("#5", text="Power", anchor=CENTER)
        
        changesTree.grid(row=40,column=10,padx=5)
        
        os.chdir("./csv files")
        try:
            with open("favchangesTemp.csv", mode="r", newline='') as changesFile:
                changesReader = csv.reader(changesFile)
                changes = list(changesReader)
                changesFile.close()
        except:
            with open("favchangesTemp.csv", mode="w", newline='') as changesFile:
                print("initiating temporary changes file")
                changes = []
                changesFile.close()
                
        os.chdir(maindir)
        for i in range(len(changes)):
            changesTree.insert('', 'end', text=changes[i][0], values=(changes[i][2], changes[i][3], changes[i][4], changes[i][5], changes[i][6], changes[i][1]))

            
         
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