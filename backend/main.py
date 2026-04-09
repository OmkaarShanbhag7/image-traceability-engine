from fastapi import FastAPI, UploadFile, File
import shutil
import os
from database import init_db, insert_image, get_all_images
from hashing import compute_phash, phash_similarity
from visual_difference import compute_ssim
from tamper_detection import detect_tampering
from engagement import simulate_engagement
from reverse_search_online import search_online
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_hash = compute_phash(file_path)

    images = get_all_images()

    results = []

    for filename, phash, upload_time in images:
        existing_path = os.path.join(UPLOAD_FOLDER, filename)

        phash_score = phash_similarity(new_hash, phash)
        ssim_score = compute_ssim(file_path, existing_path)

        final_score = 0.7 * phash_score + 0.3 * ssim_score

        results.append({
            "filename": filename,
            "score": final_score,
            "upload_time": upload_time
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    top_matches = results[:3]

    seen_before = len([r for r in results if r["score"] > 70])

    confidence = top_matches[0]["score"] if top_matches else 0
    authenticity = 100 - confidence

    if confidence > 80:
        classification = "Reused"
    elif confidence > 50:
        classification = "Suspicious"
    else:
        classification = "Authentic"

    tamper = detect_tampering(file_path)
    engagement = simulate_engagement(confidence)

    online_results = search_online(file_path)

    insert_image(file.filename, new_hash)

    return {
        "confidence": confidence,
        "authenticity": authenticity,
        "classification": classification,
        "seen_before_count": seen_before,
        "top_matches": top_matches,
        "tamper_status": tamper,
        "engagement": engagement,
        "online_matches": online_results
    }