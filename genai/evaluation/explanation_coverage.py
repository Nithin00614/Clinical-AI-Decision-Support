def compute_explanation_coverage(explanation, drivers):

    if not explanation:
        return 0.0

    text = explanation.lower()

    covered = 0

    for d in drivers:

        if isinstance(d, tuple):
            feature = d[0]
        else:
            feature = d

        if feature.lower() in text:
            covered += 1

    return covered / len(drivers) if drivers else 0