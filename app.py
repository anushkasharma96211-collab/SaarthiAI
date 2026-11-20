import json
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="SaarthiAI | AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# 2. Custom Dark Theme matching SaarthiAI Pitch Deck
st.markdown("""
<style>
    .stApp {
        background-color: #0B132B;
        color: #FFFFFF;
    }
    .card {
        background-color: #16213E;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #38BDF8;
        margin-bottom: 16px;
    }
    .mistake-card {
        background-color: #1E1B2E;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #F87171;
        margin-bottom: 14px;
    }
    .feedback-card {
        background-color: #16213E;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #34D399;
        margin-bottom: 16px;
    }
    .tag {
        background-color: #1E293B;
        color: #38BDF8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
for key, default in {
    "question": "",
    "evaluation": None,
    "prev_scores": None,
    "attempt": 1,
    "chat_history": [],
    "role_skills": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# 4. Browser Voice Output (AI Interviewer speaks aloud)
def speak_text(text):
    clean_text = text.replace('"', '\\"').replace("\n", " ")
    components.html(
        f"""
        <script>
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.rate = 1.0;
            window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )

# 5. Sidebar: Step 1 (Choose Your Goal - Slide 4)
with st.sidebar:
    st.markdown("### 🎯 Step 1: Choose Your Goal")
    api_key = st.text_input("Gemini API Key (Optional for Live AI)", type="password")
    
    course = st.selectbox(
        "Stream / Course",
        ["B.Tech / Engineering", "Diploma / Polytechnic", "BBA / MBA / Management", "B.Sc / BCA / IT", "Arts / Commerce"]
    )
    role = st.text_input("Target Role / Subject", value="Software Developer Intern")
    language = st.selectbox(
        "Comfortable Language",
        ["English", "Hinglish (Hindi + English)", "Hindi (हिंदी)"]
    )
    jd = st.text_area(
        "Paste Job Description or Key Skills",
        placeholder="e.g., Troubleshooting, Python, communication, teamwork, safety awareness..."
    )
    
    st.markdown("---")
    st.markdown("### 🎥 Practice Modes")
    read_aloud = st.toggle("🔊 AI Voice Question Read-Aloud", value=True)
    enable_video = st.toggle("📹 Video Confidence & Posture Cam", value=True)
    
    st.markdown("---")
    st.caption("Built by Team Agentic4 • ABES Engineering College, Ghaziabad")

# 6. Header (Slide 1)
st.markdown('<span class="tag">AI-POWERED CAREER READINESS • CHAT • AUDIO • VIDEO</span>', unsafe_allow_html=True)
st.title("SaarthiAI")
st.subheader("Turn skills into interview confidence.")
st.write("A personalised AI interview coach for every student — across streams, careers, and comfortable languages.")
st.markdown("---")

# 7. Agent 1: Role Analyzer & Adaptive Question Generator (Slide 4 Steps 2 & 3)
def analyze_and_generate(course, role, language, jd, api_key):
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"""
            You are SaarthiAI, a supportive, realistic AI interview coach for Indian students.
            Course: {course}
            Target Role: {role}
            Preferred Language: {language}
            Job Description / Skills: {jd}

            1. Identify 3 core skills expected for this role.
            2. Generate ONE practical, scenario-based interview question strictly in {language}.
            
            Respond ONLY in valid JSON:
            {{
                "skills": ["Skill 1", "Skill 2", "Skill 3"],
                "question": "The interview question in {language}"
            }}
            """
            response = model.generate_content(prompt)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            st.warning(f"Using offline demo mode: {e}")

    # Offline fallback matching Slide 6 & Role context
    fallbacks = {
        "English": f"As a {role}, suppose a critical system or machine keeps stopping unexpectedly right before delivery. How would you begin troubleshooting safely and explain it to your team?",
        "Hinglish (Hindi + English)": f"Maan lijiye aap {role} ke role par kaam kar rahe hain aur delivery se theek pehle ek critical system baar-baar ruk raha hai. Aap safely troubleshooting kaise shuru karenge aur team ko kaise explain karenge?",
        "Hindi (हिंदी)": f"मान लीजिए आप {role} के रूप में काम कर रहे हैं और डिलीवरी से ठीक पहले एक ज़रूरी सिस्टम बार-बार रुक रहा है। आप सुरक्षित रूप से समस्या को कैसे सुलझाएंगे?"
    }
    return {
        "skills": ["Structured Troubleshooting", "Clear Communication", "Safety & Root-Cause Analysis"],
        "question": fallbacks.get(language, fallbacks["English"])
    }

# 8. Agent 2: Mistake Analyzer, Coach & Readiness Evaluator (Slide 4 Steps 4 & 5 + Slide 6)
def evaluate_and_coach(question, text_ans, role, language, api_key, audio_bytes=None, image_bytes=None, attempt=1):
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"""
            You are SaarthiAI, an encouraging AI interview mentor. Analyze the student's attempt #{attempt} in {language}.
            Target Role: {role}
            Question: {question}
            Student Text Answer: {text_ans}
            Audio Provided: {"Yes (analyze tone, clarity, and spoken content)" if audio_bytes else "No"}
            Video Frame Provided: {"Yes (also give 1 brief tip on posture/eye contact)" if image_bytes else "No"}

            Identify exact mistakes or missing points in the student's answer, show how to fix them, give a stronger sample answer in {language}, and score out of 10.
            Respond ONLY in valid JSON:
            {{
                "mistakes": ["Specific mistake 1", "Specific mistake 2"],
                "feedback": "Encouraging, actionable feedback explaining what was good and how to improve",
                "sample_answer": "A stronger, well-structured sample answer in {language}",
                "communication": 7,
                "role_knowledge": 7,
                "problem_solving": 8,
                "confidence": 7,
                "seven_day_plan": "Focused 7-day improvement action plan"
            }}
            """
            content = [prompt]
            if audio_bytes:
                content.append({"mime_type": "audio/wav", "data": audio_bytes})
            if image_bytes:
                content.append({"mime_type": "image/jpeg", "data": image_bytes})
            response = model.generate_content(content)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            st.warning(f"Using smart offline coach: {e}")

    # Smart Offline Mistake & Improvement Analyzer (matches Slide 6 + Attempt progression)
    words = text_ans.strip().split()
    word_count = max(len(words), 16 if audio_bytes else 0)
    boost = (attempt - 1) * 1  # Rewards retry improvement
    base = min(9, max(5, (word_count // 4) + boost))

    mistakes = []
    if word_count < 15:
        mistakes.append("Answer is too brief — lacks step-by-step reasoning and context.")
    if "first" not in text_ans.lower() and "step" not in text_ans.lower() and "pehle" not in text_ans.lower():
        mistakes.append("Missed explaining the safe first step or initial diagnostic check before jumping to a fix.")
    if "why" not in text_ans.lower() and "because" not in text_ans.lower() and "kyunki" not in text_ans.lower():
        mistakes.append("Did not explain WHY you chose that action or how you verified the root cause.")
    if not mistakes:
        mistakes.append("Good structure! Add measurable impact or how you communicate status to stakeholders.")

    return {
        "mistakes": mistakes,
        "feedback": "Good start! Make your answer stronger: explain the safe first step, the exact diagnostic checks you would perform, and why — then try again." if language == "English" else "Achhi shuruat hai! Apne answer ko aur strong banane ke liye pehle safe step, diagnostic checks aur unka reason explain karein — aur phir retry karein.",
        "sample_answer": "First, I would ensure safety and isolate the system so no data or hardware is damaged. Next, I would check error logs and recent changes to identify the root cause rather than guessing. Finally, I would test the fix and update my team lead with clear timelines.",
        "communication": base,
        "role_knowledge": min(10, base + 1),
        "problem_solving": min(10, base + 1),
        "confidence": min(10, base + (1 if image_bytes or audio_bytes else 0)),
        "seven_day_plan": "Day 1-2: Practice STAR structure • Day 3-4: Record 2 voice answers daily • Day 5-7: Retry role-specific troubleshooting scenarios."
    }

# 9. Main Layout
col_left, col_right = st.columns([1.4, 1])

with col_left:
    st.markdown("### 🎙️ Step 2 & 3: Understand Role & Start Interview")
    if st.button("✨ Analyze Role & Generate Interview Question", use_container_width=True):
        data = analyze_and_generate(course, role, language, jd, api_key)
        st.session_state.role_skills = data["skills"]