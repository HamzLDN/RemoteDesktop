import cv2
import numpy as np
import socket
import pickle
import struct
import threading
import lzma
import time
import os
import json
global _win32
try:
    import win32api
    _win32 = True
except:
    _win32 = False


SWIDTH = 960
SHEIGHT = 540


class RemoteDesktop:
    def __init__(self, host, port):
        self.ip = host
        self.port = port
        self.active = False
        self.reset = False
        self.revshell = True
        self.__block = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.userinput = 0
        self.monitor = 0
        self.width = 0
        self.height = 0
        self.cwd = "> "
        self.display_data = {}
        self.position = 0    

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
            t = threading.Thread(target=self.__client_connection, args=(connection, address,))
            t.start()
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
            
            
            
    def send(self, msg, conn):
        conn.send(msg)
        
        
    def is_between(self, num, range1, range2):
        if range1 > range2:
            range1, range2 = range2, range1
        return range1 <= num <= range2

    def get_pos(self) -> int:
        for i in range(self.monitor - 1):
            self.position += self.display_data[i]['resolution'][0]
        return self.position
    

    def showcords(self, event,x,y,flags,param) -> None:
        conn = param
        if self.is_between(x, self.width-30, self.width-80) and self.is_between(y, 0, 50) and event == 4 and self.userinput==0:
            self.userinput=1
        elif self.is_between(x, self.width-30, self.width-80) and self.is_between(y, 0, 50) and event == 4 and self.userinput==1:
            self.userinput=0

        if self.userinput == 1:
            if _win32:
                win32api.SetCursor(win32api.LoadCursor(0, 32649))
            x = str(x + self.get_pos())
            y = str(y + int(self.display_data[self.monitor - 1]['position'][1]))
            #print(x + self.get_pos() + int(self.display_data[self.monitor - 1]['position'][0]))
            event = str(event)
            flags = str(flags)
            data = ["mouse", x, y, event, flags]
            keys = ":".join(data)
            self.send(keys.encode('utf-8'), conn)
            self.position = 0

    def sortframe(self, frame_data):
        data = lzma.decompress(frame_data)
        frame = pickle.loads(data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height))
        return frame


    
    def fps(self, fps):
        if int(fps) < 10:
            return (fps, (0, 0, 255))
        elif int(fps) < 30:
            return (fps, (2, 186, 252))
        else:
            return (fps, (0, 255, 0))

        

    def shell(self, connection):
        while True:
            if self.revshell:
                try:
                    shell = input(self.cwd)
                    if shell == "cls" or shell == "clear":
                        os.system("cls")
                    elif shell == "":
                        continue
                    else:
                        shell = "shell:" + shell
                        self.send(shell.encode('utf-8'), connection)
                        self.revshell = False
                except EOFError:
                    print()
                    continue
            else:
                pass
    '''Sorry for the messy function'''
    def __client_connection(self, connection, address):
        shell_thread = threading.Thread(target=self.shell, args=(connection,))
        shell_thread.start()
        try:
            display = connection.recv(1028).decode()
            self.display_data = json.loads(display)
            self.width, self.height = int(self.display_data[0]['size'][0]), int(self.display_data[0]['size'][1])
            self.monitor = int(self.display_data[0]['len_monitors'])
        except:
            pass
        payload_size = struct.calcsize('>L')
        data = b""
        loop_time = time.time()
        send = 0
        cv2.namedWindow(str(address), cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(str(address), (SWIDTH, SHEIGHT))
        cv2.createTrackbar("Quality", str(address), 15, 100, lambda x: x)
        cv2.createTrackbar("Monitor", str(address), 0, self.monitor, lambda y: y)
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
            if frame_data[0:7].decode() == "video->":
                frame = self.sortframe(frame_data[7:])
                cv2.rectangle(frame, (self.width-30, 0), (self.width-80, 50), (136, 8, 8), 4)
                if self.userinput == 0:
                    cv2.putText(frame, "Click blue box to control", (200,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0,0), 2)
                cv2.setMouseCallback(str(address), self.showcords, param=(connection))
                cv2.imshow(str(address), frame)
                k = cv2.waitKey(1)
                quality = cv2.getTrackbarPos("Quality", str(address))
                self.monitor = cv2.getTrackbarPos("Monitor", str(address)) + 1
                quality = "config:" + str(quality) + ":" + str(self.userinput) + ":" + str(self.monitor)
                if k != -1 and self.userinput == 1:
                    keyboard = "keyboard:" + str(k)
                    self.send(keyboard.encode('utf-8'), connection)
                if send >= 5:
                    self.send(str(quality).encode('utf-8'), connection)
                    send = 0
            else:
                self.cwd = frame_data.decode().strip().split(">", 1)[0] + "> "
                print(frame_data.decode().split(">", 1)[1])
                self.revshell = True
            send +=1

if __name__ == '__main__':
    server = RemoteDesktop('0.0.0.0', 443)
    server.start_server()
    print("Server listening...\n")
