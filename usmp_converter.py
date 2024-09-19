import os
import time
import subprocess
import pyautogui
import win32gui
import win32con

def usmp_converter():
    subprocess.Popen('"C:\\Program Files (x86)\\Unitronics\\UniStream Data Converters Suite\\Unitronics Data Sampler To Excel Converter.exe"')
    time.sleep(1)
    handle = win32gui.FindWindow(None, "Unitronics Data Sampler To Excel Converter")
    win32gui.SetWindowPos(handle, win32con.HWND_TOP, 0, 0, 0, 0, 0)
    win32gui.SetForegroundWindow(handle)
    steps = [(710, 127), (764, 540), (377, 217), (725, 18)]
    for step in steps:
        pyautogui.click(step)
        # print(pyautogui.position())
        time.sleep(3)

if __name__ == "__main__":
    usmp_converter()