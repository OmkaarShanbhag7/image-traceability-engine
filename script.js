const BACKEND_URL = "https://image-traceability-engine.onrender.com"; // change if needed

async function uploadImage() {
    const fileInput = document.getElementById("imageInput");

    if (!fileInput.files[0]) {
        alert("Please select an image first.");
        return;
    }

    // 🔥 Loading UI
    document.getElementById("result").innerHTML = `
        <div style="text-align:center;">
            <h2>Analyzing Image...</h2>
            <p>Please wait...</p>
        </div>
    `;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch(`${BACKEND_URL}/analyze`, {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    // 🔥 MAIN RESULT CARD
    let html = `
        <div style="background:#111; padding:20px; border-radius:15px; margin-top:20px;">
            <h2>Analysis Report</h2>

            <p><b>Confidence Score:</b> ${result.confidence_score}</p>
            <p><b>Authenticity Score:</b> ${result.authenticity_score}</p>
            <p><b>Classification:</b> ${result.classification}</p>
            <p><b>Total Images Compared:</b> ${result.total_images_compared}</p>
            <p><b>Tamper Status:</b> ${result.tamper_analysis}</p>
            <p><b>Engagement:</b> ${result.engagement_analysis}</p>
        </div>

        <h2 style="margin-top:30px;">Top Matches</h2>
    `;

    // 🔥 SHOW TOP 3 MATCHES
    result.top_matches.forEach(match => {
        html += `
            <div style="background:#1a1a1a; padding:15px; border-radius:12px; margin-top:15px;">
                <p><b>Image:</b> ${match.filename}</p>
                <p>pHash Similarity: ${match.phash_similarity}%</p>
                <p>SSIM Similarity: ${match.ssim_similarity}%</p>
                <p><b>Final Score:</b> ${match.final_score}%</p>

                <img src="${BACKEND_URL}/uploads/${match.filename}" width="200" style="margin-top:10px; border-radius:10px;">
            </div>
        `;
    });

    document.getElementById("result").innerHTML = html;
}

// 🔥 RESET BUTTON
async function resetSystem() {
    await fetch(`${BACKEND_URL}/reset`, {
        method: "POST"
    });

    document.getElementById("result").innerHTML =
        "<h2>System Reset Successfully</h2>";
}