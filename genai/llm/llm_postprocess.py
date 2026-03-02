import re

def build_clinician_summary(text: str, payload: dict = None) -> str:
    if not payload:
        return "Clinical review recommended."

    risk = payload.get("risk_score", 0)
    confidence = payload.get("confidence", 0)

    shap = payload.get("shap") or {}
    top_pos = shap.get("top_positive", [])[:2]

    drivers = [f["feature"] for f in top_pos] if top_pos else []

    if risk > 0.8:
        severity = "High CKD progression risk."
    elif risk > 0.5:
        severity = "Moderate CKD progression risk."
    else:
        severity = "Lower CKD progression risk."

    driver_text = ""
    if drivers:
        driver_text = f" Key drivers: {', '.join(drivers)}."

    uncertainty = ""
    if confidence < 0.6:
        uncertainty = " Interpret cautiously due to lower confidence."

    return severity + driver_text + uncertainty


def split_references(text: str):
    lower = text.lower()

    ref_markers = ["references:", "kdigo", ".pdf", "study", "trial"]

    for marker in ref_markers:
        idx = lower.find(marker)
        if idx != -1 and idx > len(text) * 0.4:
            body = text[:idx]
            refs = text[idx:]
            return body.strip(), refs.strip()

    return text.strip(), None

def structure_explanation(text: str) -> str:
    if not text:
        return ""

    sections = [
        "### Risk Interpretation\n",
        "### Key Contributing Factors\n",
        "### Clinical Uncertainty\n",
        "### Suggested Clinical Action\n",
    ]

    parts = text.split("\n\n")

    structured = ""
    for i, part in enumerate(parts):
        if i < len(sections):
            structured += sections[i] + part + "\n\n"
        else:
            structured += part + "\n\n"

    return structured.strip()  

def extract_references_ids(text: str):
    pattern = r"\[(.*?)\]"
    matches = re.findall(pattern, text)
    structured = []
    seen = set()

    for ref in matches:
        if "::page_" in ref:
            doc, page = ref.split("::page_")
            key = (doc, int(page))
            if key not in seen:
                structured.append({
                    "document": doc,
                    "page": int(page)
                })
                seen.add(key)

    structured = sorted(structured, key=lambda x: (x["document"], x["page"]))
    return structured