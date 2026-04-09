from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import traceback

import database, hashing, visual_difference, tamper_detection, engagement

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# FIXED PATHS FOR RENDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

database.init_db()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        current_hash = hashing.compute_phash(path)
        db_images = database.get_all_images()
        
        best_phash = 0.0
        best_ssim = 0.0
        matches = 0

        for fname, db_h in db_images:
            sim = hashing.calculate_similarity(current_hash, db_h)
            if sim > 80:
                matches += 1
                db_path = os.path.join(UPLOAD_DIR, fname)
                if os.path.exists(db_path):
                    s_score = visual_difference.compute_ssim(path, db_path)
                    best_ssim = max(best_ssim, s_score)
            best_phash = max(best_phash, sim)

        final = (0.7 * best_phash) + (0.3 * best_ssim) if best_ssim > 0 else best_phash
        tamper_results = tamper_detection.analyze_tampering(path)
        eng_sim = engagement.simulate_engagement(final)
        database.add_image(file.filename, current_hash)

        return {
            "final_score": final,
            "decision": "Reused" if final > 80 else ("Suspicious" if final > 50 else "Authentic"),
            "similarity": {"phash_similarity": best_phash, "ssim_score": best_ssim},
            "traceability": {"seen_before_count": matches},
            "tamper_analysis": tamper_results,
            "engagement": eng_sim
        }
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"detail": str(e)})

# MOUNT STATIC FOLDER
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")