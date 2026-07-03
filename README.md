# DhanushaBuddy – AI Placement Preparation Assistant

**DhanushaBuddy** is an AI-powered learning assistant designed to help students prepare for campus placements by providing personalized learning, coding practice, aptitude quizzes, HR interview practice, and AI-based guidance. 

Developed as a **Generative AI Placement Preparation Platform**.

---

## 🚀 Core Features (V1)

1. **🏡 Home Dashboard:** Welcome panel, overview, feature cards, and direct navigation links.
2. **📚 Learn Concepts:** Structured technical learning (Java, Python, SQL, DBMS, OS, Computer Networks, OOP, Aptitude, Logical Reasoning). Uses Gemini to explain concepts with simple language, analogies, examples, key points, and interview tips.
3. **💬 AI Chat:** General placement assistant for career guidance, debugging assistance, and interview advice.
4. **💻 Coding Practice:** Write and execute Python and Java code for Easy, Medium, and Hard placement interview challenges with optimization feedback.
5. **🧠 Aptitude Quiz:** Generates dynamic quizzes (Percentage, Profit and Loss, Time & Work, Time & Distance, Ratio, Probability, Number System, Logical Reasoning) with 5 MCQs and step-by-step explanations.
6. **💼 HR Mock Interview:** Interactive behavioral interviewer asking questions one-by-one (Self Intro, Strengths, Weaknesses, Projects, Teamwork, Leadership, Goals) with feedback scorecard evaluations.

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
│   ├── coding_practice.py   # Hands-on programming practice
│   └── hr_interview.py      # Conversational HR simulator
├── services/
│   ├── __init__.py
│   └── gemini_service.py    # Google-GenAI SDK Client integration wrapper
├── utils/
│   ├── __init__.py
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
   Configure the required environment variable (`GEMINI_API_KEY`) before running the application. Ensure you load this securely via a local `.env` file (see `.env.example`) or your system's environment manager.

4. **Launch application locally:**
   ```bash
   streamlit run app.py
   ```
