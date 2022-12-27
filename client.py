import cv2
import numpy as np
from pyautogui import doubleClick, press, grab
import socket
import pickle
import struct
import pyautogui
from threading import Thread, Lock
from pynput.mouse import Button, Controller
import win32api
import lzma
WIDTH = win32api.GetSystemMetrics(0)
HEIGHT = win32api.GetSystemMetrics(1)

metrics = [str(WIDTH), str(HEIGHT)]
dislpay = ":".join(metrics).encode('utf-8')
class RemoteDesktop:
    def __init__(self, host, port):
        self.ip = host
        self.port = port
        self.active = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.LeftMouseup = False
        self.RightMouseup = False
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
                    xAxis, yAxis, event, flags = int(data[1]), int(data[2]), int(data[3]), int(data[4])
                    # print(xAxis, yAxis)
                    if xAxis < 0 and yAxis < 0:
                        pass
                    else:
                        mouse.position = (xAxis,yAxis)
                        print(event)
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
                            doubleClick(xAxis,yAxis)
                        elif event == 10:
                            if flags > 0:
                                mouse.scroll(0, -1)
                            else:
                                mouse.scroll(0, 1)
                if data[0] == "keyboard":
                    keys = int(data[1])
                    if keys == 13:
                        press("enter")
                    else:
                        press(chr(keys))
                else:
                    pass
            except:
                pass
    def __client_streaming(self):
        self.socket.connect((self.ip, self.port))
        self.socket.send(dislpay)
        print("Reconnecting!")
        while self.active:
            frame = self._get_frame()
            _, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            video = lzma.compress(pickle.dumps(frame, 0))
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
            client_thread = Thread(target=self.__client_streaming)
            client_thread.start()
            controller = Thread(target=self.__servermouse)
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
        screen = grab()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

if __name__ == '__main__':
    remote = Control('localhost', 443)
    remote.connect()
