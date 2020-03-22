
import os


# existing searches checker
def remover():
    print("\nRemover initiated")
    print("\nWhich search would you like to remove?")
    fileName = input("File Name (without .csv extension): ")
    fileName = fileName + ".csv"

    # open file to read lines
    with open("csvFilesIndex.txt", mode="r") as cFi:
        lines = cFi.readlines()
        cFi.close()

    # rewrite file without removed filename
    with open("csvFilesIndex.txt", "w") as cFi:
        for line in lines:
            if line.strip("\n") != fileName:
                cFi.write(line)
    try:
        os.remove(fileName)
        print("File removed successfully")
    except:
        print("File inexistent")