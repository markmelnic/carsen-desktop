
from bs4_module import getCarPriceChecker

import csv


# existing searches checker
def checker():
    print("\n\n\n/====================================\\")
    print("Checker initiated")
    # check for files to be checked
    with open("csvFilesIndex.txt", mode="r") as cFi:
        files = cFi.readlines()
        cFi.close()
    print(len(files), "files found")
    if len(files) == 0:
        print("Nothing to check")
        print("\====================================/\n\n")
        return
    else:
        changes = []
        # start processing every file
        for file in files:
            file = file.strip("\n")

            # read file contents
            with open(file, mode="r", newline='') as csvFile:
                csvReader = csv.reader(csvFile)
                data = list(csvReader)
                csvFile.close()

            # process every link
            with open(file, mode="w", newline='') as csvFile:
                csvWriter = csv.writer(csvFile)
                links = []
                for i in range(len(data) - 1):
                    links.append(data[i + 1][0])

                # check every link
                i = -1
                for link in links:
                    i += 1
                    if i == 0:
                        print(i + 1, "ad checked")
                    else:
                        print(i + 1, "ads checked")

                    # get new price and compare to existing one
                    newPrice = getCarPriceChecker(link)
                    if(data[i + 1][3]) == newPrice:
                        continue
                    else:
                        changedPrice = int(data[i + 1][3]) - newPrice
                        changedPrice = -changedPrice
                        '''
                        try:
                            data[i + 1].pop(6)
                        except:
                            None
                        '''
                        # skip if price hasn't changed, else append the change
                        if changedPrice == 0:
                            continue
                        else:
                            if changedPrice == data[-1]:
                                continue
                            else:
                                data[i + 1].append(changedPrice)
                                changes.append(file)
                                changes.append(i + 1)
                                changes.append(changedPrice)
                # write data back to file
                csvWriter.writerows(data)
                csvFile.close()
            print(file, " checked\n")

    # print changes
    print("Changes found:")
    for i in range(int(len(changes) / 3)):
        print("In file -", changes[i+(i*2)], "- at line ", changes[i+1+(i*2)], " by ", changes[i+2+(i*2)])

    print("Checker executed successfully")
    print("\====================================/\n\n")