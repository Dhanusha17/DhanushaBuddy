import streamlit as st

def render(gemini_service):
    """
    Renders the HR Mock Interview module for DhanushaBuddy.
    Features a structured, question-by-question interview flow for behavioral evaluation using Gemini AI.
    """
    st.markdown(
        '<h1>💼 HR <span class="gradient-text">Mock Interview</span></h1>', 
        unsafe_allow_html=True
    )
    st.write(
        "Prepare for behavioral rounds by practicing standard HR topics. "
        "The AI interviewer will ask questions one-by-one, evaluate your answers, and provide suggestions."
    )
    
    st.markdown("---")
    
    # Initialize session state for HR Mock Interview
    if "hr_state" not in st.session_state:
        st.session_state.hr_state = {
            "active": False,
            "completed": False,
            "category": "",
            "difficulty": "",
            "total_questions": 5,
            "current_question_number": 0,
            "current_question_text": "",
            "messages": [],
            "evaluations": [],
            "report": None
        }
        
    state = st.session_state.hr_state
    
    # Configuration / Setup Phase
    if not state["active"] and not state["completed"]:
        st.subheader("Start HR Interview Prep")
        st.write("Configure your mock interview session. The AI will ask you 5 questions.")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Interview Category:",
                options=[
                    "Fresher Interview",
                    "Technical HR",
                    "Behavioral Interview",
                    "Leadership & Teamwork",
                    "Conflict Resolution"
                ]
            )
        with col2:
            difficulty = st.selectbox(
                "Difficulty Level:",
                options=["Beginner", "Intermediate", "Advanced"]
            )
            
        if st.button("Begin Mock Interview", type="primary"):
            with st.spinner("Preparing your interview..."):
                response = gemini_service.setup_hr_interview(category, difficulty)
                
                if "error" in response:
                    st.error(response["error"])
                else:
                    first_q = response.get("question", "Tell me about yourself.")
                    
                    state["active"] = True
                    state["category"] = category
                    state["difficulty"] = difficulty
                    state["current_question_number"] = 1
                    state["current_question_text"] = first_q
                    
                    welcome_msg = f"Hello! Welcome to your {difficulty} {category} mock interview. Let's begin.\n\n**{first_q}**"
                    state["messages"] = [{"role": "assistant", "content": welcome_msg}]
                    
                    st.rerun()
                    
    # Active Interview Phase
    elif state["active"] and not state["completed"]:
        st.subheader(f"Question {state['current_question_number']} of {state['total_questions']}")
        st.progress(state["current_question_number"] / state["total_questions"])
        
        # Display chat history
        for msg in state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Handle user text input
        if answer := st.chat_input("Type your response here..."):
            # Append user answer
            state["messages"].append({"role": "user", "content": answer})
            
            with st.chat_message("user"):
                st.markdown(answer)
                
            with st.chat_message("assistant"):
                with st.spinner("Evaluating response and generating next question..."):
                    # Call Gemini to evaluate and get next question
                    response = gemini_service.evaluate_hr_answer(
                        category=state["category"],
                        difficulty=state["difficulty"],
                        question_number=state["current_question_number"],
                        total_questions=state["total_questions"],
                        question=state["current_question_text"],
                        answer=answer
                    )
                    
                    if "error" in response:
                        st.error(response["error"])
                    else:
                        eval_data = response.get("evaluation", {})
                        next_q = response.get("next_question")
                        
                        # Save evaluation to history for report
                        state["evaluations"].append({
                            "question": state["current_question_text"],
                            "answer": answer,
                            "evaluation": eval_data
                        })
                        
                        # Format feedback message
                        feedback_msg = (
                            f"**Feedback:**\n"
                            f"- **Strengths:** {eval_data.get('strengths', 'N/A')}\n"
                            f"- **Areas for Improvement:** {eval_data.get('areas_for_improvement', 'N/A')}\n"
                            f"- **Tips:** {eval_data.get('tips', 'N/A')}\n"
                            f"- **Confidence Score:** {eval_data.get('confidence_score', 'N/A')}/100 "
                            f"| **Communication Rating:** {eval_data.get('communication_rating', 'N/A')}\n\n"
                            f"**Suggested Better Answer:**\n> {eval_data.get('suggested_better_answer', 'N/A')}\n"
                        )
                        
                        if next_q and state["current_question_number"] < state["total_questions"]:
                            state["current_question_number"] += 1
                            state["current_question_text"] = next_q
                            assistant_msg = f"{feedback_msg}\n---\n**Next Question:**\n{next_q}"
                            state["messages"].append({"role": "assistant", "content": assistant_msg})
                            st.rerun()
                        else:
                            # Interview over, generate report
                            assistant_msg = f"{feedback_msg}\n---\n**That concludes our interview!** Generating your final report..."
                            state["messages"].append({"role": "assistant", "content": assistant_msg})
                            
                            st.markdown(assistant_msg)
                            with st.spinner("Generating Final Report..."):
                                report_response = gemini_service.generate_hr_report(
                                    category=state["category"],
                                    difficulty=state["difficulty"],
                                    history=state["evaluations"]
                                )
                                
                                if "error" in report_response:
                                    st.error(report_response["error"])
                                else:
                                    state["report"] = report_response
                                    state["completed"] = True
                                    state["active"] = False
                                    st.rerun()
                                    
    # Completed Phase
    elif state["completed"]:
        st.subheader("🎉 Mock HR Interview Completed!")
        
        report = state["report"]
        if report:
            st.markdown(
                """
                <div class="glass-card" style="border: 2px solid #4F46E5; margin-bottom: 20px;">
                    <h4 style="text-align: center;">📊 Professional Interview Report</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="metric-box"><div class="metric-val">{report.get("overall_score", "N/A")}</div><div class="metric-lbl">Overall Score</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-box"><div class="metric-val">{report.get("communication_score", "N/A")}</div><div class="metric-lbl">Communication</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-box"><div class="metric-val">{report.get("confidence_score", "N/A")}</div><div class="metric-lbl">Confidence</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-box"><div class="metric-val">{report.get("technical_score", "N/A")}</div><div class="metric-lbl">Technical/Domain</div></div>', unsafe_allow_html=True)
                
            st.markdown("---")
            
            st.markdown(f"**🌟 Strongest Area:** {report.get('strongest_area', 'N/A')}")
            st.markdown(f"**⚠️ Weakest Area:** {report.get('weakest_area', 'N/A')}")
            st.markdown(f"**📈 Placement Readiness:** {report.get('placement_readiness_level', 'N/A')}")
            
            st.info(f"**Final Recommendation:**\n{report.get('final_recommendation', 'N/A')}")
            
            st.markdown("---")
            st.subheader("Detailed History")
            for i, eval_item in enumerate(state["evaluations"]):
                with st.expander(f"Question {i+1}"):
                    st.write(f"**Q:** {eval_item['question']}")
                    st.write(f"**Your Answer:** {eval_item['answer']}")
                    st.write("**Evaluation:**")
                    eval_data = eval_item.get('evaluation', {})
                    st.write(f"- **Strengths:** {eval_data.get('strengths', 'N/A')}")
                    st.write(f"- **Areas for Improvement:** {eval_data.get('areas_for_improvement', 'N/A')}")
                    st.write(f"- **Tips:** {eval_data.get('tips', 'N/A')}")
        else:
            st.error("Report could not be generated.")
            
        if st.button("Start New Mock Interview", type="primary"):
            st.session_state.hr_state = {
                "active": False,
                "completed": False,
                "category": "",
                "difficulty": "",
                "total_questions": 5,
                "current_question_number": 0,
                "current_question_text": "",
                "messages": [],
                "evaluations": [],
                "report": None
            }
            st.rerun()
