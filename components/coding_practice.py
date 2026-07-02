import streamlit as st
from services.gemini_service import GeminiService

def render(gemini_service: GeminiService):
    """
    Renders the Coding Practice module for DhanushaBuddy.
    Allows selection of Java/Python, difficulty levels, dynamic problem generation,
    and structured code evaluations using Gemini.
    """
    st.markdown(
        '<h1>💻 Coding <span class="gradient-text">Practice</span></h1>', 
        unsafe_allow_html=True
    )
    st.write(
        "Ace your coding interview rounds. Generate algorithmic and data structure problems, "
        "write your solution, and get instantaneous feedback on optimization, complexity, and cleanliness."
    )
    st.markdown("---")

    # Initialize coding practice session states
    if "coding_state" not in st.session_state:
        st.session_state.coding_state = {
            "problem": None,
            "evaluation": None,
            "language": "Python",
            "difficulty": "Easy"
        }

    state = st.session_state.coding_state

    # 1. Config form (if no active problem is loaded)
    if state["problem"] is None:
        st.subheader("Select Challenge Options")
        
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Programming Language:", options=["Python", "Java"])
        with col2:
            diff = st.selectbox("Difficulty Level:", options=["Easy", "Medium", "Hard"])

        if st.button("Generate Coding Challenge", type="primary"):
            with st.spinner("DhanushaBuddy is compiling a fresh problem for you..."):
                problem = gemini_service.generate_coding_problem(lang, diff)
                
            if "error" in problem:
                st.error(problem["error"])
                if "raw_text" in problem and problem["raw_text"]:
                    st.code(problem["raw_text"])
            else:
                state["problem"] = problem
                state["language"] = lang
                state["difficulty"] = diff
                state["evaluation"] = None
                st.rerun()
    else:
        # Active problem is loaded!
        problem = state["problem"]
        lang = state["language"]
        diff = state["difficulty"]

        # Header card displaying title and metadata
        st.markdown(
            f"""
            <div class="glass-card" style="border-left: 5px solid #2563EB; margin-bottom: 1.5rem;">
                <span class="badge-blue">{lang.upper()} | {diff.upper()}</span>
                <h3 style="margin-top: 0.5rem; color: #1E3A8A;">{problem.get('title', 'Coding Challenge')}</h3>
                <p style="font-size: 1rem; line-height: 1.6; color: #334155; margin-bottom: 0;">
                    <b>Problem Statement:</b><br>{problem.get('problem_statement', '')}
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Inputs and Constraints columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Sample Input:**")
            st.code(problem.get("sample_input", "N/A"), language="text")
        with col2:
            st.markdown("**Sample Output:**")
            st.code(problem.get("sample_output", "N/A"), language="text")

        st.markdown(f"*Constraints:* `{problem.get('constraints', 'None specified.')}`")
        
        # Hints Accordion
        with st.expander("💡 Need a hint?"):
            st.write(problem.get("hint", "Try breaking down the problem into smaller sub-tasks."))

        st.markdown("---")

        # Starter templates
        starter_code = ""
        if lang == "Python":
            starter_code = "def solve(input_val):\n    # Write your Python solution here\n    pass\n"
        elif lang == "Java":
            starter_code = "import java.util.*;\n\npublic class Solution {\n    public static void solve() {\n        // Write your Java solution here\n    }\n}\n"

        # Code paste block
        st.subheader(f"Submit your {lang} Solution")
        user_code = st.text_area(
            "Paste your solution code block below:",
            value=starter_code,
            height=280,
            help="Ensure your solution is written in the chosen language."
        )

        # Action Buttons
        btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 4])
        
        with btn_col1:
            if st.button("Evaluate Code", type="primary", use_container_width=True):
                if not user_code.strip() or user_code == starter_code:
                    st.warning("Please enter your solution before evaluating.")
                else:
                    with st.spinner("AI Evaluator is validating and grading your logic..."):
                        evaluation = gemini_service.evaluate_coding_solution(problem, lang, user_code)
                    
                    if "error" in evaluation:
                        st.error(evaluation["error"])
                        if "raw_text" in evaluation and evaluation["raw_text"]:
                            st.code(evaluation["raw_text"])
                    else:
                        state["evaluation"] = evaluation
                        st.rerun()
                        
        with btn_col2:
            if st.button("Change Topic/Diff", type="secondary", use_container_width=True):
                state["problem"] = None
                state["evaluation"] = None
                st.rerun()

        # Display Evaluation results
        if state["evaluation"]:
            eval_report = state["evaluation"]
            st.markdown("---")
            st.markdown("<h3>📊 Code Evaluation <span class=\"gradient-text\">Report</span></h3>", unsafe_allow_html=True)

            # 1. Correctness Card
            st.markdown(
                f"""
                <div class="glass-card" style="border-left: 5px solid #10B981;">
                    <h5 style="color: #065F46;">✅ 1. Correctness & Execution</h5>
                    <p style="margin: 0; font-size: 0.95rem;">{eval_report.get('correctness', 'No evaluation details.')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

            # 2. Logic Card
            st.markdown(
                f"""
                <div class="glass-card" style="border-left: 5px solid #3B82F6;">
                    <h5 style="color: #1E3A8A;">⚙️ 2. Algorithmic Logic</h5>
                    <p style="margin: 0; font-size: 0.95rem;">{eval_report.get('logic', 'No logic details.')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

            # 3. Code Quality Card
            st.markdown(
                f"""
                <div class="glass-card" style="border-left: 5px solid #8B5CF6;">
                    <h5 style="color: #5B21B6;">✨ 3. Code Style & Cleanliness</h5>
                    <p style="margin: 0; font-size: 0.95rem;">{eval_report.get('quality', 'No code style details.')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

            # Complexity Indicators
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-val" style="font-size: 1.8rem;">{eval_report.get('time_complexity', 'O(N)')}</div>
                        <div class="metric-lbl">Time Complexity</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with comp_col2:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-val" style="font-size: 1.8rem;">{eval_report.get('space_complexity', 'O(1)')}</div>
                        <div class="metric-lbl">Space Complexity</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Suggestions Card
            st.markdown(
                """
                <div class="glass-card" style="border-left: 5px solid #F59E0B;">
                    <h5 style="color: #92400E;">📝 Suggestions for Improvements</h5>
                </div>
                """, 
                unsafe_allow_html=True
            )
            suggestions = eval_report.get('suggestions', [])
            if suggestions:
                for s in suggestions:
                    st.write(f"- {s}")
            else:
                st.write("Your solution looks optimal! Excellent work.")
