const BACKEND_URL = "https://image-traceability-engine.onrender.com"; // change if needed

async function uploadImage() {
async function upload() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image!");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");

    let formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // Fill analysis
        document.getElementById("confidence").innerText = data.confidence.toFixed(2) + "%";
        document.getElementById("authenticity").innerText = data.authenticity.toFixed(2) + "%";
        document.getElementById("classification").innerText = data.classification;
        document.getElementById("seen").innerText = data.seen_before_count;
        document.getElementById("tamper").innerText = data.tamper_status;
        document.getElementById("engagement").innerText = data.engagement;

        // Top Matches
        let matchesHTML = "";
        data.top_matches.forEach(m => {
            matchesHTML += `
                <div>
                    <p><strong>${m.filename}</strong> — ${m.score.toFixed(2)}%</p>
                </div>
            `;
        });
        document.getElementById("matches").innerHTML = matchesHTML;

        // Online Matches
        let onlineHTML = "";
        data.online_matches.forEach(m => {
            onlineHTML += `
                <div>
                    <img src="${m.thumbnail}" width="120"><br>
                    <p>${m.title}</p>
                    <a href="${m.link}" target="_blank">🔗 View Source</a>
                    <hr>
                </div>
            `;
        });
        document.getElementById("online").innerHTML = onlineHTML;

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("result").classList.remove("hidden");

    } catch (error) {
        console.error(error);
        alert("Error connecting to backend");
        }
    }
}