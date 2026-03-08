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
    """
    Parse and preserve the LLM's strict output template structure.
    The LLM is prompted to return sections with these headers:
    - Risk Interpretation:
    - Key Contributing Factors:
      - Risk Increasing Drivers:
      - Risk Reducing Drivers:
    - Clinical Uncertainty:
    - Potential Clinical Considerations:
    - References:
    
    This function preserves that structure and formats it for UI rendering.
    """
    if not text:
        return ""

    # Check if text already has the structured template headers
    expected_headers = [
        "Risk Interpretation:",
        "Key Contributing Factors:",
        "Clinical Uncertainty:",
        "Potential Clinical Considerations:",
        "References:"
    ]
    
    has_structure = any(header in text for header in expected_headers)
    
    if not has_structure:
        # If LLM didn't follow template, add markdown headers to free-form text
        # and split into logical parts
        parts = text.split("\n\n")
        structured = ""
        
        if len(parts) > 0:
            structured += "### Risk Interpretation\n\n" + parts[0] + "\n\n"
        
        if len(parts) > 1:
            structured += "### Key Contributing Factors\n\n" + parts[1] + "\n\n"
        
        if len(parts) > 2:
            structured += "### Clinical Uncertainty\n\n" + parts[2] + "\n\n"
        
        if len(parts) > 3:
            structured += "### Additional Context\n\n" + "\n\n".join(parts[3:]) + "\n\n"
        
        return structured.strip()
    
    # If LLM followed template, convert plain text headers to markdown for UI
    structured = text.replace("Risk Interpretation:", "### Risk Interpretation")
    structured = structured.replace("Key Contributing Factors:", "### Key Contributing Factors")
    structured = structured.replace("Risk Increasing Drivers:", "**Risk Increasing Drivers:**")
    structured = structured.replace("Risk Reducing Drivers:", "**Risk Reducing Drivers:**")
    structured = structured.replace("Clinical Uncertainty:", "### Clinical Uncertainty")
    structured = structured.replace("Potential Clinical Considerations:", "### Potential Clinical Considerations")
    structured = structured.replace("References:", "### References")
    
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