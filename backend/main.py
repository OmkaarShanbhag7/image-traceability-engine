@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_hash = generate_phash(file_path)

    db = SessionLocal()
    images = db.query(ImageRecord).all()

    total_images_compared = len(images)

    top_matches = []

    for image in images:
        similarity = compare_hash(new_hash, image.phash)

        image_path = f"{UPLOAD_FOLDER}/{image.filename}"

        try:
            visual_diff = calculate_ssim(file_path, image_path)
        except:
            visual_diff = 100  # worst case

        ssim_similarity = max(0, 100 - visual_diff)

        final_score = (0.7 * similarity) + (0.3 * ssim_similarity)

        top_matches.append({
            "filename": image.filename,
            "phash_similarity": round(similarity, 2),
            "ssim_similarity": round(ssim_similarity, 2),
            "final_score": round(final_score, 2)
        })

    top_matches = sorted(top_matches, key=lambda x: x["final_score"], reverse=True)[:3]

    db.add(ImageRecord(filename=file.filename, phash=new_hash))
    db.commit()
    db.close()

    best_match = top_matches[0] if top_matches else None

    confidence_score = best_match["final_score"] if best_match else 0
    authenticity_score = max(0, 100 - confidence_score)

    if confidence_score > 80:
        classification = "Reused Content"
    elif confidence_score > 50:
        classification = "Suspicious"
    else:
        classification = "Authentic"


    tamper_status = detect_tampering(file_path)
    engagement_status = simulate_engagement(confidence_score)

    return {
        "top_matches": top_matches,
        "confidence_score": f"{confidence_score:.2f}%",
        "authenticity_score": f"{authenticity_score:.2f}%",
        "classification": classification,
        "total_images_compared": total_images_compared,
        "tamper_analysis": tamper_status,
        "engagement_analysis": engagement_status
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
