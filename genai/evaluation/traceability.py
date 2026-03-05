def compute_driver_evidence_traceability(drivers, evidence_chunks):

    if isinstance(evidence_chunks, str):
        evidence_chunks = [evidence_chunks]

    text = " ".join(evidence_chunks).lower()

    matched = 0

    for d in drivers:

        if isinstance(d, tuple):
            feature = d[0]
        else:
            feature = d

        if feature.lower() in text:
            matched += 1

    return matched / len(drivers) if drivers else 0