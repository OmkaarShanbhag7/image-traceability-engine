import cv2

def analyze_tampering(path):
    img = cv2.imread(path, 0)
    if img is None: return {"suspicious": False, "edge_variance": 0}
    var = cv2.Laplacian(img, cv2.CV_64F).var()
    return {"edge_variance": float(var), "suspicious": var < 50 or var > 4000}