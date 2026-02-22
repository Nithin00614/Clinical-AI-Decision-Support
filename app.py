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

    st.subheader("Enter Clinical Features")

    col1, col2 = st.columns(2)

    with col1:
        bp = st.number_input("Blood Pressure", value=120)
        sg = st.number_input("Specific Gravity", value=1.02, format="%.3f")
        al = st.number_input("Albumin", value=0)
        su = st.number_input("Sugar", value=0)
        rbc = st.selectbox("RBC (0=abnormal,1=normal)", [0,1])
        bu = st.number_input("Blood Urea", value=10)
        sc = st.number_input("Serum Creatinine", value=0.7)

    with col2:
        sod = st.number_input("Sodium", value=140)
        pot = st.number_input("Potassium", value=4.2)
        hemo = st.number_input("Hemoglobin", value=15.0)
        wbcc = st.number_input("WBC Count", value=7000)
        rbcc = st.number_input("RBC Count", value=5)
        htn = st.selectbox("Hypertension (0/1)", [0,1])

    if st.button("Run Prediction"):

        st.session_state.payload = {
            "bp": bp,
            "sg": sg,
            "al": al,
            "su": su,
            "rbc": rbc,
            "bu": bu,
            "sc": sc,
            "sod": sod,
            "pot": pot,
            "hemo": hemo,
            "wbcc": wbcc,
            "rbcc": rbcc,
            "htn": htn
        }

        start = time.time()
        res = requests.post(f"{API}/reason", json=st.session_state.payload)
        latency = time.time() - start

        if res.status_code == 200:
            data = res.json()
            data["prediction"]["latency"] = latency
            st.session_state.latest = data

            st.session_state.timeline.append({
                "risk": data["prediction"]["risk_score"],
                "confidence": data["prediction"]["confidence"],
                "mode": data["prediction"]["decision_mode"]
            })
        else:
            st.error("Backend error")

    if st.session_state.latest:

        pred = st.session_state.latest["prediction"]

        risk = float(pred["risk_score"])
        conf = float(pred["confidence"])
        mode = pred["decision_mode"]

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"### {risk_badge(risk)} — {risk:.3f}")

            if risk < 0.3:
                st.info("Clinical interpretation: low likelihood of CKD progression.")
            elif risk < 0.7:
                st.warning("Clinical interpretation: monitoring recommended.")
            else:
                st.error("Clinical interpretation: specialist evaluation recommended.")

        with c2:
            st.markdown(f"### {conf_badge(conf)} — {conf:.3f}")

            if mode == "SAFE":
                st.info("SAFE mode triggered due to limited certainty or weak signals.")
                st.warning("SAFE triggered due to uncertainity or weak supporting signals.")

        st.caption(f"Inference latency: {pred.get('latency', 0):.2f}s")

        abnormal = abnormal_snapshot(st.session_state.payload)
        if abnormal:
            st.error("Patient snapshot: " + ", ".join(abnormal))  

#===================== Reasoning TAB =====================

with tabs[1]:

    if not st.session_state.latest:
        st.info("Run prediction to view reasoning.")
    else:
        data = st.session_state.latest
        exp = data["explainability"]
        reason = data["reasoning"]
        mode = data["prediction"]["decision_mode"]

        st.subheader("Explainability Reliability")
        st.write(explanation_confidence(mode))
        st.caption("Based on SHAP availability + guideline retrieval + model certainity")

        st.subheader("Model Explainability")
        st.caption("Top contributing features shown first.")

        shap_text = exp.get("shap_explanation")

        with st.expander("Feature contribution explanation", expanded=True):
            st.caption("Feature attribution reflects model influence, not casual clinical relationships.")
            if shap_text and "unavailable" not in shap_text.lower():
                st.success(shap_text)
            else:
                st.warning("SHAP explanation unavailable for this prediction.")    

        st.subheader("Retrieved Evidence")
        st.success(exp.get("retrieved_evidence", "None"))

        st.subheader("Clinician Summary")
        for line in reason["clinician_summary"].split("\n"):
            st.success("." + line)

        with st.expander("Decision Trace"):
            st.write("Risk → Confidence → Decision Mode → Guardrails → LLM reasoning")
            st.caption("Confidence derived from certainity + SHAP availabilty + guideline retrieval")

        with st.expander("Full Explanation"):
            st.write(reason["full_explanation"])

        if reason.get("references"):
            st.markdown("### 📚 Evidence & References")
            st.info(reason["references"])

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
st.caption("Clinical decision-support only. Not a replacement for medical judgment.")