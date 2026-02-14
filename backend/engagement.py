def simulate_engagement(reuse_score):
    if reuse_score > 80:
        return "Likely Organic Engagement"
    elif reuse_score > 50:
        return "Mixed Engagement"
    else:
        return "Suspicious Engagement Pattern"
