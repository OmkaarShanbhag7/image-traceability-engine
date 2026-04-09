import cv2
import numpy as np

def detect_tampering(image_path):
    img = cv2.imread(image_path, 0)
    edges = cv2.Canny(img, 100, 200)
    variance = np.var(edges)

    if variance > 1000:
        return "High"
    elif variance > 500:
        return "Medium"
    else:
        return "Low"