# ⚕️ MediScan AI — Clinical Intelligence Platform

AI-powered healthcare app for disease prediction, medicine recommendations, personalised nutrition plans, and daily routine generation.

---

## 🚀 How to Run (3 steps)

**Step 1 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2 — Add your CSV datasets to the `data/` folder**
```
data/
├── Testing.csv
├── Final_Augmented_dataset_Diseases_and_Symptoms.csv
├── Symptom-severity.csv
├── medical data.csv
└── drugsComTest_raw.csv
```

**Step 3 — Train the model (run once)**
```bash
python train_models.py
```

**Step 4 — Launch the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
MediScan_AI/
│
├── app.py               ← Main Streamlit app (all pages)
├── auth.py              ← Login, register, session management
├── database.py          ← SQLite — users, predictions, metrics, profiles
├── history.py           ← Prediction history page
├── profile.py           ← Patient profile settings page
├── train_models.py      ← Run once to train the ML model
├── requirements.txt
│
├── utils/               ← Core ML + recommendation logic (unchanged)
│   ├── prediction.py
│   ├── preprocessing.py
│   ├── medicine_recommender.py
│   ├── diet_planner.py
│   ├── routine_generator.py
│   └── analytics.py
│
├── data/                ← Place your CSV datasets here
└── models/              ← Auto-generated after running train_models.py
```

---

## ✨ Features

- 🔒 **User Authentication** — Sign up / Sign in with secure password hashing (SQLite)
- 🔬 **Symptom Analysis** — AI disease prediction with confidence scores (130+ symptoms, 40+ diseases)
- 💊 **Medications** — OTC, prescription, natural remedies, dosage, and contraindications
- 🥗 **Nutrition Plan** — Personalised 7-day meal plan with recipes and exercise suggestions
- 🗓️ **Daily Routine** — Hour-by-hour schedule with medication timing and rest periods
- 📊 **Health Analytics** — BMI, temperature trends, symptom frequency charts
- 📋 **Clinical Report** — Full patient summary with downloadable `.txt` report
- 🕑 **History** — All past predictions saved and viewable (persists across sessions)
- 👤 **Profile** — Save your health profile to pre-fill forms automatically

---

## ⚠️ Disclaimer

This tool is for **educational and informational purposes only**. It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.
