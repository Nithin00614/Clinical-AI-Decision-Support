def compute_driver_evidence_traceability(drivers, evidence_chunks):

    if not evidence_chunks:
        return 0

    if isinstance(evidence_chunks, str):
        evidence_chunks = [evidence_chunks]

    text = " ".join(str(e) for e in evidence_chunks).lower()

    matched = 0

    for d in drivers:

        if isinstance(d, tuple):
            feature = d[0]
        else:
            feature = d

        if str(feature).lower() in text:
            matched += 1
    traced = round(matched / len(drivers) if drivers else 0, 2)
    return traced