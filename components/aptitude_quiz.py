import streamlit as st
import time
from services.gemini_service import GeminiService

def render(gemini_service: GeminiService):
    """
    Renders the Aptitude & Reasoning Quizzer page for DhanushaBuddy.
    Features dynamic Gemini quiz generation, timer controls, question-by-question navigation,
    and automatic evaluation scorecard details with step-by-step corrections.
    """
    st.markdown(
        '<h1>🧠 Aptitude & <span class="gradient-text">Reasoning Quiz</span></h1>', 
        unsafe_allow_html=True
    )
    st.write(
        "Build analytical, quantitative, and logical capacity. Configure your topic and difficulty, "
        "and get a 5-question Multiple Choice Quiz with dynamic AI explanations."
    )
    st.markdown("---")

    # 1. Topic Topics List
    topics = [
        "Percentage",
        "Profit and Loss",
        "Ratio and Proportion",
        "Time and Work",
        "Time and Distance",
        "Average",
        "Number System",
        "Probability",
        "Permutation & Combination",
        "Logical Reasoning"
    ]

    # Initialize session state for Aptitude Quiz
    if "aptitude_quiz_state" not in st.session_state:
        st.session_state.aptitude_quiz_state = {
            "active": False,
            "category": "",
            "difficulty": "Easy",
            "questions": [],
            "current_index": 0,
            "user_answers": {},  # Maps q_index (0..4) -> string option key (A/B/C/D)
            "submitted": False,
            "start_time": 0.0,
            "time_limit": None,   # Seconds
            "auto_submitted": False
        }

    state = st.session_state.aptitude_quiz_state

    # 2. Config Screen (if quiz not started or finished)
    if not state["active"] and not state["submitted"]:
        st.subheader("Quiz Parameters")
        
        selected_category = st.selectbox("Select Topic Category:", options=topics)
        selected_difficulty = st.selectbox("Select Difficulty Level:", options=["Easy", "Medium", "Hard"])
        
        # Timer Option Configuration
        enable_timer = st.checkbox("Enable Quiz Timer", value=False)
        timer_duration = 10
        if enable_timer:
            timer_duration = st.radio("Timer Duration:", options=[10, 15], format_func=lambda x: f"{x} minutes", horizontal=True)

        if st.button("Generate Quiz with AI", type="primary"):
            with st.spinner("DhanushaBuddy is compiling your quantitative quiz..."):
                questions = gemini_service.generate_aptitude_quiz(selected_category, selected_difficulty)

            # Check generated questions output
            if not questions or (isinstance(questions, list) and len(questions) > 0 and "error" in questions[0]):
                error_msg = questions[0]["error"] if questions else "Failed to generate questions. Please try again."
                st.error(error_msg)
            elif not isinstance(questions, list) or len(questions) != 5:
                st.error("DhanushaBuddy generated an invalid quiz. Please retry.")
            else:
                # Seed the active state
                state["active"] = True
                state["category"] = selected_category
                state["difficulty"] = selected_difficulty
                state["questions"] = questions
                state["current_index"] = 0
                state["user_answers"] = {}
                state["submitted"] = False
                state["auto_submitted"] = False
                
                if enable_timer:
                    state["start_time"] = time.time()
                    state["time_limit"] = timer_duration * 60
                else:
                    state["time_limit"] = None
                
                st.rerun()

    # 3. Active Quiz rendering
    elif state["active"] and not state["submitted"]:
        # Handle Timer Checks if configured
        remaining_str = ""
        if state["time_limit"]:
            elapsed = time.time() - state["start_time"]
            remaining = state["time_limit"] - elapsed
            
            if remaining <= 0:
                # Auto submit the quiz
                state["submitted"] = True
                state["active"] = False
                state["auto_submitted"] = True
                st.rerun()
            else:
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                remaining_str = f"⏳ Time Remaining: **{mins:02d}:{secs:02d}**"
                st.info(remaining_str)

        # Question header
        idx = state["current_index"]
        q_data = state["questions"][idx]

        st.subheader(f"Topic: {state['category']} | Difficulty: {state['difficulty']}")
        
        # Progress Indicator
        st.write(f"Question {idx + 1} of 5")
        st.progress((idx + 1) / 5)

        # Render Question Text inside a Card
        st.markdown(
            f"""
            <div class="glass-card" style="border-left: 5px solid #2563EB; margin-bottom: 1.5rem;">
                <p style="font-size: 1.05rem; font-weight: 500; line-height: 1.5; margin: 0;">
                    {q_data.get('question', '')}
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Render Radio options mapping
        options = q_data.get("options", {})
        options_keys = ["A", "B", "C", "D"]
        radio_choices = [f"{k}) {options.get(k, '')}" for k in options_keys]
        
        # Track active selection pre-selections
        preselected_idx = 0
        current_ans = state["user_answers"].get(idx)
        if current_ans and current_ans in options_keys:
            preselected_idx = options_keys.index(current_ans)

        chosen = st.radio(
            "Select your answer option:",
            options=radio_choices,
            index=preselected_idx,
            key=f"apt_q_{idx}"
        )

        # Record answer PREFIX option
        state["user_answers"][idx] = chosen[0]

        # Action Columns
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if idx > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    state["current_index"] -= 1
                    st.rerun()
        with col2:
            if idx < 4:
                if st.button("Next ➡️", use_container_width=True):
                    state["current_index"] += 1
                    st.rerun()
            else:
                if st.button("Submit Quiz", type="primary", use_container_width=True):
                    state["submitted"] = True
                    state["active"] = False
                    st.rerun()
                    
        with col3:
            if st.button("Exit Quiz", type="secondary"):
                # Reset State
                st.session_state.aptitude_quiz_state = {
                    "active": False,
                    "category": "",
                    "difficulty": "Easy",
                    "questions": [],
                    "current_index": 0,
                    "user_answers": {},
                    "submitted": False,
                    "start_time": 0.0,
                    "time_limit": None,
                    "auto_submitted": False
                }
                st.rerun()

    # 4. Result/Evaluation Screen
    elif state["submitted"]:
        if state["auto_submitted"]:
            st.warning("⏳ Time limit exceeded! Your answers have been auto-submitted.")

        # Calculate Score Metrics
        questions = state["questions"]
        user_answers = state["user_answers"]
        
        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0
        
        for idx, q_data in enumerate(questions):
            ans = user_answers.get(idx)
            correct_key = q_data.get("correct_answer", "").strip()
            
            if not ans:
                unanswered_count += 1
            elif ans == correct_key:
                correct_count += 1
            else:
                incorrect_count += 1
                
        total_questions = len(questions)
        percentage = (correct_count / total_questions) * 100

        st.subheader("Quiz Results Scorecard")

        # Scorecard block metrics
        col_score, col_perc, col_stats = st.columns([1, 1, 2])
        
        with col_score:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-val">{correct_count} / {total_questions}</div>
                    <div class="metric-lbl">Total Score</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col_perc:
            st.markdown(
                f"""
                <div class="metric-box" style="border-left-color: #10B981;">
                    <div class="metric-val">{percentage:.0f}%</div>
                    <div class="metric-lbl">Percentage</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col_stats:
            st.markdown(
                f"""
                <div class="metric-box" style="border-left-color: #6B7280; text-align: left;">
                    <div style="font-size: 0.95rem; font-weight:600; color: #1E3A8A;">🟢 Correct: {correct_count}</div>
                    <div style="font-size: 0.95rem; font-weight:600; color: #EF4444;">🔴 Incorrect: {incorrect_count}</div>
                    <div style="font-size: 0.95rem; font-weight:600; color: #6B7280;">⚪ Unanswered: {unanswered_count}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Detailed Review & Solutions")

        # Review Questions one by one
        for idx, q_data in enumerate(questions):
            ans = user_answers.get(idx, "None")
            correct_key = q_data.get("correct_answer", "").strip()
            
            status_symbol = "⚪ Unanswered"
            card_border_color = "#6B7280"
            if ans != "None":
                if ans == correct_key:
                    status_symbol = "🟢 Correct"
                    card_border_color = "#10B981"
                else:
                    status_symbol = "🔴 Incorrect"
                    card_border_color = "#EF4444"

            options = q_data.get("options", {})
            st.markdown(
                f"""
                <div class="glass-card" style="border-left: 5px solid {card_border_color};">
                    <span style="font-weight: 700; color: {card_border_color};">{status_symbol}</span>
                    <h5 style="margin-top: 0.25rem;">Question {idx + 1}:</h5>
                    <p style="font-size: 1rem; color: #1F2937;">{q_data.get('question', '')}</p>
                    <ul>
                        <li><b>A:</b> {options.get('A', '')}</li>
                        <li><b>B:</b> {options.get('B', '')}</li>
                        <li><b>C:</b> {options.get('C', '')}</li>
                        <li><b>D:</b> {options.get('D', '')}</li>
                    </ul>
                    <p style="margin-bottom: 0.25rem;"><b>Your Answer:</b> {ans} | <b>Correct Answer:</b> {correct_key}</p>
                    <div style="background-color: #F8FAFC; padding: 0.75rem; border-radius: 6px; border: 1px dashed #CBD5E1; margin-top: 0.5rem;">
                        <b>Step-by-step Solution:</b><br>
                        <p style="font-size: 0.95rem; color: #475569; margin: 0;">{q_data.get('explanation', '')}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("Start New Quiz", type="primary"):
            st.session_state.aptitude_quiz_state = {
                "active": False,
                "category": "",
                "difficulty": "Easy",
                "questions": [],
                "current_index": 0,
                "user_answers": {},
                "submitted": False,
                "start_time": 0.0,
                "time_limit": None,
                "auto_submitted": False
            }
            st.rerun()
