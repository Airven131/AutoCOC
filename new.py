import cv2
import os
from ppadb.client import Client as AdbClient

client = AdbClient(host = "127.0.0.1", port = 5037)
device = client.device("emulator-5554")
result = device.screencap()
print(type(result))
print(result)
icon = cv2.imread('icon\\attack.png', cv2.IMREAD_GRAYSCALE)
print(type(icon))