# Crush Them All Bot

## Requirements

Python 3+

* Install external screen reader lib https://github.com/tesseract-ocr/tesseract
    * .exe install here https://github.com/UB-Mannheim/tesseract/wiki
* pip install -r requirements.txt
    * Will install the following
    * pip install autopy
    * pip install pillow
    * pip install pynput
    * pip install louie
    * pip install pytesseract
    * pip install tesseract
	* pip install pywin32
	* pip install pywin32-ctypes
* pip install pypiwin32 (might need this?)

## Setup

Nox window needs to be in the top lefthand corner of the screen - check the screen.png file for reference on exact size. Adjust the assets as needed (screenshot + overwrite the files in paint if needed) - probably want to change your special abilities and preferred guild medal.

## Sizing

- 1920 x 1080 display resolution
- Basic Mode (Direct X) 540x960 mobile phone
- Low quality mode in-game

## Running and Stopping 

* If you've run the program and can't get it to stop try hitting the "End" key on your keyboard - the program is listening to this as a kill signal
* I recommend using VS Code because it's lightweight and simplifies the run process (just click the play button on the main.py screen) and you can easily debug if needed: https://code.visualstudio.com/
* The program is multi-threaded and since I haven't set it up properly part of it will continue running in the background and lock your terminal if you do ctrl+c to exit - to fully exit hit the End key. This was originally implemented because the program took over the mouse and keyboard and made it really difficult to click over to vs code or a command line terminal and hit ctrl+c and stop the program. It's kinda nice so I haven't bothered to fix it.

## Features so far

* Image recognition for assets used to navigate around and use abilities off cooldown
* Watches ads for gold chests and 2x speed
* Levels up all heroes and shops (for vip leves with the upgrade all)
* Does dungeons (last or first dungeon only)
* Helps and requests guild medals (set via reference image asset)
* Does expeditions (autofill only)
* Crash detection / app restart
* Closes popup windows (most of the time)
* Image to text recognition to ascend at a given stage #
* ~~smart logout (if you login via your phone the app will logout for 15 minutes then start again)~~ not working right now
* powershell script to resize and position the Nox window (run in powershell using `. ./Position-Nox.ps1`)
* installation script so it's not a pain to setup via the requirements.txt file
* Explored win32gui for further virtual automation - windows only feature allows the program to spoof mouse clicks into the Nox window. Sadly this doesn't work for keyboard presses yet.

## Planned features

* mail checking / collection (so close to working but it's finnicky)
* scroll up / down (required for leveling shop without upgrade all)
* upgrade all heroes / shops manually
* overhaul the entire system to use a json+assets config (maybe remote?) instead of code + hotkey to refresh config so the bot can be edited while running AND be used for other games
* guild boss battles
* guild wars? arena? blitz? (these are the fun parts so maybe don't want to automate)