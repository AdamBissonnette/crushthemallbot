import win32con
import win32api
import win32ui
import win32gui
import time
from PIL import Image
import ctypes

hwnd = win32gui.FindWindow(None, 'NoxPlayer')
coords = win32api.MAKELONG(120, 270)

def post_button(hwnd, coords, stime=0.1):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, coords)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, coords)
    time.sleep(stime)
    move_mouse(hwnd, coords)

def send_button(hwnd, coords, stime=0.1):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, coords)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, coords)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, coords)
    time.sleep(stime)
    move_mouse(hwnd, coords)

def move_mouse(hwnd, coords):
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, coords)

def get_screenshot(hwnd, maxheight=-1):
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bot - top
    if maxheight > 0:
        h = maxheight

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print (result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")

get_screenshot(hwnd)