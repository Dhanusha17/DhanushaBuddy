import streamlit as st

def render(*args, **kwargs):
    """
    Renders the Home page of the DhanushaBuddy AI Placement Preparation Assistant.
    """
    # 1. Hero / Professional Banner Section
    st.markdown(
        """
        <div class="hero-banner">
            <span class="badge-blue" style="background-color: rgba(255,255,255,0.2); color: white;">Infosys Pragati Cohort 9 Capstone</span>
            <h1 style="font-size: 2.75rem; font-weight: 800; margin-bottom: 0.5rem; color: white;">🎯 DhanushaBuddy</h1>
            <p style="font-size: 1.25rem; font-weight: 400; opacity: 0.95; margin-bottom: 1.5rem; color: white;">
                Your Personal AI Placement Preparation Assistant
            </p>
            <p style="font-size: 1.05rem; line-height: 1.6; max-width: 800px; color: white;">
                DhanushaBuddy is an advanced Generative AI-powered learning companion engineered to empower college students, 
                final-year graduates, and job seekers. Practice coding, learn technical concepts, solve quantitative 
                aptitude questions, and polish your soft skills with automated behavioral feedback.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Statistics Section
    st.subheader("Placement Insights & Benchmarks")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.markdown(
            '<div class="metric-box"><div class="metric-val">85%+</div><div class="metric-lbl">Recruiter Match</div></div>',
            unsafe_allow_html=True
        )
    with stat_col2:
        st.markdown(
            '<div class="metric-box"><div class="metric-val">10+</div><div class="metric-lbl">Core Subjects</div></div>',
            unsafe_allow_html=True
        )
    with stat_col3:
        st.markdown(
            '<div class="metric-box"><div class="metric-val">500+</div><div class="metric-lbl">Aptitude Qs</div></div>',
            unsafe_allow_html=True
        )
    with stat_col4:
        st.markdown(
            '<div class="metric-box"><div class="metric-val">24/7</div><div class="metric-lbl">AI Tutoring</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Core Features Cards Grid
    st.subheader("Explore Preparation Modules")
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown(
            """
            <div class="glass-card">
                <span class="badge-blue">TUTORIALS</span>
                <h4>📚 Learn Concepts</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5;">
                    Master Java, Python, SQL, DBMS, OS, Networks, OOP, Data Structures, and Reasoning. 
                    Gemini AI generates definitions, real-life analogies, clean code blocks, interview tips, and common pitfalls.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="glass-card">
                <span class="badge-blue">QUANTITATIVE</span>
                <h4>🧠 Aptitude Quiz</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5;">
                    Practice Percentage, Ratio, Profit & Loss, Time & Work, Time & Distance, Probability, 
                    and logical sequences. Features random questions, timer, scoring, and instant step-by-step math breakdowns.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="glass-card">
                <span class="badge-blue">CONVERSATION</span>
                <h4>💬 General AI Chat</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5;">
                    Clear programming doubts, ask career guidance queries, review syllabus guidelines, 
                    or receive mock corporate advice from a supportive AI mentor.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feat_col2:
        st.markdown(
            """
            <div class="glass-card">
                <span class="badge-blue">INTERACTIVE HANDS-ON</span>
                <h4>💻 Coding Practice</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5;">
                    Write and execute Python and Java code for Easy, Medium, and Hard placement interview challenges. 
                    Includes complete problem descriptions, sample inputs, hints, and optimization advice.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="glass-card">
                <span class="badge-blue">BEHAVIORAL EVALUATION</span>
                <h4>💼 HR Mock Interview</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5;">
                    Simulate real HR behavioral rounds question-by-question. Answer recruiter queries, get detailed 
                    feedback, learn structure frameworks (STAR method), and track your scoring metrics.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="glass-card">
                <span class="badge-blue">ATS COMPATIBILITY</span>
                <h4>📄 Resume Review</h4>
                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5;">
                    Upload your resume to get instant ATS scores, grammar checks, skill-gap analysis, 
                    and bullet point recommendations tailored to software engineering job specs.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 4. How It Works Section
    st.subheader("How DhanushaBuddy Accelerates Your Prep")
    how_col1, how_col2, how_col3 = st.columns(3)
    with how_col1:
        st.markdown("##### 1. Select Domain")
        st.write("Pick your learning subject, coding practice question, or mock HR interview role from the sidebar navigation.")
    with how_col2:
        st.markdown("##### 2. Engage & Practice")
        st.write("Ask queries, solve aptitude math quizzes, submit code codeblocks, or talk to the HR behavioral interviewer panel.")
    with how_col3:
        st.markdown("##### 3. Get AI Analysis")
        st.write("Get instant evaluation cards, detailed analogies, step-by-step quiz corrections, or full ATS resume reports.")

    st.markdown("---")

    # 5. Testimonials (Dummy Data)
    st.subheader("What Students Say")
    test_col1, test_col2 = st.columns(2)
    with test_col1:
        st.markdown(
            """
            <div class="glass-card" style="background-color: #F8FAFC;">
                <p style="font-style: italic; color: #475569;">
                    "DhanushaBuddy's HR Mock Interview helped me build confidence. The feedback on structuring my answers 
                    using the STAR method made a huge difference in my actual interview!"
                </p>
                <h6 style="margin: 0; color: #1E3A8A;">— Rahul Sharma, Software Engineer at TCS</h6>
            </div>
            """,
            unsafe_allow_html=True
        )
    with test_col2:
        st.markdown(
            """
            <div class="glass-card" style="background-color: #F8FAFC;">
                <p style="font-style: italic; color: #475569;">
                    "The Learn Concepts explanations are incredibly easy to understand. The analogies Gemini generates 
                    turned complex multi-threading topics in Java into simple day-to-day scenarios."
                </p>
                <h6 style="margin: 0; color: #1E3A8A;">— Sneha Patel, CSE Final Year Student</h6>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 6. Frequently Asked Questions (FAQ)
    st.subheader("Frequently Asked Questions")
    
    with st.expander("Is DhanushaBuddy free to use?"):
        st.write("Yes! DhanushaBuddy is a free AI learning platform built for student placement training.")
        
    with st.expander("Which programming languages are supported in learn and coding modules?"):
        st.write("V1 natively supports Python and Java for coding challenges, and extends concept tutoring to Python, Java, SQL, and database languages.")
        
    with st.expander("How does the AI Mock Interview system work?"):
        st.write("It conducts an interactive, multi-turn interview asking questions one-by-one, evaluates your behavioral responses, and outputs an assessment scorecard detailing communication and confidence levels.")

    # 7. Professional Footer Section
    st.markdown(
        """
        <div class="footer-text">
            <p style="margin-bottom: 0.5rem; font-weight: 600;">🎯 DhanushaBuddy – Your Personal AI Placement Preparation Assistant</p>
            <p style="margin-bottom: 0.5rem; font-size: 0.8rem; color: #94A3B8;">Infosys Pragati Cohort 9 Generative AI Capstone Project</p>
            <p style="font-size: 0.8rem; color: #94A3B8;">&copy; 2026 DhanushaBuddy. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
