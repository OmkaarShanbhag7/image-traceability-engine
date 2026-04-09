def simulate_engagement(score):
    if score > 80:
        return "High viral potential"
    elif score > 50:
        return "Moderate engagement"
    else:
        return "Low engagement"