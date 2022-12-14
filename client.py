from PIL import ImageGrab, Image
import io
import zlib
import socket
import cv2
import numpy as np
from cryptography.fernet import Fernet
import win32api
import win32con
import math

# Monitors resolution
WIDTH = win32api.GetSystemMetrics(0)
HEIGHT = win32api.GetSystemMetrics(1)
# 1920x1080 FOR MY SCREENs

# Software resolution
SWIDTH = 960
SHEIGHT = 540
# 960x540
class remoteDesktop:
	def __init__(self, ip: str = "192.168.1.10", port: int = 443):
		self.ip = ip
		self.port = port
		#self.enc = fernet(key)
		while True:
			try:
				remoteDesktop.showscreen(self,remoteDesktop.imagebytes(self))
			except:
				break


	def connect(self) -> None:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(self.ip, self.port)
	
	def sendall(self, sock) -> None:
		pass
	# Server
	def showcords(self, event, x, y, flags, params) -> int:
		xRatio = WIDTH / SWIDTH
		yRatio = HEIGHT / SHEIGHT
		print(event, math.ceil(x*xRatio), math.ceil(y*yRatio), flags)
		win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_HAND))
		return event, math.ceil(x*xRatio), math.ceil(y*yRatio)

	# Server
	def showscreen(self, img) -> None:
		'''Decompresses and displays on screen'''
		decompress = zlib.decompress(img)
		nparr = np.frombuffer(decompress, np.uint8)
		frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		frame = cv2.resize(frame, (SWIDTH, SHEIGHT))
		cv2.imshow('frame', frame)
		cv2.setMouseCallback("frame", self.showcords)
		cv2.waitKey(1)

	def imagebytes(self) -> bytes:
		'''Grabs screenshot in JPEG and compresses the bytes'''
		buffer = io.BytesIO()
		im = ImageGrab.grab()
		im.save(buffer, format="JPEG")
		value = buffer.getvalue()
		compressed = zlib.compress(value)
		return compressed

if __name__ == '__main__':
	remoteDesktop()
