from PIL import Image
import imagehash

def compute_phash(path):
    return str(imagehash.phash(Image.open(path)))

def calculate_similarity(h1, h2):
    diff = imagehash.hex_to_hash(h1) - imagehash.hex_to_hash(h2)
    return max(0, 100 - (diff * 100 / 64.0))