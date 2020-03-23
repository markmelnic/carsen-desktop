
import os


# existing searches checker
def remover():
    print("\n\n\n/====================================\\")
    print("Remover initiated")
    cwd = os.getcwd()
    os.chdir('./csv files')

    # open file to read lines
    with open("csvFilesIndex.txt", mode="r") as cFi:
        lines = cFi.readlines()
        cFi.close()

    if len(lines) != 0:
        print("Currently active files:")
        i = 1
        for line in lines:
            print(str(i) + ".", line.strip("\n"))
            i += 1

        print("\nWhich search would you like to remove?")
        i = input("File number as appears in the list above: ")
        try:
            i = int(i) - 1
            fileName = lines[i]

            # rewrite file without removed filename
            with open("csvFilesIndex.txt", "w") as cFi:
                for line in lines:
                    if line != fileName:
                        cFi.write(line)
                    else:
                        fileName = line.strip("\n")

            try:
                print(fileName)
                os.remove(fileName)
                print("File removed successfully")
            except:
                print("File inexistent")
        except:
            print("Execution canceled")

    else:
        print("No files to remove")

    os.chdir(cwd)
    print("\====================================/\n\n")