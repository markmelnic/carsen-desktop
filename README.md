# Mobile.de Bot
A python bot for scraping and tracking mobile.de. Get all data for a specific car make and model directly into a spreadsheet, where you can analyze it. Run the checker to see whether the price has changed since the first search.

## Some technical aspects
Built in python 3.8. Essential packages used:
 * bs4
 * selenium
 * threading

Not all come standart with python, so if you are using the 1st installation method make sure to have them installed. Or just don't bother and follow installation method number 2.

## Installation
#### First method
1. clone all github files into a folder  
2. Run the program from main.py

#### Second method
1. Get the installer here, version Alpha 0.7.5 
https://www.dropbox.com/s/x3qm4zkv3mb1pd1/Mobile.de%20Bot%20v.Alpha.0.7.5.exe?dl=0
version Alpha 0.8.6 
https://www.dropbox.com/s/mrapcch6apmq3pq/Mobile.de%20Bot%20v.Alpha.0.8.6.exe?dl=0
2. Install the app and run "Mobile.de Bot.exe" 

## Running the program (console, before version Alpha 0.8.4)
In the terminal you will be presented with this little menu

![Imgur](https://i.imgur.com/PzQZO8Rm.png)

#### Search
Start by pressing F1 and introducing a new search. The bot will start execution after all input field have been completed or skipped.
Now that your search has been indexed and executed, find the output file in the "csv files" directory.

Alpha 0.8 update: Now every ad is being assigned a "how good of a deal this is" score. Most accurate with cars of the same or ± 1 registration year. In Excel (presumably) sort all cells by the score tab from highest to lowest, and find the best deals at the top. I have tested this feature mostly with Lexus vehicles with registration years from 2016 to 2020 and it works like a charm.

For now, a car's mileage has the biggest impact on the score, followed shortly by it's price and eventually, registration year. I would take into consideration horsepower and other parameters, but due to inconsistency in how precise sellers describe their cars, there is too much room for crashing the app so this is what we get.

#### Check
To see if there are any changes to indexed searches, press F2. Once the checker has been executed, the changes can be found in the .csv files themselves, or will be presented in the terminal window as following

![Imgur](https://i.imgur.com/ieHLcp8m.png)

If any of the indexed ads have disappeared from the site you will see a "X ads removed" line at the end of the changes list.

#### Remove
Recommended to be used instead of just deleting the corresponding .csv file.
Press F3 to run and insert the number corresponding to the file you'd like to remove. This will also diable checking this file for price updates.

![Imgur](https://i.imgur.com/jEVXJqSm.png)

#### Backup
Pretty self explanatory, backs up all .csv files to a directory with your current timestamp in the backup folder. The checking function does it by default in case something goes wrong, but you still may want to use it from stability concerns.

## Running the program (gui, after version Alpha 0.8.4)
A GUI has been added, so no more need to work with the terminal. I would include a screenshot but since the GUI is constantly changing, well, you get the idea. The functions remain the same as described above, and do the same stuff. Actually, changed my mind, it's ugly but at least it works. Here you go

![Imgur](https://imgur.com/yOauWZI)

## Thank you for taking a look at my work! Throw an eye on my website https://markmelnic.com/ to find some of my other projects, or for no reason really :D Cheers!
