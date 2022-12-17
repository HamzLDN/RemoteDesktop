import cv2
from PIL import ImageGrab
import numpy as np
import pyautogui
import socket
import pickle
import struct
import threading
from pynput.mouse import Button, Controller
import base64
import zlib
class RemoteDesktop:
    def __init__(self, host, port):
        self.ip = host
        self.port = port
        self.active = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def _get_frame(self):
        return None
    
    def recv_msg(self):
        msg = self.socket.recv(1028).decode()
        return msg
    
    def __servermouse(self):
        while self.active:
            try:
                data = self.recv_msg().split(":")
                if data[0] == "mouse":
                    mouse = Controller()
                    datatype, xAxis, yAxis, event = data[0], int(data[1]), int(data[2]), int(data[3])
                    print(datatype, xAxis, yAxis, event)
                    if xAxis < 0 and yAxis < 0:
                        pass
                    else:
                        mouse.position = (xAxis,yAxis)
                        if event == 1:
                            mouse.press(Button.left)
                        if event == 4:
                            mouse.release(Button.left)
                        if event == 2:
                            mouse.press(Button.right)
                        if event == 5:
                            mouse.release(Button.right)
                        if event == 7:
                            pyautogui.doubleClick(xAxis,yAxis)
                if data[0] == "keyboard":
                    keys = int(data[1])
                    if keys == 13:
                        pyautogui.press("enter")
                    else:
                        pyautogui.press(chr(keys))
                        print("keyboard", chr(keys))
                else:
                    pass
            except:
                pass
    def __client_streaming(self):
        self.socket.connect((self.ip, self.port))
        while self.active:
            frame = None
            _, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            video = pickle.dumps(frame, 0)
            length = len(video)
            try:
                self.socket.send(struct.pack('>L', length) + video)
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
            client_thread = threading.Thread(target=self.__client_streaming)
            client_thread.start()
            controller = threading.Thread(target=self.__servermouse)
            controller.start()

            
    def stop_stream(self):
        if self.active:
            self.active = False
        else:
            print("Client is not active!")

class Control(RemoteDesktop):
    def __init__(self, host, port, x_res=1024, y_res=576):
        self.xResolution = x_res
        self.yResolution = y_res
        super(Control, self).__init__(host, port)

    def _get_frame(self):
        screen = ImageGrab.grab()
        # screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

if __name__ == '__main__':
    remote = Control(IP ADDRESS, 443)
    remote.connect()
