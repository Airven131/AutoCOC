import cv2

img = cv2.imread('center1.png', cv2.IMREAD_GRAYSCALE)
img = img[0:772, 0:1265].copy()

img = cv2.GaussianBlur(img, (11, 11), 10)

# img = cv2.Canny(img, 5, 40)


cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()