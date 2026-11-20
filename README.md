# SaarthiAI — Turn Skills into Interview Confidence 🎯

**SaarthiAI** is a personalized, multilingual AI interview coach built by **Team Agentic4** for **PromptWars x AgentX 2.0**. It helps students across all academic streams practice interviews privately via **Chat, Audio (Voice), and Video**, detects exact mistakes in their answers, and guides them through iterative retries to build real confidence.

---

## 🚀 Key Features
- **Role & Skill Analyzer:** Tailors scenario-based interview questions to the student's academic stream, target role, or pasted job description.
- **Comfortable Languages:** Supports **English**, **Hinglish (Hindi + English)**, and **Hindi (हिंदी)** so language is never a barrier.
- **Multi-Modal Practice (Chat • Audio • Video):**
  - **Chat Mode:** Interactive text practice with full session transcript history.
  - **Audio Mode:** Native microphone voice recording (`st.audio_input`) + AI voice question read-aloud.
  - **Video Practice Mode:** Live camera preview (`st.camera_input`) for posture, eye contact, and confidence feedback.
- **Mistake Analysis & Retry Loop:** Highlights exact gaps/mistakes in each response, provides a stronger sample answer, and tracks score improvements across retries.
- **Readiness Snapshot & 7-Day Plan:** Evaluates **Communication**, **Role Knowledge**, **Problem Solving**, and **Confidence** out of 10 with a personalized 7-day improvement plan.

---

## 🛠️ Tech Stack & Agentic Workflow
- **Frontend & Multi-Modal UI:** Python, Streamlit
- **AI Engine:** Google Gemini (`gemini-2.5-flash`) with a multi-step agentic pipeline:
  1. **Role Analyzer Agent** (extracts role expectations & key skills)
  2. **Multilingual Interviewer Agent** (generates adaptive questions + voice read-aloud)
  3. **Mistake Evaluator & Readiness Coach Agent** (analyzes text/audio/video responses, flags mistakes, and tracks retry deltas)

---

## ⚙️ How to Run Locally
```bash
git clone https://github.com<your-username>/SaarthiAI.git
cd SaarthiAI
pip install -r requirements.txt
streamlit run app.py
```

---

## 👥 Team Agentic4 (ABES Engineering College, Ghaziabad)
- **Anuj Yadav**
- **Anurag**
- **Anushka Sharma**
- **Anshika Tripathi**
-