from PIL import ImageGrab
import io
import zlib
import socket
import win32api
import time

# Monitors resolution
WIDTH = win32api.GetSystemMetrics(0)
HEIGHT = win32api.GetSystemMetrics(1)

# Software resolution
SWIDTH = 960
SHEIGHT = 540
class remoteDesktop:
	def __init__(self, ip: str = "192.168.1.10", port: int = 443):
		self.ip = ip
		self.port = port
		self.socket = None
		# self.enc = fernet(key)

	def startsession(self) -> None:
		print("started!")
		while True:
			try:
				remoteDesktop.sendall(self)
			except:
				break
	def connect(self) -> None:
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.ip, self.port))
		self.socket.recv(1028)
		self.startsession()
		
	def sendall(self) -> None:
		self.socket.send(self.imagebytes())


	def imagebytes(self) -> bytes:
		''' Grabs screenshot in JPEG and compresses the bytes '''
		buffer = io.BytesIO()
		im = ImageGrab.grab()
		im.save(buffer, format="JPEG")
		value = buffer.getvalue()
		# compressed = zlib.compress(value)
		# if self.socket.recv(4) != "":
		# 	print(self.socket.recv(4))
		return value


def main(limit: int = 5) -> None:
	desktop = remoteDesktop()
	while True:
		try:
			desktop.connect()
		except Exception:
			time.sleep(limit)
			break
if __name__ == '__main__':
	while True:
		main()
