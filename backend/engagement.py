import random

def simulate_engagement(score):
    v_score = random.randint(70, 100) if score > 70 else random.randint(10, 60)
    behavior = "Likely to go viral due to reuse/controversy" if score > 70 else "Natural organic reach"
    return {"viral_score": v_score, "behavior": behavior}