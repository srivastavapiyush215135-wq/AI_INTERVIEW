import streamlit as st
import requests

st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🤖",
    layout="wide"
)

BACKEND = "https://ai-interview-platform-s4j9.onrender.com"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🤖 AI Interview")
    st.markdown("---")
    st.success("🟢 Backend Connected")

    st.markdown("### Features")
    st.write("✅ Resume Parsing")
    st.write("✅ AI Questions")
    st.write("✅ AI Evaluation")
    st.write("🚀 Interview Report")

# ---------------- TITLE ----------------
st.title("🤖 AI Interview Platform")
st.write("Practice real interviews powered by Generative AI.")

# ---------------- SESSION STATE ----------------
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "scores" not in st.session_state:
    st.session_state.scores = []

# ---------------- CANDIDATE DETAILS ----------------
st.markdown("## Candidate Details")

candidate = st.text_input("Candidate Name")
role = st.text_input(
    "Target Role",
    value="Mechanical Engineer"
)

# ---------------- RESUME UPLOAD ----------------
st.markdown("## Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("✅ Resume Uploaded Successfully")

    if st.button("Generate Interview"):

        if not candidate.strip():
            st.warning("Please enter candidate name.")
            st.stop()

        if not role.strip():
            st.warning("Please enter target role.")
            st.stop()

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        try:
            response = requests.post(
                f"{BACKEND}/upload-resume/",
                files=files,
                timeout=120
            )

            response.raise_for_status()
            data = response.json()

        except Exception as e:
            st.error(f"Backend Error: {e}")
            st.stop()

        if "interview_questions" in data:

            st.session_state.questions = data[
                "interview_questions"
            ]

            st.session_state.current_index = 0
            st.session_state.scores = []

            # Save these for evaluate-answer API
            st.session_state.candidate = candidate
            st.session_state.role = role

            st.rerun()

        else:
            st.error(
                "Backend didn't return interview questions."
            )
            st.json(data)
            st.stop()


# ---------------- INTERVIEW ----------------
if (
    "questions" in st.session_state
    and st.session_state.questions
):

    current = st.session_state.current_index
    questions = st.session_state.questions

    # Interview still running
    if current < len(questions):

        question = questions[current]

        progress = (
            current + 1
        ) / len(questions)

        st.progress(progress)

        st.subheader(
            f"Question {current + 1}/{len(questions)}"
        )

        st.write(question)

        answer = st.text_area(
            "Your Answer",
            key=f"answer_{current}"
        )

        if st.button(
            "Submit Answer",
            key=f"submit_{current}"
        ):

            if not answer.strip():
                st.warning(
                    "Please enter an answer."
                )
                st.stop()

            # IMPORTANT:
            # Backend requires all 4 fields
            payload = {
                "candidate":
                    st.session_state.candidate,

                "role":
                    st.session_state.role,

                "question":
                    question,

                "answer":
                    answer
            }

            try:

                response = requests.post(
                    f"{BACKEND}/evaluate-answer/",
                    json=payload,
                    timeout=120
                )

                # Show API error safely
                if response.status_code != 200:

                    st.error(
                        f"API Error: "
                        f"{response.status_code}"
                    )

                    try:
                        st.json(response.json())
                    except Exception:
                        st.write(response.text)

                    st.stop()

                feedback = response.json()

            except Exception as e:

                st.error(
                    f"Backend request failed: {e}"
                )

                st.stop()

            # ---------------- FEEDBACK ----------------
            st.subheader("AI Feedback")

            st.write(
                feedback.get(
                    "feedback",
                    "No feedback returned."
                )
            )

            # Score if backend returns one
            if "score" in feedback:

                st.metric(
                    "Interview Score",
                    f"{feedback['score']}/10"
                )

                st.session_state.scores.append(
                    feedback["score"]
                )

            # Move to next question
            st.session_state.current_index += 1

            st.rerun()


    # ---------------- INTERVIEW COMPLETE ----------------

else:
    st.balloons()
    st.success("🎉 Interview Completed!")
    st.markdown("## 📊 Final Interview Report")

    # Your existing metrics here...

    report = f"""
AI INTERVIEW REPORT

Candidate: {st.session_state.get("candidate", "Candidate")}
Target Role: {st.session_state.get("role", "Not specified")}
Questions Attempted: {len(questions)}

Interview completed successfully.
"""

    st.download_button(
        label="📥 Download Interview Report",
        data=report,
        file_name="AI_Interview_Report.txt",
        mime="text/plain"
    )
        if st.session_state.scores:

            avg_score = (
                sum(st.session_state.scores)
                / len(st.session_state.scores)
            )

            st.metric(
                "Average Score",
                f"{avg_score:.2f}/10"
            )

        st.metric(
            "Questions Attempted",
            len(questions)
        )

        st.success("""
        ✅ Resume analyzed  
        ✅ AI questions generated  
        ✅ Answers evaluated  
        ✅ Interview completed
        """)
