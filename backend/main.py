from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from visual_difference import calculate_ssim
from database import engine, SessionLocal
from models import Base, ImageRecord
from hashing import generate_phash, compare_hash
from tamper_detection import detect_tampering
from engagement import simulate_engagement

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folder for uploaded images
UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_hash = generate_phash(file_path)

    db = SessionLocal()
    images = db.query(ImageRecord).all()

    total_images_compared = len(images)

    reuse_score = 0
    most_similar_filename = None
    most_similar_path = None

    for image in images:
        similarity = compare_hash(new_hash, image.phash)
        if similarity > reuse_score:
            reuse_score = similarity
            most_similar_filename = image.filename
            most_similar_path = f"{UPLOAD_FOLDER}/{image.filename}"

    db.add(ImageRecord(filename=file.filename, phash=new_hash))
    db.commit()
    db.close()

    tamper_status = detect_tampering(file_path)
    engagement_status = simulate_engagement(reuse_score)

    risk_level = "Low Risk"
    if reuse_score > 80:
        risk_level = "High Reuse Risk"
    elif reuse_score > 50:
        risk_level = "Moderate Reuse Risk"

    visual_difference = None
    if most_similar_path:
        visual_difference = calculate_ssim(file_path, most_similar_path)

    return {
        "reuse_probability": f"{reuse_score:.2f}%",
        "similarity_score": f"{reuse_score:.2f}",
        "most_similar_image": most_similar_filename,
        "total_images_compared": total_images_compared,
        "tamper_analysis": tamper_status,
        "engagement_analysis": engagement_status,
        "risk_level": risk_level,
        "visual_difference_percentage": visual_difference
    }

@app.post("/reset")
def reset_system():
    db = SessionLocal()
    db.query(ImageRecord).delete()
    db.commit()
    db.close()

    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, file))

    return {"message": "System reset successfully"}
