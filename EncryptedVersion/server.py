import cv2
import numpy as np
import socket
import pickle
import struct
import threading
import lzma
import time
from cryptography.fernet import Fernet
global _win32
try:
    import win32api
    _win32 = True
except:
    _win32 = False

# Change the width and height of window
# Small window
SWIDTH = 960
SHEIGHT = 540

# Large window
#SWIDTH = 1920
#SHEIGHT = 1080

class RemoteDesktop:
    def __init__(self, host, port, key):
        self.ip = host
        self.port = port
        self.active = False
        self.reset = False
        self.__block = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_socket()
        self.fernet = Fernet(key)
        

    def bind_socket(self):
        self.socket.bind((self.ip, self.port))

    def start_server(self):
        if self.active:
            print("server already running")
        else:
            self.active = True
            server_thread = threading.Thread(target=self.__server_listening)
            server_thread.start()
    def __server_listening(self):
        self.socket.listen()
        while self.active:
            self.__block.acquire()
            connection, address = self.socket.accept()
            self.__block.release()
            self.__client_connection(connection, address,)
            print("Connection started!")

    
    def stop_server(self):
        if self.active:
            self.active = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.ip, self.port))
            closing_connection.close()
            self.__block.acquire()
            self.socket.close()
            self.__block.release()
        else:
            print("Server not running!")
            
            
            
    def send_msg(self, msg, conn):
        conn.send(msg)
        

    def showcords(self, event,x,y,flags,param) -> None:
        conn, userinput = param
        if userinput == 1:
            if _win32:
                win32api.SetCursor(win32api.LoadCursor(0, 32649))
            x = str(x)
            y = str(y)
            event = str(event)
            flags = str(flags)
            data = ["mouse", x, y, event, flags]
            keys = ":".join(data)
            self.send_msg(keys.encode('utf-8'), conn)

    def sortframe(self, frame_data):
        data = lzma.decompress(frame_data)
        decrypt = self.fernet.decrypt(data)
        frame = pickle.loads(decrypt, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        return frame

    def fps(self, fps):
        if int(fps) < 10:
            return (fps, (0, 0, 255))
        elif int(fps) < 30:
            return (fps, (2, 186, 252))
        else:
            return (fps, (0, 255, 0))
    def __client_connection(self, connection, address):
        global WIDTH, HEIGHT

        try:
            display = connection.recv(1028).decode().split(":")
            WIDTH, HEIGHT = int(display[0]), int(display[1])
        except:
            pass
        payload_size = struct.calcsize('>L')
        data = b""
        loop_time = time.time()
        send = 0
        cv2.namedWindow(str(address), cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(str(address), (SWIDTH, SHEIGHT))
        cv2.createTrackbar("Quality", str(address), 15, 100, lambda x: x)
        cv2.createTrackbar("Control", str(address), 0, 1, lambda x: x)
        while self.active:
            break_loop = False
            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':
                    connection.close()
                    break_loop = True
                    break
                data += received

            if break_loop:
                break
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += connection.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = self.sortframe(frame_data)
            userinput = cv2.getTrackbarPos("Control", str(address))
            if userinput == 0:
                cv2.putText(frame, "Toggle Control to 1 to control client", (200,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0,0), 2)
            cv2.setMouseCallback(str(address), self.showcords, param=(connection, userinput))
            fps = self.fps(str(int(1 / (time.time()-loop_time))))
            cv2.putText(frame, fps[0], (5, 30), cv2.FONT_HERSHEY_COMPLEX, 1, fps[1], 2)
            cv2.imshow(str(address), frame)
            k = cv2.waitKey(1)
            if k != -1 and userinput == 1:
                keyboard = "keyboard:" + str(k)
                self.send_msg(keyboard.encode('utf-8'), connection)
            quality = cv2.getTrackbarPos("Quality", str(address))
            quality = "config:" + str(quality) + ":" + str(userinput)
            if send == 50:
                self.send_msg(str(quality).encode('utf-8'), connection)
                send = 0
            loop_time = time.time()
            send += 1
if __name__ == '__main__':
    server = RemoteDesktop('0.0.0.0', 443, b'3GkUAE69YzG-jYM0vDGfRsKzosra4JaMtzuC-KGXEDk=')
    server.start_server()
