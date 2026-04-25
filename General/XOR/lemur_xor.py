import cv2
import numpy as np
from PIL import Image
img = cv2.imread(r"/home/quq/coding/Python/flag_7ae18c704272532658c10b5faad06d74.png", cv2.IMREAD_UNCHANGED)
img2 = cv2.imread(r"/home/quq/coding/Python/lemur_ed66878c338e662d3473f0d98eedbd0d.png", cv2.IMREAD_UNCHANGED)


height, width = img.shape[:2]


img3 = Image.new('RGB', (width, height), color='white')
for y in range(height):
    for x in range(width):
        flag=""
        b, g, r= img[y, x]
        b2,g2,r2=img2[y,x]
        b3=b^b2
        g3=g^g2
        r3=r^r2
        img3.putpixel((x, y), (r3, g3, b3))
img3.save('flag.png')