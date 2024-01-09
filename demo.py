from core import *

# get_screen()
img = cv2.imread('/home/airven/.zhuoyi/common/移动数据/存储卡/screen2.png', cv2.IMREAD_COLOR)
image = image_cut(img)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
