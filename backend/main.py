from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import traceback

# Import your custom modules
import database
import hashing
import visual_difference
import tamper_detection
import engagement

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# --- UPDATED PATH LOGIC FOR RENDER ---
# BASE_DIR is the directory where main.py lives (the backend folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
# ROOT_DIR looks one folder up to find index.html, style.css, script.js
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Database on startup
database.init_db()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # 1. Save the uploaded file locally
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Generate Hash
        current_hash = hashing.compute_phash(path)
        
        # 3. Compare against Database
        db_images = database.get_all_images()
        best_phash = 0.0
        best_ssim = 0.0
        matches = 0

        for fname, db_h in db_images:
            sim = hashing.calculate_similarity(current_hash, db_h)
            
            # If it's a likely match (>80%), do a deep SSIM check
            if sim > 80:
                matches += 1
                db_path = os.path.join(UPLOAD_DIR, fname)
                if os.path.exists(db_path):
                    s_score = visual_difference.compute_ssim(path, db_path)
                    best_ssim = max(best_ssim, s_score)
            
            best_phash = max(best_phash, sim)

        # 4. Calculate Final Score
        final = (0.7 * best_phash) + (0.3 * best_ssim) if best_ssim > 0 else best_phash
        
        # 5. Tamper Detection & Engagement Simulation
        tamper_results = tamper_detection.analyze_tampering(path)
        eng_sim = engagement.simulate_engagement(final)

        # 6. Save to database for future checks
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
        # Prints the exact error to your Render Logs
        print(traceback.format_exc()) 
        # Sends the error message cleanly back to the frontend JSON so it won't trigger the 'I' error
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Mount frontend files from the root directory so Render serves them
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="static")