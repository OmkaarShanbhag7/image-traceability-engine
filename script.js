const BACKEND_URL = "https://image-traceability-engine.onrender.com"; // change if needed

const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        imagePreview.src = URL.createObjectURL(e.target.files[0]);
        imagePreview.style.display = 'block';
        analyzeBtn.disabled = false;
    }
});

analyzeBtn.addEventListener('click', async () => {
    analyzeBtn.textContent = 'Processing...';
    const formData = new FormData();
    formData.append('file', imageInput.files[0]);

    try {
        const response = await fetch('/analyze', { method: 'POST', body: formData });
        const data = await response.json();
        
        resultsSection.classList.remove('hidden');
        document.getElementById('authScore').textContent = `${data.final_score.toFixed(1)}%`;
        document.getElementById('decisionText').textContent = data.decision;
        document.getElementById('phashResult').textContent = `${data.similarity.phash_similarity.toFixed(1)}%`;
        document.getElementById('ssimResult').textContent = `${data.similarity.ssim_score.toFixed(1)}%`;
        document.getElementById('matchesFound').textContent = data.traceability.seen_before_count;
        document.getElementById('tamperStatus').textContent = data.tamper_analysis.suspicious ? "Modified" : "Original";
        document.getElementById('edgeVariance').textContent = Math.round(data.tamper_analysis.edge_variance);
        document.getElementById('viralScore').textContent = data.engagement.viral_score;
        document.getElementById('behaviorText').textContent = data.engagement.behavior;

    } catch (err) {
        alert("Server Error. Make sure backend is running.");
    } finally {
        analyzeBtn.textContent = 'Run Analysis';
    }
});