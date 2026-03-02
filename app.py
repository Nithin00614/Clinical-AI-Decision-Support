import streamlit as st 
import requests 
import time

API = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="CKD Clinical AI", layout="wide")

st.title("CKD Clinical Decision Support System")

#========================= HELPERS =========================

def risk_badge(score): 
    if score < 0.3: return "🟢 Low Risk" 
    elif score < 0.7: return "🟡 Moderate Risk" 
    return "🔴 High Risk"

def conf_badge(conf): 
    if conf > 0.75: return "🟢 High confidence" 
    elif conf > 0.45: return "🟡 Moderate confidence" 
    return "🔴 Low confidence"

def mode_badge(mode): 
    if mode == "SAFE": return "🟢 SAFE" 
    elif mode == "VERBOSE": return "🟡 VERBOSE" 
    elif mode == "FALLBACK": return "🔴 FALLBACK" 
    return mode

def abnormal_snapshot(payload): 
    if not payload:
        return []
    abnormal = [] 
    if payload.get("bp", 0) > 140: 
        abnormal.append("High BP") 
    if payload.get("sc", 0) > 1.3: 
        abnormal.append("Elevated Creatinine") 
    if payload.get("hemo", 0) < 11: 
        abnormal.append("Low Hemoglobin") 
    if payload.get("rbc", 1) == 0: 
        abnormal.append("Abnormal RBC")  
    if payload.get("al", 0) > 1: 
        abnormal.append("Albuminuria") 
    return abnormal

def explanation_confidence(mode): 
    if mode == "SAFE": return "LOW" 
    elif mode == "VERBOSE": return "MODERATE" 
    return "HIGH"

if "latest" not in st.session_state: 
    st.session_state.latest = None

if "timeline" not in st.session_state: 
    st.session_state.timeline = []

if "payload" not in st.session_state: 
    st.session_state.payload = None

tabs = st.tabs([ "Prediction", "Reasoning", "Clinician Override", "Review Queue", "System" ])


#===================== Prediction TAB =====================

with tabs[0]:

    st.subheader("Clinical Risk Assessment")

    # ================= INPUT SECTION =================

   # ===================== Prediction TAB =====================

with tabs[0]:

    st.subheader("Clinical Feature Input")

    # -------- Initialize Default State --------
    default_values = {
        "bp": 135,
        "sg": 1.015,
        "al": 1,
        "su": 0,
        "rbc": 1,
        "bu": 35,
        "sc": 1.3,
        "sod": 138,
        "pot": 4.6,
        "hemo": 12.0,
        "wbcc": 8500,
        "rbcc": 4.6,
        "htn": 1
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # -------- Sample Loader (MUST BE BEFORE WIDGETS) --------

    st.markdown("### Load Sample Cases")

    c1, c2, c3 = st.columns(3)

    if c1.button("🟢 Low Risk Sample"):
        st.session_state.update({
            "bp": 100,
            "sg": 1.025,
            "al": 0,
            "su": 0,
            "rbc": 1,
            "bu": 10,
            "sc": 0.6,
            "sod": 142,
            "pot": 4.1,
            "hemo": 15.5,
            "wbcc": 6000,
            "rbcc": 5.2,
            "htn": 0
        })

    if c2.button("🟡 Moderate Risk Sample"):
        st.session_state.update({
            "bp": 120,
            "sg": 1.02,
            "al": 0,
            "su": 0,
            "rbc": 1,
            "bu": 20,
            "sc": 1.0,
            "sod": 140,
            "pot": 4.2,
            "hemo": 14.0,
            "wbcc": 8000,
            "rbcc": 5.0,
            "htn": 0
        })

    if c3.button("🔴 High Risk Sample"):
        st.session_state.update({
            "bp": 155,
            "sg": 1.01,
            "al": 3,
            "su": 1,
            "rbc": 0,
            "bu": 60,
            "sc": 2.8,
            "sod": 132,
            "pot": 5.5,
            "hemo": 9.5,
            "wbcc": 11000,
            "rbcc": 3.5,
            "htn": 1
        })

    st.markdown("---")

    # -------- Input Widgets --------

    col1, col2 = st.columns(2)

    with col1:
        bp = st.number_input("Blood Pressure", key="bp")
        sg = st.number_input("Specific Gravity", format="%.3f", key="sg")
        al = st.number_input("Albumin", key="al")
        su = st.number_input("Sugar", key="su")
        rbc = st.selectbox("RBC (0=abnormal,1=normal)", [0,1], key="rbc")
        bu = st.number_input("Blood Urea", key="bu")
        sc = st.number_input("Serum Creatinine", key="sc")

    with col2:
        sod = st.number_input("Sodium", key="sod")
        pot = st.number_input("Potassium", key="pot")
        hemo = st.number_input("Hemoglobin", key="hemo")
        wbcc = st.number_input("WBC Count", key="wbcc")
        rbcc = st.number_input("RBC Count", key="rbcc")
        htn = st.selectbox("Hypertension (0/1)", [0,1], key="htn")

    st.markdown("---")

    # -------- Run Prediction --------
    st.write("Stored latest:", st.session_state.latest)
    if st.button("Run Prediction"):

        payload = {k: st.session_state.get(k) for k in default_values.keys()}
        

        start = time.time()
        res = requests.post(f"{API}/reason", json=payload)
        latency = time.time() - start

        if res.status_code == 200:

            data = res.json()
            st.session_state.latest = data
            pred = data["prediction"]

            risk = float(pred["risk_score"])
            confidence = float(pred["confidence"])
            mode = pred["decision_mode"]

            certainty = abs(risk - 0.5) * 2

            st.markdown("## Risk Summary")
            st.caption("Risk score represents calibrated probability from primary CKD classifier.")

            c1, c2 = st.columns(2)

            with c1:
                if risk < 0.30:
                    st.success(f"🟢 Low Probability of CKD — {risk:.3f}")
                elif risk < 0.60:
                    st.warning(f"🟡 Intermediate Probability (Near Decision Boundary) — {risk:.3f}")
                else:
                    st.error(f"🔴 High Probability of CKD — {risk:.3f}")

                if certainty < 0.2:
                    st.caption(f"Model Separation: {certainty:.3f} (Low — near decision boundary)")
                elif certainty < 0.6:
                    st.caption(f"Model Separation: {certainty:.3f} (Moderate)")
                else:
                    st.caption(f"Model Separation: {certainty:.3f} (High — strong separation)")

            with c2:
                if confidence > 0.75:
                    st.success(f"System Confidence: HIGH — {confidence:.3f}")
                elif confidence > 0.45:
                    st.warning(f"System Confidence: MODERATE — {confidence:.3f}")
                else:
                    st.error(f"System Confidence: LOW — {confidence:.3f}")

                st.caption(f"Routing Decision Mode: {mode}")


                if mode == "SAFE":
                    st.info("SAFE mode activated due to low separation or low confidence.")
                elif mode == "VERBOSE":
                    st.info("VERBOSE mode activated for enhanced explanation due to moderate confidence.")
                else:
                    st.info("NORMAL mode activated — stable prediction confidence.")

            st.markdown("---")

            st.markdown("### System Diagnostics")

            st.json({
                "risk_score": round(risk, 4),
                "model_separation": round(certainty, 4),
                "system_confidence": round(confidence, 4),
                "decision_mode": mode,
                "inference_latency_seconds": (round(latency, 3))
            })
        else:
            st.error("Backend error. Please check API.")


# ===================== REASONING TAB =====================

with tabs[1]:

    if  st.session_state.latest is None:
        st.info("Run prediction to view reasoning.")
    else:
        data = st.session_state.latest
        st.write("debug latest:", st.session_state.latest)

        prediction = data["prediction"]
        explainability = data.get("explainability", {})
        reasoning = data.get("reasoning", {})
        diagnostics = data.get("diagnostics", {})

        st.header("Clinical Reasoning Engine")

        # ======================================================
        # SECTION 1 — Explainability Reliability
        # ======================================================

        st.subheader("Explainability Reliability")

        structured_shap = explainability.get("structured_shap", {})
        shap_latency = explainability.get("shap_latency", None)
        shap_missing = explainability.get("missing_features", [])
        shap_mismatch = diagnostics.get("shap_mismatch", False)
        explain_rel = diagnostics.get("explainability_reliability", "UNKNOWN")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Vector Available:", structured_shap.get("vector_available", False))
            st.write("Missing Features:", shap_missing if shap_missing else "None")
            st.write("Mismatch Detected:", shap_mismatch)

        with col2:
            st.write("Explainability Reliability:", explain_rel)
            if shap_latency is not None:
                st.write("SHAP Latency (s):", round(shap_latency, 3))

        st.markdown("---")

        # ======================================================
        # SECTION 2 — Structured Feature Attribution
        # ======================================================

        st.subheader("Feature Attribution (Model-Level)")

        top_positive = structured_shap.get("top_positive", [])
        top_negative = structured_shap.get("top_negative", [])

        col_pos, col_neg = st.columns(2)

        with col_pos:
            st.markdown("### 🔺 Positive Contributors")
            if top_positive:
                for item in top_positive:
                    st.write(f"{item['feature']} → {round(item['impact'],4)}")
            else:
                st.info("No positive contributors available.")

        with col_neg:
            st.markdown("### 🔻 Negative Contributors")
            if top_negative:
                for item in top_negative:
                    st.write(f"{item['feature']} → {round(item['impact'],4)}")
            else:
                st.info("No negative contributors available.")

        st.markdown("---")

        # ======================================================
        # SECTION 3 — Evidence Retrieval
        # ======================================================

        st.subheader("Retrieved Clinical Evidence")

        retrieval_count = explainability.get("retrieval_count", 0)
        retrieval_latency = explainability.get("retrieval_latency", None)
        retrieved_chunks = explainability.get("retrieved_evidence_chunks", [])

        st.write("Evidence Count:", retrieval_count)

        if retrieval_latency is not None:
            st.write("Retrieval Latency (s):", round(retrieval_latency, 3))

        if retrieved_chunks:
            for idx, chunk in enumerate(retrieved_chunks):
                with st.expander(f"Evidence Source {idx+1}"):
                    st.write(chunk)
        else:
            st.warning("No evidence retrieved for this case.")

        st.markdown("---")

        # ======================================================
        # SECTION 4 — Generated Clinical Reasoning
        # ======================================================

        st.subheader("Generated Clinical Summary")

        clinician_summary = reasoning.get("clinician_summary", "")

        if clinician_summary:
            for line in clinician_summary.split("\n"):
                if line.strip():
                    st.write("•", line.strip())
        else:
            st.warning("No clinician summary available.")

        with st.expander("Full Clinical Explanation"):
            st.write(reasoning.get("full_explanation", "Not available."))

        st.markdown("---")

        # ======================================================
        # SECTION 5 — Reasoning Diagnostics
        # ======================================================

        st.subheader("Reasoning Diagnostics")

        explanation_conf = diagnostics.get("explanation_confidence", None)
        reasoning_rel = diagnostics.get("reasoning_reliability", None)
        clinician_trust = diagnostics.get("clinician_trust", None)

        diag_col1, diag_col2 = st.columns(2)

        with diag_col1:
            st.write("Explanation Confidence:", explanation_conf)
            st.write("Reasoning Reliability:", reasoning_rel)

        with diag_col2:
            st.write("Clinician Trust Level:", clinician_trust)
            st.write("Decision Mode:", prediction.get("decision_mode"))

        # ======================================================
        # SECTION 6 — Coverage Check (High ROI)
        # ======================================================

        st.markdown("---")
        st.subheader("Explanation Coverage Validation")

        llm_text = reasoning.get("full_explanation", "").lower()

        shap_features = [f["feature"].lower() for f in top_positive] if top_positive else []

        if shap_features and llm_text:
            mentioned = sum(1 for f in shap_features if f in llm_text)
            coverage = mentioned / len(shap_features)

            st.write("Top Feature Coverage:", round(coverage, 2))

            if coverage < 0.4:
                st.warning("Low alignment between SHAP features and explanation.")
            else:
                st.success("Good alignment between model drivers and explanation.")
        else:
            st.info("Coverage validation unavailable.")

#===================== OVERRIDE TAB =====================

with tabs[2]:

    st.subheader("Clinician Override")

    pid = st.text_input("Patient ID")
    decision = st.selectbox("Override Decision", ["SAFE", "NORMAL", "VERBOSE"])
    notes = st.text_area("Clinical Notes")

    if st.button("Submit Override"):
        payload = {
            "patient_id": pid,
            "override_decision": decision,
            "clinician_notes": notes
        }

        st.session_state.payload.update(payload)

        r = requests.post(f"{API}/clinician/review", json=st.session_state.payload)

        if r.status_code == 200:
            st.success("Override stored")
        else:
            st.error(r.text)

#===================== REVIEW QUEUE =====================

with tabs[3]:

    st.subheader("Decision Timeline")
    st.json(st.session_state.timeline)

#===================== SYSTEM =====================

with tabs[4]:

    r = requests.get(f"{API}/metadata")

    if r.status_code == 200:
        st.json(r.json())
    else:
        st.error("Backend offline")

st.markdown("---")
st.caption("This system provides decision-support guidance. Final clinical decisions remain under physician responsibility.")