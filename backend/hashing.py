from PIL import Image
import imagehash

def generate_phash(image_path):
    image = Image.open(image_path)
    return str(imagehash.phash(image))

def compare_hash(hash1, hash2):
    h1 = imagehash.hex_to_hash(hash1)
    h2 = imagehash.hex_to_hash(hash2)
    return 100 - (h1 - h2) * 100 / 64
