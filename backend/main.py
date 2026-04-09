from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import traceback

from database import init_db, insert_image, get_all_images
from hashing import compute_phash, phash_similarity
from visual_difference import compute_ssim
from tamper_detection import detect_tampering
from engagement import simulate_engagement

# OPTIONAL (keep if working)
try:
    from reverse_search_online import search_online
except:
    def search_online(x): return []

# ------------------ APP SETUP ------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ STORAGE ------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ INIT DB ------------------
init_db()

# ------------------ API ------------------
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 🔹 Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Saved:", file.filename)

        # 🔹 Generate hash
        new_hash = compute_phash(file_path)
        print("NEW HASH:", new_hash)

        # 🔹 Get DB data
        images = get_all_images()
        print("DB DATA:", images)

        results = []

        # 🔹 Compare with DB images
        for filename, phash, upload_time in images:
            try:
                existing_path = os.path.join(UPLOAD_FOLDER, filename)

                # 🔥 STRONG DEMO MATCH FIX
                if new_hash == phash:
                    final_score = 100
                else:
                    phash_score = phash_similarity(new_hash, phash)
                    ssim_score = compute_ssim(file_path, existing_path)
                    final_score = 0.7 * phash_score + 0.3 * ssim_score

                results.append({
                    "filename": filename,
                    "score": final_score,
                    "upload_time": upload_time
                })

            except Exception as e:
                print("Comparison error:", e)

        # 🔹 Sort results
        results.sort(key=lambda x: x["score"], reverse=True)
        top_matches = results[:3]

        # 🔹 Seen before count
        seen_before = len([r for r in results if r["score"] > 70])

        # 🔹 Confidence
        confidence = top_matches[0]["score"] if top_matches else 0
        authenticity = 100 - confidence

        # 🔹 Classification
        if confidence > 80:
            classification = "Reused"
        elif confidence > 50:
            classification = "Suspicious"
        else:
            classification = "Authentic"

        # 🔹 Tamper
        try:
            tamper = detect_tampering(file_path)
        except:
            tamper = "Unknown"

        # 🔹 Engagement
        try:
            engagement = simulate_engagement(confidence)
        except:
            engagement = "Unknown"

        # 🔹 Online search (safe)
        try:
            online_results = search_online(file_path)
        except Exception as e:
            print("Online search failed:", e)
            online_results = []

        # 🔹 Save to DB
        insert_image(file.filename, new_hash)
        print("Inserted into DB:", file.filename)

        # 🔹 Return response
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

    except Exception as e:
        print("UPLOAD ERROR:")
        traceback.print_exc()
        return {
            "error": str(e)
        }