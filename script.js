const BACKEND_URL = "https://image-traceability-engine.onrender.com";

async function uploadImage() {
    const fileInput = document.getElementById("imageInput");

    if (!fileInput.files[0]) {
        alert("Please select an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch(`${BACKEND_URL}/analyze`, {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    document.getElementById("result").innerHTML = `
        <h3>Analysis Report</h3>

        <p><b>Reuse Probability:</b> ${result.reuse_probability}</p>
        <p><b>Total Images Compared:</b> ${result.total_images_compared}</p>
        <p><b>Tamper Status:</b> ${result.tamper_analysis}</p>
        <p><b>Engagement Analysis:</b> ${result.engagement_analysis}</p>
        <p><b>Risk Level:</b> ${result.risk_level}</p>
    `;

    if (result.visual_difference_percentage !== null) {
        document.getElementById("result").innerHTML += `
            <p><b>Visual Difference:</b> ${result.visual_difference_percentage}%</p>
        `;
    }

    if (result.most_similar_image) {
        document.getElementById("result").innerHTML += `
            <h3>Most Similar Stored Image</h3>
            <div style="display:flex; justify-content:center; gap:40px; margin-top:20px;">
                <div>
                    <p><b>Uploaded Image</b></p>
                    <img src="${URL.createObjectURL(fileInput.files[0])}" width="250">
                </div>
                <div>
                    <p><b>Matched Image</b></p>
                    <img src="${BACKEND_URL}/uploads/${result.most_similar_image}" width="250">
                </div>
            </div>
        `;
    }
}

async function resetSystem() {
    await fetch(`${BACKEND_URL}/reset`, {
        method: "POST"
    });

    document.getElementById("result").innerHTML =
        "<h3>System Reset Successfully</h3>";
}
