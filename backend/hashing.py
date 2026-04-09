from PIL import Image
import imagehash

def compute_phash(image_path):
    try:
        image = Image.open(image_path)
        return str(imagehash.phash(image))
    except:
        return "0" * 16

def hamming_distance(hash1, hash2):
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

def phash_similarity(hash1, hash2):
    distance = hamming_distance(hash1, hash2)
    return 100 - (distance / 64 * 100)