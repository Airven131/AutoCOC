import cv2
import numpy as np
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port = 5037)
client.remote_connect(host="127.0.0.1", port=5555)
device = client.device("127.0.0.1:5555")

sc = device.screencap()
sc_ts = np.frombuffer(sc, np.uint8)
image = cv2.imdecode(sc_ts, cv2.IMREAD_COLOR)
icon = cv2.imread(".\\icon\\attack.png")

print(image.shape, icon.shape)

with open("temp.png", "wb") as f:
    f.write(sc)

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(image_gray, icon_gray, cv2.TM_CCOEFF_NORMED)

_, _, min_loc, max_loc = cv2.minMaxLoc(result)
print(max_loc)