import cv2
import numpy as np

# 读取图像
image = cv2.imread('image.png')
image = image[0:880, 0:1920]

# 目标RGB颜色对应的BGR值 (164,71,52) → (52,71,164)
target_bgr = (52, 71, 164)
delta = 20  # 调整阈值敏感度（值越小，颜色匹配越严格）

# 计算阈值上下限
lower = np.array([
    max(0, target_bgr[0] - delta),
    max(0, target_bgr[1] - delta),
    max(0, target_bgr[2] - delta)
], dtype=np.uint8)

upper = np.array([
    min(255, target_bgr[0] + delta),
    min(255, target_bgr[1] + delta),
    min(255, target_bgr[2] + delta)
], dtype=np.uint8)

# 生成颜色掩膜
mask = cv2.inRange(image, lower, upper)

# 创建全黑背景（与输入图像尺寸相同）
black_bg = np.zeros_like(image)

# 将目标颜色区域从原图复制到黑色背景上
result = cv2.bitwise_and(image, image, mask=mask)  # 提取目标区域
result += cv2.bitwise_and(black_bg, black_bg, mask=cv2.bitwise_not(mask))  # 合并黑色背景

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 设置最小有效面积（过滤噪声）
min_contour_area = 300  
for cnt in contours:
    # 过滤小面积轮廓
    if cv2.contourArea(cnt) < min_contour_area:
        continue
    
    # 获取最小旋转矩形
    rect = cv2.minAreaRect(cnt)
    
    # 获取矩形顶点坐标
    box = cv2.boxPoints(rect)
    box = box.astype(int)  # 坐标转为整数
    
    # 绘制四边形边框（绿色，线宽2像素）
    cv2.drawContours(result, [box], 0, (0, 255, 0), 2)

# 显示结果
cv2.imshow('Black Background', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
