# Mobile.de Bot
A terminal based python bot for scraping and tracking mobile.de. Get all data for a specific car make and model directly into a spreadsheet, where you can analyze it. Run the checker to see whether the price has changed since the first search.

## Installation
### 1st method
1. clone all github files to a folder
2. inside that folder, add more folders to follow the structure:
Main Folder
 |
 +-- backup
 |    
 +-- csv files
    |  
    +-- search parameters
3. Run the program from main.py

### 2nd method
1. Get the installer here https://www.dropbox.com/s/x3qm4zkv3mb1pd1/Mobile.de%20Bot%20v.Alpha.0.7.5.exe?dl=0
2. Install the app and run "Mobile.de Bot.exe" 

## Running the program (and it's features)
In the console you will be presented with this menu
![Imgur](https://i.imgur.com/PzQZO8Rl.png)

### Searching
Start by pressing F1 and introducing a new search. The bot will start execution after all input field have been completed or skipped.
Now that searching is done, find the outpit file in the "csv files" directory.

### Check
To check whether there are any changes to the se3arches indexed previously, press F2. Once the checker has been executed, the searches can be found in the .csv files themselves, or will be presented as following in the terminal window
![Imgur](https://i.imgur.com/ieHLcp8m.png)
If any of the ads have disappeared from the site you will see a "X ads removed" line at the end of the changes list.

### Remove
Recommended to be used instead of just deleting the corresponding .csv file.
Press F3 to run and input the number corresponding to the file you'd like to remove. This will also diable checking this file for price updates.
![Imgur](https://i.imgur.com/jEVXJqSm.png)

### Backup
Pretty self explanatory, backs up all .csv files to a directory with current timestamp in the backup folder. The checking function does it by default in case something goes wrong, but you still may want to use it for stability concerns.

## Thanks you for taking a look at my work! Throw an eye on my website https://markmelnic.com/ to find some of my other projects, or for no reason really :D. Cheers!
