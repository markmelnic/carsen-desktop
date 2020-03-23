
import os


# existing searches checker
def remover():
    print("\nRemover initiated")
    # open file to read lines
    with open("csvFilesIndex.txt", mode="r") as cFi:
        lines = cFi.readlines()
        cFi.close()

    if len(lines) != 0:
        print("Currently active files:")
        for line in lines:
            print(line.strip("\n"))

        print("\nWhich search would you like to remove?")
        fileName = input("File Name (without .csv extension): ")
        fileName = fileName + ".csv"

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

    else:
        print("No files to remove")