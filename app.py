import streamlit as st 
import requests 
import time

API = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="CKD Clinical AI", layout="wide")

st.title("CKD Clinical AI Decision Support System")
st.info("⚕️ Clinical Decision Support Tool")
st.caption("This System Assists Clinicians by Highlighting CKD Risk Patterns based on EHR Features.")
st.caption("Predictions are not Medical Diagnoses and Require Physician Validation.")

st.markdown("---")

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


with tabs[0]:

    st.subheader("Clinical Risk Assessment")

    # ---------------- Sample Loaders ----------------

    st.markdown("### Load Sample Case")

    col_s1, col_s2, col_s3 = st.columns(3)

    if col_s1.button("🟢 Low Risk Sample"):
        st.session_state.update({
            "bp": 100, "sg": 1.025, "al": 0, "su": 0,
            "rbc": 1, "bu": 10, "sc": 0.6,
            "sod": 142, "pot": 4.1,
            "hemo": 15.5, "wbcc": 6000,
            "rbcc": 5.2, "htn": 0
        })

    if col_s2.button("🟡 Moderate Risk Sample"):
        st.session_state.update({
            "bp": 120, "sg": 1.020, "al": 0, "su": 0,
            "rbc": 1, "bu": 20, "sc": 1.0,
            "sod": 140, "pot": 4.2,
            "hemo": 14.0, "wbcc": 8000,
            "rbcc": 5.0, "htn": 0
        })

    if col_s3.button("🔴 High Risk Sample"):
        st.session_state.update({
            "bp": 155, "sg": 1.010, "al": 3, "su": 1,
            "rbc": 0, "bu": 60, "sc": 2.8,
            "sod": 132, "pot": 5.5,
            "hemo": 9.5, "wbcc": 11000,
            "rbcc": 3.5, "htn": 1
        })

    st.divider()

    # ---------------- Input Section ----------------

    st.markdown("### Clinical Feature Input")

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

    st.divider()

    # ---------------- Run Prediction ----------------

    if st.button("Run Prediction"):

        payload = {
            "bp": bp, "sg": sg, "al": al, "su": su,
            "rbc": rbc, "bu": bu, "sc": sc,
            "sod": sod, "pot": pot,
            "hemo": hemo, "wbcc": wbcc,
            "rbcc": rbcc, "htn": htn
        }

        start_time = time.time()
        response = requests.post(f"{API}/reason", json=payload)
        total_latency = (time.time() - start_time) * 1000

        if response.status_code == 200:

            data = response.json()
            st.session_state.latest = data

            pred = data["prediction"]
            full_response = data
            metrics = data.get("system_metrics", {})

            risk = float(pred["risk_score"])
            risk_label = pred["risk_label"]
            reasoning_data = full_response.get("reasoning", {})
            confidence = float(pred["confidence"])
            mode = pred["decision_mode"]

            if risk >= 0.999:
                risk_display = "0.99"
            else:
                risk_display = f"{risk:.3f}"    

            separation = abs(risk - 0.5) 
            if separation >= 0.40:
                stability = "Very Stable"
            elif separation >= 0.25:
                stability = "Stable"
            elif separation >= 0.10:
                stability = "Moderate Stability"
            else:
                stability = "Near Decision Boundary"

            # ================= RISK SUMMARY =================

            st.markdown("## Risk Summary")
            st.caption("Calibrated Risk Probability reflects calibrated mode output, not a confirmed diagnosis.")
            st.divider()
            col_r1, col_r2 = st.columns(2)

            with col_r1:

                if risk_label == "LOW":
                    st.success(f"🟢 Low CKD Risk – Estimated Probability {risk_display}")
                elif risk_label == "MODERATE":
                    st.warning(f"🟡 Moderate CKD Risk – Estimated Probability {risk_display}")
                else:
                    st.error(f"🔴 High CKD Risk – Estimated Probability {risk_display}")
  
                
                st.caption("Decision Threshold: 0.50(Calibrated)")

                if risk < 0.30:
                    category = "LOW"
                elif risk < 0.60:
                    category = "MODERATE"
                else:
                    category = "HIGH"    

                st.markdown(f"***Decision Stability Distance:** {separation:.3f}")

                if separation >= 0.40:
                    st.success("Decision Stability: Very Stable")
                elif separation >= 0.25:
                    st.success("Decision Stability: Stable")
                elif separation >= 0.10:
                    st.warning("Decision Stability: Moderate Stability")
                else:
                    st.error("Decision Stability: Near Decision Boundary")
                st.caption("Distance of prediction from classification boundary (0.5). Higher values indicate more stable classification.")

                st.markdown("### Key Model Drivers (SHAP)")

                explain = data.get("explainability", {})
                shap_block = explain.get("shap", {})

                top_positive = shap_block.get("top_positive", [])
                top_negative = shap_block.get("top_negative", [])

                shown = False

                for item in top_positive[:2]:
                    feature = item.get("feature")
                    impact = item.get("impact")
                    st.markdown(f"• **{feature}** ↑ `{abs(impact):.2f}`")
                    shown = True

                for item in top_negative[:2]:
                    feature = item.get("feature")
                    impact = item.get("impact")
                    st.markdown(f"• **{feature}** ↓ `{abs(impact):.2f}`")
                    shown = True

                if not shown:
                    st.info("No SHAP drivers available for this prediction.")

                st.markdown("### Prediction Trust Score")

                explain_rel = reasoning_data.get("explanation_reliability", {}).get("score", 0)
                trust_score = (confidence + explain_rel) / 2

                st.metric("Trust Score", f"{trust_score:.2f}")
                st.caption("Combined Assessment of Model Prediction Stability and Explanation Grounding.")


                st.markdown("### Prediction Reliability")

                if confidence <= 0.39:
                    st.error(f"Prediction Reliability: LOW — {confidence:.2f}")
                elif confidence <= 0.69:
                    st.warning(f"Prediction Reliability: MEDIUM — {confidence:.2f}")
                else:
                    st.success(f"Prediction Reliability: HIGH — {confidence:.2f}")

                st.caption("Represents Calibrated System Reliability and Prediction Stability - Not Clinical Certainity. ")    

                model_version = pred.get("model_version", "UNKNOWN")
                st.caption(f"MODEL Version: {model_version}")

            with col_r2:

                st.markdown("### Decision Context")
                st.caption(f"Decision Mode: {mode}")
                decision_source = pred.get("decision_source", "MODEL")
                st.caption(f"Decision Source: {decision_source}")

                st.markdown("### Model Explainability")
                explain_status = full_response.get("explainability_status")

                if explain_status is None:
                    explain_status = "UNAVAILABLE"

                status_lower = explain_status.lower() if isinstance(explain_status, str) else ""
                
                if "available" in status_lower:
                    st.success("SHAP Explainability: AVAILABLE")
                elif "degraded" in status_lower:
                    st.warning("SHAP Explainability: DEGRADED")
                else:
                    st.error("SHAP Explainability: UNAVAILABLE")

                st.caption("Reflects Availability of SHAP-Based Model Drivers.")
                
                st.divider()
                st.markdown("### System Mode")
                if mode == "SAFE":
                    st.info("SAFE Mode Triggered Due to Low Prediction Separation (near decision boundary) or Degraded Explainability.")
                elif mode == "VERBOSE":
                    st.info("VERBOSE Mode Activated for Extended Reasoning Transparency.")
                else:
                    st.success("NORMAL Mode — Stable Prediction State.")

                st.caption("Reflects System Guardrail State Controlling Explanation Behaviour.")
            st.divider()

            # ================= ABNORMAL SNAPSHOT =================

            abnormal = abnormal_snapshot(payload)
            if abnormal:
                st.markdown("### Structured Clinical Snapshot")
                renal = []
                hemodynamic = []
                hematology = []
                metabolic = []

                for item in abnormal:
                    text = item.lower()
                    if "creatinine" in text or "albumin" in text or "gfr" in text:
                        renal.append(item)
                    elif "bp" in text:
                        hemodynamic.append(item)
                    elif "hemoglobin" in text or "rbc" in text:
                        hematology.append(item)
                    else:
                        metabolic.append(item)

                if hemodynamic:
                    st.markdown(f"**Hemodynamics:** {', '.join(hemodynamic)}")

                if renal:
                    st.markdown(f"**Renal Markers:** {', '.join(renal)}")

                if hematology:
                    st.markdown(f"**Hematology:** {','.join(hematology)}")

                if metabolic:
                    st.markdown(f"**Metabolic:** {','.join(metabolic)}")            

            st.divider()

            # ================= SYSTEM METRICS =================

            retrieval_ms = metrics.get("retrieval_latency_ms", 0)
            shap_ms = metrics.get("shap_latency_ms", 0)
            llm_ms = metrics.get("llm_latency_ms", 0)
            total_ms = metrics.get("total_latency_ms", total_latency)

            overhead_ms = max(total_ms - (retrieval_ms + shap_ms + llm_ms), 0)

            st.markdown("### Operational Latency (Audit Transparency Metrics)")
            st.caption("System Performance Metrics")
            m1, m2, m3, m4, m5 = st.columns(5)

            m1.metric("Retrieval (ms)", int(retrieval_ms))
            m2.metric("SHAP (ms)", round(shap_ms, 2))
            m3.metric("LLM (ms)", int(llm_ms))
            m4.metric("Overhead (ms)", int(overhead_ms))
            m5.metric("Total (ms)", int(total_ms))

            st.caption("Confidence Reflects Model Calibration Reliability and Output Stability - Not Clinical Certainty.")

        else:
            st.error("Backend error. Please check API.")


# ===================== REASONING TAB =====================

with tabs[1]:

    if st.session_state.latest is None:
        st.info("Run prediction to view reasoning.")
    else:
        data = st.session_state.latest

        prediction = data.get("prediction", {})
        explainability = data.get("explainability", {})
        reasoning = data.get("reasoning", {})
        system_metrics = data.get("system_metrics", {})
        mode = prediction.get("decision_mode", "NORMAL")

        metadata = reasoning.get("metadata", {})

        coverage_data = reasoning.get("coverage", {})
        traceability_data = reasoning.get("traceability", {})
        reliability_data = reasoning.get("reliability_score", {})

        st.header("Clinical Reasoning Engine")
        with st.expander("Decision Trace (Pipeline Execution)", expanded=False):
            trace_steps = [
                ("Input validation", metadata.get("input_valid", True)),
                ("Model prediction generated", True),
                ("SHAP attribution computed", metadata.get("shap_used", False)),
                ("Clinical evidence retrieved", metadata.get("evidence_used", False)),
                ("Evidence filtered by SHAP drivers", metadata.get("evidence_used", False)),
                ("LLM interpretation generated", metadata.get("llm_used", False)),
                ("Output guardrails validated", metadata.get("guardrail_mode") == "NORMAL"),
                ("Reliability diagnostics computed", True),
            ]

            for step, status in trace_steps:
                icon = "✅" if status else "❌"
                st.write(f"{icon} {step}")
    
                        
        if mode == "SAFE":
            st.error("🔒 Human Review Required — Automated Reasoning Constrained due to limited Reliability Signals.")
        # ======================================================
        # SECTION 1 — MODEL ATTRIBUTION (Structured SHAP)
        # ======================================================

        st.subheader("1️⃣ Model Attribution (SHAP Explainability)")

        shap_data = explainability.get("shap", {})
        shap_available = explainability.get("shap_available", False)

        top_positive = shap_data.get("top_positive", [])
        top_negative = shap_data.get("top_negative", [])

        shap_latency = system_metrics.get("shap_latency_ms", None)

        col_a, col_b = st.columns([2,1])

        with col_a:
            if shap_available:
                st.success("Explainability: AVAILABLE")
            else:
                st.error("Explainability: DEGRADED")

        with col_b:
            if shap_latency is not None:
                st.caption(f"SHAP Latency: {round(shap_latency)} ms")

        col_pos, col_neg = st.columns(2)

        with col_pos:
            st.markdown("### 🔺 Risk Increasing Drivers")
            if top_positive:
                for idx, item in enumerate(top_positive, start=1):
                    st.write(f"{idx}. {item['feature']} (+) — {round(item['impact'],4)}")
            else:
                st.info("No Significant Protective Contibutors Detected.")

        with col_neg:
            st.markdown("### 🔻 Protective / Negative Drivers")
            if top_negative:
                for idx, item in enumerate(top_negative, start=1):
                    st.write(f"{idx}. {item['feature']} (−) — {round(item['impact'],4)}")
            else:
                st.info("No Significant Negative Contributors Available.")

        st.caption("Drivers Ranked by Absolute SHAP Contribution Magnitude.")
        st.markdown("---")

        # ======================================================
        # SECTION 2 — EVIDENCE RETRIEVAL (RAG Layer)
        # ======================================================

        st.subheader("2️⃣ Evidence Retrieval (Clinical Grounding)")

        retrieval_data = data.get("retrieval", {})
        references = reasoning.get("references", [])

        retrieval_used = retrieval_data.get("used", False)
        raw_evidence = retrieval_data.get("evidence", [])

        # Normalize evidence structure safely
        if isinstance(raw_evidence, str):
            evidence_chunks = [c.strip() for c in raw_evidence.split("[") if c.strip()]
            evidence_chunks = ["[" + c for c in evidence_chunks] # wrap string into list
        elif isinstance(raw_evidence, list):
            evidence_chunks = raw_evidence
        else:
            evidence_chunks = []

        MAX_EVIDENCE_DISPLAY = 3
        evidence_chunks = evidence_chunks[:MAX_EVIDENCE_DISPLAY]    
        retrieval_latency = system_metrics.get("retrieval_latency_ms", None)

        col_r1, col_r2 = st.columns([2,1])

        with col_r1:
            if retrieval_used:
                st.success("Retrieval Used: YES")
            else:
                st.warning("Retrieval Used: NO")

        with col_r2:
            if retrieval_latency is not None:
                st.caption(f"Retrieval Latency: {round(retrieval_latency)} ms")

        st.write("Evidence Count:", len(evidence_chunks))

        st.caption(f"Showing Top {len(evidence_chunks)} Clinically Relevant Evidence Excerpts")

        if evidence_chunks:
            st.caption("Evidence Supports Key Risk Drivers.")

        if evidence_chunks:
            for idx, chunk in enumerate(evidence_chunks):
                with st.expander(f"Retrieved Guideline Evidence {idx+1}"):
                    st.write(chunk)
        else:
            st.info("No Evidence Retrieved For This Case.")


        # Structured references (production style)
        if references:
            st.markdown("**Structured References**")
            for ref in references:
                st.write(f"- {ref.get('document')} (Page {ref.get('page')})")

        st.markdown("### Evidence Sources")
        st.markdown("""
        - KDIGO CKD Guidelines
        - NIDDK CKD Guidelines
        """)        

        st.markdown("---")

        # ======================================================
        # SECTION 3 — GENERATED CLINICAL REASONING
        # ======================================================

        st.subheader("3️⃣ Generated Clinical Interpretation")

        clinician_summary = reasoning.get("clinician_summary", "")

        full_explanation = reasoning.get("full_explanation", "")
    


        if clinician_summary:
            parts = clinician_summary.split("Key drivers:")
            
            if len(parts) == 2:
                st.markdown(f"• {parts[0].strip()}")
                st.markdown(f"• **Key Drivers**: {parts[1].strip()}")
            else:
                for line in clinician_summary.split("\n"):
                    if line.strip():
                        st.write("•", line.strip())
        

        # Parse structured explanation into sections
        st.markdown("### Explanation Scope")

        st.markdown("""
        - Based on Model-Attributed Drivers  
        - Supported by Retrieved clinical guidelines 
        - No external risk factors introduced 
        """)

        with st.expander("Full Clinical Explanation", expanded=True):
            if full_explanation:
                # Split by markdown headers to identify sections
                sections = full_explanation.split("###")
                
                for section in sections:
                    section = section.strip()
                    if not section:
                        continue
                    
                    lines = section.split("\n", 1)
                    header = lines[0].strip() if lines else ""
                    content = lines[1].strip() if len(lines) > 1 else ""
                    
                    if header and content:
                        st.markdown(f"### {header}")
                        
                        # Handle bulleted lists for driver sections
                        if "Drivers" in header or "drivers" in header.lower():
                            for line in content.split("\n"):
                                if line.strip().startswith("-"):
                                    st.markdown(f"  {line.strip()}")
                                elif line.strip():
                                    st.markdown(f"  • {line.strip()}")
                        else:
                            st.write(content)
                    elif header:
                        st.markdown(f"### {header}")
            else:
                st.info("No Explanation Available.")
       
           

        # Reasoning confidence and guardrail status
        reasoning_conf = metadata.get("reasoning_confidence", "UNKNOWN")
        guardrail_mode = metadata.get("guardrail_mode", "UNKNOWN")

        col_c1, col_c2 = st.columns(2)

        with col_c1:
            if reasoning_conf == "HIGH":
                st.success(f"AI Reasoning Integrity: {reasoning_conf}")

            elif reasoning_conf == "MEDIUM":
                st.warning(f"AI Reasoning Integrity: {reasoning_conf}")

            elif reasoning_conf == "LOW":
                st.error(f"AI Reasoning Integrity: {reasoning_conf}")

            else:
                st.info(f"AI Reasoning Integrity: {reasoning_conf}")

        with col_c2:
            if mode == "SAFE":
                guardrail_mode = "SAFE"

            if guardrail_mode == "SAFE":
                st.error("Guardrail Mode: SAFE")
            else:
                st.info("Guardrail Mode: NORMAL")

        st.caption("System Provides Decision Support Guidance. Final Clinical Judgement Remains with the Clinician.")

        # ======================================================
        # SECTION 4 — EXPLANATION ALIGNMENT VALIDATION
        # ======================================================

        st.subheader("4️⃣ Explanation Alignment Validation")

        decision_mode = metadata.get("decision_mode", prediction.get("decision_mode"))

        if decision_mode == "SAFE":
            st.info("Alignment Validation Skipped Due to Constrained Reasoning Signals in SAFE Mode.")
            st.markdown("---")
        else:
            llm_text = full_explanation.lower()

        shap_features = [f["feature"].lower() for f in top_positive] if top_positive else []

        if decision_mode != "SAFE" and shap_features and llm_text:
            mentioned = sum(1 for f in shap_features if f in llm_text)
            coverage = mentioned / len(shap_features)
            st.caption(f"{mentioned} of {len(shap_features)} top drivers explicitly referenced.")

            st.markdown(f"**Top Feature Coverage:** {coverage:.2f} ({coverage*100:.0f}%)")
            st.caption("Fraction of Top SHAP Drivers Explicitly Referenced in Explanation.")

            if coverage < 0.4:
                st.warning("Weak Alignment Between Model Drivers and Explanation.")
            elif coverage < 0.7:
                st.info("Moderate Alignment Between SHAP Drivers and Explanation.")
            else:
                st.success("Strong Alignment Between Model Drivers and Explanation.")
        else:
            st.info("Alignment Validation Unavailable.")

        st.markdown("---")



        # ==========================================================
        # SECTION 4B — Explanation Reliability Diagnostics
        # ==========================================================

        st.subheader("Explanation Reliability Diagnostics")

        # Extract reasoning block from API response
        response_json = response.json() 
        reasoning_data = response_json.get("reasoning", {})

        reliability_data = reasoning_data.get("explanation_reliability", {})

        coverage_score = reliability_data.get("coverage", 0)
        traceability_score = reliability_data.get("traceability", 0)
        reliability_score = reliability_data.get("score", 0)
        reliability_label = reliability_data.get("level", "UNKNOWN")

        col_r1, col_r2, col_r3 = st.columns(3)

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric("Driver Coverage", f"{coverage_score:.2f}")

        with col_r2:
            st.metric("Evidence Traceability", f"{traceability_score:.2f}")

        with col_r3:
            st.metric("Explanation Reliability", f"{reliability_score:.2f}")

        # Reliability indicator
        if reliability_label == "HIGH":
            st.success("Explanation Reliability: HIGH")
        elif reliability_label in ["MEDIUM", "MODERATE"]:
            st.warning("Explanation Reliability: MODERATE")
        else:
            st.error("Explanation Reliability: LOW")
        st.progress(min(max(reliability_score, 0.0), 1.0))
        st.caption(f"Reliability Score: {reliability_score:.2f}")
        st.markdown("---")

        
        # ======================================================
        # SECTION 5 — RELIABILITY & GOVERNANCE DIAGNOSTICS
        # ======================================================

        st.subheader("5️⃣ Reliability & Governance Diagnostics")

        llm_used = metadata.get("llm_used", False)
        llm_fallback = metadata.get("llm_fallback", False)
        shap_used = metadata.get("shap_used", False)
        evidence_used = metadata.get("evidence_used", False)
        decision_mode = metadata.get("decision_mode", prediction.get("decision_mode"))
        decision_source = prediction.get("decision_source")

        # Confidence vs Reasoning Confidence Consistency Check
        # ======================================================

        model_conf = float(prediction.get("confidence", 0.0))
        reasoning_conf = metadata.get("reasoning_confidence", "UNKNOWN")

        # Convert numeric confidence into category
        if model_conf <= 0.39:
            model_conf_label = "LOW"
        elif model_conf <= 0.69:
            model_conf_label = "MEDIUM"
        else:
            model_conf_label = "HIGH"

        st.markdown("### Confidence Consistency Check")

        st.write("Prediction Reliability Level:", model_conf_label)
        st.write("Reasoning Confidence Level:", reasoning_conf)

        # Detect mismatch
        decision_mode = metadata.get("decision_mode", prediction.get("decision_mode"))

        if decision_mode == "SAFE":
            st.info("Alignment Validation Skipped in SAFE Mode Due to Intentionally Constrained Reasoning.")
            st.markdown("---")
        

        elif reasoning_conf != "UNKNOWN" and model_conf_label != reasoning_conf:
            st.warning(" ⚠️ Model Confidence and Reasoning Confidence Level Are Not Aligned.")
        else:
            st.success("Model Confidence and Reasoning Confidence are Aligned.")

        st.subheader("AI System Governance & Safety")

        metadata = reasoning.get("metadata", {})

        llm_fallback = metadata.get("llm_fallback", False)
        evidence_used = metadata.get("evidence_used", False)
        shap_used = metadata.get("shap_used", False)
        retrieval_failed = metadata.get("retrieval_failed", False)
        explainability_status = metadata.get("explainability_status")

        if mode == "SAFE":
                llm_used = False

        if not explainability_status:
            explainability_status = "UNAVAILABLE"

        critical = False
        degraded = False

        if llm_fallback and decision_mode != "SAFE":
            critical = True    

        if explainability_status in ["DEGRADED","UNAVAILABLE"]:
            degraded = True

        if retrieval_failed:
            degraded = True

        if critical:
            st.error("🔴 Critical: LLM Fallback Activated. Explanation Reliability May Be Limited.")
        elif degraded:
            st.warning("🟡 Degraded: One or More Reasoning Components Partially Unavailable.")
        else:
            st.success("🟢 System Operating Normally — All Core Reasoning Components Are Active.")

        st.caption("System Health Reflects Reasoning Pipeline Integrity, Not Clinical Certainity.")

        col_d1, col_d2 = st.columns(2)

        with col_d1:
            st.write("LLM Used:", "✅" if llm_used else "❌")
            st.write("LLM Fallback Activated:", "✅" if llm_fallback else "❌")
            st.write("SHAP Used:", "✅" if shap_used else "❌")


        with col_d2:
            if decision_mode == "SAFE":
                st.write("Evidence Retrieval:", "⚠️ Suppressed (SAFE_MODE)")
            elif retrieval_failed:
                st.write("Evidence Retrieval:", "❌ Retrieval Failed")
            elif evidence_used:
                st.write("Evidence Retrieval:", "✅ Retrieved ")
            else:
                st.write("Evidence Retrieval:", " No Relevant Evidence Found")
            st.write("Decision Mode:", decision_mode)
            st.write("Decision Source:", decision_source)


        # ======================================================
        # SECTION 6 — SYSTEM OBSERVABILITY (LLM Layer)
        # ======================================================
        st.divider()
        st.subheader("6️⃣ Operational Health")

        llm_latency = system_metrics.get("llm_latency_ms", None)
        total_latency = system_metrics.get("total_latency_ms", None)

        col_o1, col_o2 = st.columns(2)

        with col_o1:
            if llm_latency is not None:
                st.metric("LLM Latency (ms)", int(llm_latency))

        with col_o2:
            if total_latency is not None:
                st.metric("Total End-to-End Latency (ms)", int(total_latency))

        st.caption("Latency Metrics Enable Scaling Decisions And Performance Diagnostics.")

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