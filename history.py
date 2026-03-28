"""
history.py
----------
Shows the logged-in user's saved prediction history
and health metrics fetched from SQLite.
"""

import pandas as pd
import streamlit as st
from auth import get_current_user
from database import get_predictions, get_metrics


def render_history_page():
    st.markdown('<p style="font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:#606060;">Your Records</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size:1.7rem;font-weight:400;margin-bottom:1.5rem;">Prediction History</h2>', unsafe_allow_html=True)

    user = get_current_user()
    if not user:
        st.warning("Please log in to view your history.")
        return

    history = get_predictions(user["id"])

    if not history:
        st.markdown("""
        <div style="background:#1C1C1C;border:1px solid rgba(255,255,255,.08);
                    border-radius:16px;padding:3rem;text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:.75rem;">📋</div>
            <div style="color:#A0A0A0;">No predictions yet.
                Run a <strong>Symptom Analysis</strong> to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Summary row
    risk_scores = [r["risk_score"] for r in history if r.get("risk_score")]
    avg_risk    = sum(risk_scores) / len(risk_scores) if risk_scores else 0
    c1, c2, c3  = st.columns(3)
    c1.metric("Total Predictions", len(history))
    c2.metric("Avg Risk Score",    f"{avg_risk * 100:.1f}%")
    c3.metric("Latest Condition",  history[0]["disease"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Each prediction as an expander
    for record in history:
        risk_val = record.get("risk_score") or 0
        date_str = str(record["created_at"])[:10]
        symptoms = record.get("symptoms", [])

        with st.expander(f"🔬 {record['disease']}  ·  {date_str}", expanded=False):
            col1, col2, col3 = st.columns(3)
            col1.metric("Confidence",  f"{record['confidence']:.1f}%")
            col2.metric("Risk Score",  f"{risk_val * 100:.1f}%")
            col3.metric("Risk Level",  record.get("risk_level", "—"))

            if symptoms:
                chips = "".join(
                    f'<span style="background:rgba(74,158,255,.1);border:1px solid rgba(74,158,255,.25);'
                    f'color:#4A9EFF;border-radius:100px;padding:3px 12px;font-size:.78rem;'
                    f'margin:.2rem;display:inline-block;">{s}</span>'
                    for s in symptoms
                )
                st.markdown(f'<div style="margin-top:.5rem;">{chips}</div>', unsafe_allow_html=True)

    # Health metrics table
    st.markdown("---")
    st.markdown("##### 📊 Health Metrics Over Time")
    metrics = get_metrics(user["id"])
    if metrics:
        df = pd.DataFrame(metrics)[["recorded_at", "bmi", "temperature", "symptom_count", "risk_score"]]
        df["recorded_at"] = pd.to_datetime(df["recorded_at"]).dt.strftime("%b %d, %Y")
        df["risk_score"]  = (df["risk_score"] * 100).round(1).astype(str) + "%"
        df.columns        = ["Date", "BMI", "Temp (°C)", "Symptoms", "Risk"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Health metrics will appear here after your first Symptom Analysis.")
