import cv2
from skimage.metrics import structural_similarity as ssim

def compute_ssim(img1_path, img2_path):
    try:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1 is None or img2 is None:
            return 0

        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        score, _ = ssim(gray1, gray2, full=True)

        return score * 100

    except:
        return 0