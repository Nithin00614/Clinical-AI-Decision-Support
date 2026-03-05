def compute_explanation_reliability(traceability, coverage):

    score = (0.6 * traceability) +(0.4 * coverage) 

    if score >= 0.7:
        label = "HIGH"
    elif score >= 0.4:
        label = "MEDIUM"
    else:
        label = "LOW"

    return score, label