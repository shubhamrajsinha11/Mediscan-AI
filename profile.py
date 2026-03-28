"""
profile.py
----------
Lets the logged-in user view and update their patient profile.
"""

import streamlit as st
from auth import get_current_user
from database import get_profile, save_profile


def render_profile_page():
    st.markdown('<p style="font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:#606060;">Account</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size:1.7rem;font-weight:400;margin-bottom:1.5rem;">Patient Profile</h2>', unsafe_allow_html=True)

    user = get_current_user()
    if not user:
        st.warning("Please log in to view your profile.")
        return

    # Read-only account info
    st.markdown("##### 👤 Account Information")
    c1, c2, c3 = st.columns(3)
    c1.metric("Username",     user["username"])
    c2.metric("Email",        user["email"])
    c3.metric("Member Since", str(user.get("created_at", ""))[:10])

    st.markdown("---")
    st.markdown("##### 🏥 Health Profile")
    st.caption("This pre-fills your Symptom Analysis forms automatically.")

    profile = get_profile(user["id"]) or {}

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            age         = st.number_input("Age",         min_value=1,   max_value=120,   value=int(profile.get("age") or 25))
            weight_kg   = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=float(profile.get("weight_kg") or 70.0))
            blood_opts  = ["", "A+", "A−", "B+", "B−", "AB+", "AB−", "O+", "O−"]
            blood_group = st.selectbox("Blood Group", blood_opts,
                            index=blood_opts.index(profile.get("blood_group", "")) if profile.get("blood_group") in blood_opts else 0)
        with col2:
            gender_opts = ["Male", "Female", "Other"]
            gender      = st.selectbox("Gender", gender_opts,
                            index=gender_opts.index(profile.get("gender", "Male")) if profile.get("gender") in gender_opts else 0)
            height_cm   = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=float(profile.get("height_cm") or 170.0))

        saved = st.form_submit_button("💾 Save Profile", use_container_width=True)

    if saved:
        try:
            save_profile(user["id"], age, gender, weight_kg, height_cm, blood_group)
            st.success("✅ Profile saved successfully!")
            if "patient_data" in st.session_state:
                st.session_state["patient_data"].update({
                    "age": age, "gender": gender,
                    "weight": weight_kg, "height": height_cm
                })
        except Exception as e:
            st.error(f"❌ Could not save: {e}")

    # BMI preview
    if profile.get("weight_kg") and profile.get("height_cm"):
        bmi = profile["weight_kg"] / ((profile["height_cm"] / 100) ** 2)
        st.markdown("---")
        b1, b2 = st.columns(2)
        b1.metric("Your BMI",  f"{bmi:.1f}")
        b2.metric("Category",  _bmi_cat(bmi))


def _bmi_cat(bmi):
    if bmi < 18.5: return "Underweight"
    if bmi < 25.0: return "Normal"
    if bmi < 30.0: return "Overweight"
    return "Obese"
