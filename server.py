import cv2
import numpy as np
import socket
import pickle
import struct
import threading
import math
global _win32
try:
    import win32api
    _win32 = True
except:
    _win32 = False
SWIDTH = 960
SHEIGHT = 540
class StreamingServer:
    def __init__(self, host, port, slots=8):
        self.ip = host
        self.port = port
        self.active = False
        self.reset = False
        self.__slots = slots
        self.__used_slots = 0
        self.__block = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_socket()
        

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
            if self.__used_slots >= self.__slots:
                print("Connection refused! No free slots!")
                connection.close()
                self.__block.release()
                continue
            else:
                self.__used_slots += 1
            self.__block.release()
            thread = threading.Thread(target=self.__client_connection, args=(connection, address,))
            thread.start()
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
        try:
            conn.send(msg)
        except Exception as e:
            pass
        

    def showcords(self, event,x,y,flags,conn) -> None:
        if _win32:
            win32api.SetCursor(win32api.LoadCursor(0, 32649))
        x = str(math.ceil(x*(WIDTH / SWIDTH)))
        y = str(math.ceil(y*(WIDTH / SWIDTH)))
        event = str(event)
        flags = str(flags)
        data = ["mouse", x, y, event, flags]
        keys = ":".join(data)
        self.send_msg(keys.encode('utf-8'), conn)

    def sortframe(self, frame_data):
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.resize(frame, (SWIDTH, SHEIGHT))
            return frame
        
    def __client_connection(self, connection, address):
        global WIDTH, HEIGHT

        try:
            display = connection.recv(1028).decode().split(":")
            WIDTH, HEIGHT = int(display[0]), int(display[1])
        except:
            pass
        payload_size = struct.calcsize('>L')
        data = b""
        while self.active:
            break_loop = False
            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':
                    connection.close()
                    self.__used_slots -= 1
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
            cv2.imshow(str(address), frame)
            cv2.setMouseCallback(str(address), self.showcords, param=connection)
            keyboard = "keyboard:" + str(cv2.waitKey(100) & 0xFF)
            self.send_msg(keyboard.encode('utf-8'), connection)
                
if __name__ == '__main__':
    server = StreamingServer('0.0.0.0', 443)
    server.start_server()
