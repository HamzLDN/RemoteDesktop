import cv2
from PIL import ImageGrab
import numpy as np
import pyautogui
import socket
import pickle
import struct
import threading


class RemoteDesktop:
    def __init__(self, host, port):
        self.ip = host
        self.port = port
        self._configure()
        self.__running = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def _configure(self):
        """
        Basic configuration function.
        """
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def _get_frame(self):
        return None

    def _cleanup(self):
        """
        Cleans up resources and closes everything.
        """
        cv2.destroyAllWindows()

    
    def recv_msg(self):
        msg = self.socket.recv(16).decode()
        return msg
    
    def _servermouse(self):
        while True:
            try:
                data = self.recv_msg().split(" ")
                event, xAxis, yAxis = data[0], data[1], data[2]
                print(event, xAxis, yAxis)
                if event == "1":
                    pyautogui.mouseDown(button='left', x=int(xAxis), y=int(yAxis))
                if event == "4":
                    pyautogui.mouseUp(button='left', x=int(xAxis), y=int(yAxis))
            except:
                pass
    def __client_streaming(self):
        """
        Main method for streaming the client data.
        """
        self.socket.connect((self.ip, self.port))
        while self.__running:
            frame = self._get_frame()
            _, frame = cv2.imencode('.jpg', frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)
            try:
                self.socket.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                self.__running = False
            except ConnectionAbortedError:
                self.__running = False
            except BrokenPipeError:
                self.__running = False

        self._cleanup()

    def start_stream(self):
        if self.__running:
            print("Client is already streaming!")
        else:
            self.__running = True
            client_thread = threading.Thread(target=self.__client_streaming)
            client_thread.start()
            mouse = threading.Thread(target=self._servermouse())
            mouse.start()
            


    def stop_stream(self):
        """
        Stops client stream if running
        """
        if self.__running:
            self.__running = False
        else:
            print("Client not streaming!")

class Control(RemoteDesktop):
    def __init__(self, host, port, x_res=1024, y_res=576):
        self.xResolution = x_res
        self.yResolution = y_res
        super(Control, self).__init__(host, port)

    def _get_frame(self):
        screen = ImageGrab.grab()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
if __name__ == '__main__':
    remote = Control('localhost', 443)
    remote.start_stream()
