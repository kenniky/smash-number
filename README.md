# smash-number

This is a command-line python script that will find the set chain from one player to another. It is backed by the smashdata.gg database.

### Requirements

- Command-line usage and `python3` installed
  - Default installed command line tools are **PowerShell** on Windows and **Terminal** on Mac OS. If you don't know how to use them, I would suggest looking it up online.
- smashdata database downloaded and unzipped [(find it here)](https://github.com/smashdata/ThePlayerDatabase)

### Usage

1. Modify the `DATABASE_PATH` variable with the path to the unzipped smashdata sql database
2. Run the script via `python3 number.py`
3. Enter the beginning and ending smashdata id. The easiest way to retrieve this id is to navigate to the player's smashdata.gg page and retrieve the id from the url. For example, in the following url: `https://smashdata.gg/smash/ultimate/player/kenniky?id=160058`, the id is `160058`.  
If the id does not show up in the url, toggle one of the settings in the settings bar and it should show up. Make sure to copy only the part that comes directly after the `?id=` part of the url.
You can also query for the player id directly in the sql database.
4. Decide whether you want to include online sets. Inputting `y` or `Y` will enable online sets, anything else will exclude them. Offline sets are always included.
5. Wait for a while lol. The script will periodically print stuff so that it's clear that it's still running
