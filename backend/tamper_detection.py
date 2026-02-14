import cv2
import numpy as np

def detect_tampering(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    variance = np.var(edges)

    if variance > 1000:
        return "High Manipulation Probability"
    elif variance > 500:
        return "Moderate Manipulation"
    else:
        return "Low Manipulation"
