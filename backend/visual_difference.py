import cv2
from skimage.metrics import structural_similarity as ssim

def compute_ssim(p1, p2):
    img1 = cv2.imread(p1, 0)
    img2 = cv2.imread(p2, 0)
    if img1 is None or img2 is None: return 0.0
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    score, _ = ssim(img1, img2, full=True)
    return score * 100