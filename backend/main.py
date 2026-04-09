from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import traceback

# Import your modules
import database
import hashing
import visual_difference
import tamper_detection
import engagement

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Paths tailored to your folder structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
ROOT_DIR = os.path.join(BASE_DIR, "..") # Looks up to root for index.html

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
        
        database.add_image(file.filename, current_hash)

        return {
            "final_score": final,
            "decision": "Reused" if final > 80 else ("Suspicious" if final > 50 else "Authentic"),
            "similarity": {"phash_similarity": best_phash, "ssim_score": best_ssim},
            "traceability": {"seen_before_count": matches},
            "tamper_analysis": tamper_detection.analyze_tampering(path),
            "engagement": engagement.simulate_engagement(final)
        }
        
    except Exception as e:
        # Prints the full error to your Render Logs
        print(traceback.format_exc()) 
        # Sends the specific error text back to the website
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Mount frontend files from root
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="static")