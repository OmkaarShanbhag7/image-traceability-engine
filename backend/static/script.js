async function uploadImage() {
    const fileInput = document.getElementById("imageInput");

    if (!fileInput.files[0]) {
        alert("Please select an image first.");
        return;
    }

    // 🔥 Loading state
    document.getElementById("result").innerHTML = `
        <h3>Analyzing...</h3>
        <p>Please wait while we process the image.</p>
    `;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        // ❗ handle server error
        if (!response.ok) {
            throw new Error("Server error");
        }

        const result = await response.json();

        let html = `
            <h3>Analysis Report</h3>

            <p><b>Reuse Probability:</b> ${result.reuse_probability}</p>
            <p><b>Total Images Compared:</b> ${result.total_images_compared}</p>
            <p><b>Tamper Status:</b> ${result.tamper_analysis}</p>
            <p><b>Engagement Analysis:</b> ${result.engagement_analysis}</p>
            <p><b>Risk Level:</b> ${result.risk_level}</p>
        `;

        if (result.visual_difference_percentage !== null) {
            html += `
                <p><b>Visual Difference:</b> ${result.visual_difference_percentage}%</p>
            `;
        }

        // 🔥 Show images comparison
        if (result.most_similar_image) {
            html += `
                <h3>Most Similar Stored Image</h3>
                <div style="display:flex; justify-content:center; gap:40px; margin-top:20px;">
                    <div>
                        <p><b>Uploaded Image</b></p>
                        <img src="${URL.createObjectURL(fileInput.files[0])}" width="250">
                    </div>
                    <div>
                        <p><b>Matched Image</b></p>
                        <img src="/uploads/${result.most_similar_image}" width="250">
                    </div>
                </div>
            `;
        }

        document.getElementById("result").innerHTML = html;

    } catch (error) {
        document.getElementById("result").innerHTML = `
            <h3>Error</h3>
            <p>Something went wrong. Please try again.</p>
        `;
        console.error(error);
    }
}


// 🔄 RESET SYSTEM
async function resetSystem() {
    try {
        await fetch("/reset", {
            method: "POST"
        });

        document.getElementById("result").innerHTML =
            "<h3>System Reset Successfully</h3>";

    } catch (error) {
        document.getElementById("result").innerHTML =
            "<h3>Error resetting system</h3>";
    }
}