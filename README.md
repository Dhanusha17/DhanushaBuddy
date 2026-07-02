# DhanushaBuddy – AI Placement Preparation Assistant

**DhanushaBuddy** is an AI-powered learning assistant designed to help students prepare for campus placements by providing personalized learning, coding practice, aptitude quizzes, HR interview practice, and AI-based guidance. 

Developed as a Generative AI Capstone project for **Infosys Pragati Cohort 9**.

---

## 🚀 Core Features (V1)

1. **🏡 Home Dashboard:** Welcome panel, overview, feature cards, and direct navigation links.
2. **📚 Learn Concepts:** Structured technical learning (Java, Python, SQL, DBMS, OS, Computer Networks, OOP, Aptitude, Logical Reasoning). Uses Gemini to explain concepts with simple language, analogies, examples, key points, and interview tips.
3. **💬 AI Chat:** General placement assistant for career guidance, debugging assistance, and interview advice.
4. **🧠 Aptitude Quiz:** Generates dynamic quizzes (Percentage, Profit and Loss, Time & Work, Time & Distance, Ratio, Probability, Number System, Logical Reasoning) with 5 MCQs and step-by-step explanations.
5. **💼 HR Mock Interview:** Interactive behavioral interviewer asking questions one-by-one (Self Intro, Strengths, Weaknesses, Projects, Teamwork, Leadership, Goals) with feedback scorecard evaluations.

---

## 🛠️ Tech Stack & Architecture

- **App Framework:** Streamlit
- **AI Service:** Google Gemini API (`google-genai` SDK)
- **Styling:** Custom CSS stylesheet with a modern dark-slate theme and glassmorphic card designs
- **Database:** None (V1 stores local session states)

---

## 📦 Directory Structure

```text
placement_prep_buddy/
├── .streamlit/
│   └── config.toml          # Custom theme settings
├── assets/
│   └── style.css            # Custom CSS styles (glassmorphic cards, gradient text)
├── components/
│   ├── __init__.py
│   ├── home.py              # Main landing module
│   ├── learn_concepts.py    # Language & technical subject tutoring
│   ├── ai_chat.py           # General Q&A placement chat
│   ├── aptitude_quiz.py     # Quantitative & reasoning quizzes
│   └── hr_interview.py      # Conversational HR simulator
├── utils/
│   ├── __init__.py
│   ├── gemini_helper.py     # Google-GenAI SDK Client integration wrapper
│   └── prompts.py           # Standard prompt templates & system instructions
├── .env.example             # Example environment file
├── requirements.txt         # Project package requirements
├── app.py                   # Streamlit application routing main entrance
└── README.md                # Project documentation
```

---

## ⚙️ Development Setup

1. **Move into the project folder:**
   ```bash
   cd C:\Users\admin\.gemini\antigravity\scratch\placement_prep_buddy
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   Copy `.env.example` to `.env` and fill in your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Launch application locally:**
   ```bash
   streamlit run app.py
   ```
