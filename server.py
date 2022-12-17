import cv2
import numpy as np
import socket
import pickle
import struct
import threading
import win32api
import win32con
import math
import base64
WIDTH = win32api.GetSystemMetrics(0)
HEIGHT = win32api.GetSystemMetrics(1)
# 1920x1080 FOR MY SCREENs

# Softwares resolution
SWIDTH = 960
SHEIGHT = 540
class StreamingServer:
    def __init__(self, host, port, slots=8, quit_key='q'):
        self.__host = host
        self.__port = port
        self.__slots = slots
        self.__used_slots = 0
        self.__running = False
        self.__block = threading.Lock()
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__init_socket()

    def __init_socket(self):
        """
        Binds the server socket to the given host and port
        """
        self.__server_socket.bind((self.__host, self.__port))

    def start_server(self):
        """
        Starts the server if it is not running already.
        """
        if self.__running:
            print("Server is already running")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__server_listening)
            server_thread.start()

    def __server_listening(self):
        """
        Listens for new connections.
        """
        global connection
        self.__server_socket.listen()
        while self.__running:
            self.__block.acquire()
            connection, address = self.__server_socket.accept()
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
        """
        Stops the server and closes all connections
        """
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
        else:
            print("Server not running!")
            
            
    def restart_server(self):
        if self.__running:
            self.__running = False
            self.stop_server()
            self.start_server()
        else:
            print("Server not running!")
            
    def send_msg(self, msg):
        connection.send(msg)
        
    def showcords(self, event,x,y,flags,params) -> None:
        win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_HAND))
        xRatio = WIDTH / SWIDTH
        yRatio = HEIGHT / SHEIGHT
        x = str(math.ceil(x*xRatio))
        y = str(math.ceil(y*yRatio))
        event = str(event)
        data = [x, y, event]
        keys = ":".join(data)
        self.send_msg(keys.encode('utf-8'))

    def __client_connection(self, connection, address):
        """
        Handles the individual client connections and processes their stream data.
        """
        payload_size = struct.calcsize('>L')
        data = b""

        while self.__running:
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

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.resize(frame, (SWIDTH, SHEIGHT))
            cv2.imshow(str(address), frame)
            cv2.setMouseCallback(str(address), self.showcords)
            cv2.waitKey(1)
            # if cv2.waitKey(1) == ord(self.__quit_key):
            #     connection.close()
            #     self.__used_slots -= 1
            #     break
if __name__ == '__main__':
    server = StreamingServer('0.0.0.0', 443)
    server.start_server()
