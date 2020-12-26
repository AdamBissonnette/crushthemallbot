# Crush Them All Bot

## Requirements

Python 3+

* pip install autopy
* pip install pillow
* pip install pynput
* pip install louie
* https://github.com/tesseract-ocr/tesseract
* pip install pytesseract
* pip install tesseract

## Setup

Nox window needs to be in the top lefthand corner of the screen - check the screen.png file for reference on exact size. Adjust the assets as needed (screenshot + overwrite the files in paint if needed) - probably want to change your special abilities and preferred guild medal.

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
* smart logout (if you login via your phone the app will logout for 15 minutes then start again)
* powershell script to resize and position the Nox window (run in powershell using `. ./Position-Nox.ps1`)

## Planned features

* mail checking / collection
* installation script so it's not a pain to setup
* scroll up / down (required for leveling shop without upgrade all)
* upgrade all heroes / shops manually
* overhaul the entire system to use a json+assets config (maybe remote?) instead of code + hotkey to refresh config so the bot can be edited while running AND be used for other games
* guild boss battles
* guild wars? arena? blitz? (these are the fun parts so maybe don't want to automate)
* Explore win32gui for further virtual automation (hwnd = win32gui.FindWindow(None, 'NoxPlayer'), win32gui.PostMessage(hwnd, ))