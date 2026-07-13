import streamlit as st
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND = "https://ai-interview-platform-s4j9.onrender.com"


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "current_index": 0,
    "scores": [],
    "answers": [],
    "feedbacks": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 AI Interview")

    st.markdown("---")

    st.success("🟢 Backend Connected")

    st.markdown("### Features")

    st.write("✅ Resume Parsing")
    st.write("✅ AI Questions")
    st.write("✅ AI Evaluation")
    st.write("🚀 Interview Report")
    st.write("📊 Dashboard")

    st.markdown("---")

    st.caption("Version 1.0")


# =========================================================
# MAIN TITLE
# =========================================================

st.title("🤖 AI Interview Platform")

st.write(
    "Practice real interviews powered by Generative AI."
)

st.divider()


# =========================================================
# CANDIDATE DETAILS
# =========================================================

st.markdown("## 👤 Candidate Details")

candidate = st.text_input(
    "Candidate Name",
    value=st.session_state.get("candidate", "")
)

role = st.text_input(
    "Target Role",
    value=st.session_state.get(
        "role",
        "Mechanical Engineer"
    )
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown("## 📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        "✅ Resume Uploaded Successfully"
    )

    if st.button(
        "Generate Interview",
        type="primary"
    ):

        # Check candidate name
        if not candidate.strip():

            st.warning(
                "Please enter your candidate name."
            )

            st.stop()

        # Check role
        if not role.strip():

            st.warning(
                "Please enter your target role."
            )

            st.stop()


        # Save candidate details
        st.session_state["candidate"] = (
            candidate.strip()
        )

        st.session_state["role"] = (
            role.strip()
        )


        # Prepare PDF
        files = {

            "file": (

                uploaded_file.name,

                uploaded_file,

                "application/pdf"

            )

        }


        # Call backend
        try:

            with st.spinner(
                "Analyzing resume and generating interview questions..."
            ):

                response = requests.post(

                    f"{BACKEND}/upload-resume/",

                    files=files,

                    timeout=120

                )


            # API error
            if response.status_code != 200:

                st.error(
                    f"Backend Error: "
                    f"{response.status_code}"
                )

                try:

                    st.json(
                        response.json()
                    )

                except Exception:

                    st.write(
                        response.text
                    )

                st.stop()


            data = response.json()


        except requests.RequestException as e:

            st.error(
                f"Could not connect to backend: {e}"
            )

            st.stop()


        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )

            st.stop()


        # Check questions
        if (
            "interview_questions" in data
            and data["interview_questions"]
        ):

            st.session_state[
                "questions"
            ] = data[
                "interview_questions"
            ]


            # Reset interview
            st.session_state[
                "current_index"
            ] = 0

            st.session_state[
                "scores"
            ] = []

            st.session_state[
                "answers"
            ] = []

            st.session_state[
                "feedbacks"
            ] = []


            st.rerun()


        else:

            st.error(
                "Backend did not return interview questions."
            )

            st.json(data)

            st.stop()


# =========================================================
# INTERVIEW SECTION
# =========================================================

if (
    "questions" in st.session_state
    and st.session_state["questions"]
):

    questions = (
        st.session_state["questions"]
    )

    current = (
        st.session_state[
            "current_index"
        ]
    )


    # =====================================================
    # INTERVIEW RUNNING
    # =====================================================

    if current < len(questions):

        question = questions[current]


        # Progress bar
        progress = (
            current + 1
        ) / len(questions)

        st.divider()

        st.progress(progress)


        st.subheader(

            f"Question "
            f"{current + 1}/"
            f"{len(questions)}"

        )


        st.info(question)


        # Answer box
        answer = st.text_area(

            "Your Answer",

            key=f"answer_{current}",

            height=150

        )


        # Submit answer
        if st.button(

            "Submit Answer",

            key=f"submit_{current}",

            type="primary"

        ):


            # Empty answer check
            if not answer.strip():

                st.warning(
                    "Please enter an answer."
                )

                st.stop()


            # =================================================
            # API PAYLOAD
            # =================================================

            payload = {

                "candidate":
                    st.session_state.get(
                        "candidate",
                        "Candidate"
                    ),

                "role":
                    st.session_state.get(
                        "role",
                        "Mechanical Engineer"
                    ),

                "question":
                    question,

                "answer":
                    answer.strip()

            }


            # =================================================
            # CALL EVALUATION API
            # =================================================

            try:

                with st.spinner(
                    "AI is evaluating your answer..."
                ):

                    response = requests.post(

                        f"{BACKEND}/evaluate-answer/",

                        json=payload,

                        timeout=120

                    )


                # API Error
                if response.status_code != 200:

                    st.error(

                        f"API Error: "
                        f"{response.status_code}"

                    )


                    try:

                        st.json(
                            response.json()
                        )

                    except Exception:

                        st.write(
                            response.text
                        )


                    st.stop()


                feedback_data = (
                    response.json()
                )


            except requests.RequestException as e:

                st.error(

                    f"Backend request failed: {e}"

                )

                st.stop()


            except Exception as e:

                st.error(

                    f"Unexpected error: {e}"

                )

                st.stop()


            # =================================================
            # SAVE ANSWER
            # =================================================

            st.session_state[
                "answers"
            ].append(

                answer.strip()

            )


            # Get feedback safely
            feedback_text = (
                feedback_data.get(
                    "feedback",
                    "No feedback returned."
                )
            )


            # Convert feedback to text
            if not isinstance(
                feedback_text,
                str
            ):

                feedback_text = str(
                    feedback_text
                )


            st.session_state[
                "feedbacks"
            ].append(

                feedback_text

            )


            # Save score if backend returns it
            if "score" in feedback_data:

                st.session_state[
                    "scores"
                ].append(

                    feedback_data[
                        "score"
                    ]

                )


            # Move to next question
            st.session_state[
                "current_index"
            ] += 1


            st.rerun()


    # =====================================================
    # INTERVIEW COMPLETED
    # =====================================================

    else:

        st.divider()

        st.balloons()

        st.success(
            "🎉 Interview Completed!"
        )


        st.markdown(
            "## 📊 Final Interview Report"
        )


        # Candidate information
        st.write(

            "**Candidate:**",

            st.session_state.get(
                "candidate",
                "Candidate"
            )

        )


        st.write(

            "**Target Role:**",

            st.session_state.get(
                "role",
                "Not specified"
            )

        )


        # Metrics
        col1, col2 = st.columns(2)


        with col1:

            st.metric(

                "Questions Attempted",

                len(
                    st.session_state[
                        "answers"
                    ]
                )

            )


        with col2:

            if st.session_state[
                "scores"
            ]:

                average_score = (

                    sum(
                        st.session_state[
                            "scores"
                        ]
                    )

                    /

                    len(
                        st.session_state[
                            "scores"
                        ]
                    )

                )


                st.metric(

                    "Average Score",

                    f"{average_score:.2f}/10"

                )

            else:

                st.metric(

                    "Interview Status",

                    "Completed"

                )


        # =================================================
        # DISPLAY QUESTIONS, ANSWERS AND FEEDBACK
        # =================================================

        st.markdown(
            "## 📝 Interview Details"
        )


        for i, question in enumerate(
            questions
        ):

            with st.expander(

                f"Question {i + 1}"

            ):

                st.write(
                    "**Question:**"
                )

                st.write(
                    question
                )


                if i < len(
                    st.session_state[
                        "answers"
                    ]
                ):

                    st.write(
                        "**Your Answer:**"
                    )

                    st.write(

                        st.session_state[
                            "answers"
                        ][i]

                    )


                if i < len(
                    st.session_state[
                        "feedbacks"
                    ]
                ):

                    st.write(
                        "**AI Feedback:**"
                    )

                    st.write(

                        st.session_state[
                            "feedbacks"
                        ][i]

                    )


        # =================================================
        # CREATE DOWNLOADABLE REPORT
        # =================================================

        report_lines = [

            "AI INTERVIEW REPORT",

            "=" * 50,

            "",

            "Candidate: "
            + st.session_state.get(
                "candidate",
                "Candidate"
            ),

            "Target Role: "
            + st.session_state.get(
                "role",
                "Not specified"
            ),

            "",

            "Questions Attempted: "
            + str(
                len(
                    st.session_state[
                        "answers"
                    ]
                )
            ),

            "",

            "=" * 50,

            ""

        ]


        # Add every question
        for i, question in enumerate(
            questions
        ):

            report_lines.append(

                f"QUESTION {i + 1}"

            )

            report_lines.append(

                str(question)

            )

            report_lines.append("")


            # Answer
            if i < len(
                st.session_state[
                    "answers"
                ]
            ):

                report_lines.append(

                    "ANSWER:"

                )

                report_lines.append(

                    st.session_state[
                        "answers"
                    ][i]

                )

                report_lines.append("")


            # Feedback
            if i < len(
                st.session_state[
                    "feedbacks"
                ]
            ):

                report_lines.append(

                    "AI FEEDBACK:"

                )

                report_lines.append(

                    st.session_state[
                        "feedbacks"
                    ][i]

                )

                report_lines.append("")


            report_lines.append(

                "-" * 50

            )

            report_lines.append("")


        # Average score
        if st.session_state[
            "scores"
        ]:

            average_score = (

                sum(
                    st.session_state[
                        "scores"
                    ]
                )

                /

                len(
                    st.session_state[
                        "scores"
                    ]
                )

            )


            report_lines.append(

                f"AVERAGE SCORE: "
                f"{average_score:.2f}/10"

            )


        # Join report
        report = "\n".join(
            report_lines
        )


        # =================================================
        # DOWNLOAD BUTTON
        # =================================================

        st.download_button(

            label="📥 Download Interview Report",

            data=report,

            file_name="AI_Interview_Report.txt",

            mime="text/plain",

            type="primary"

        )


        st.success(
            """
            ✅ Resume analyzed  
            ✅ AI questions generated  
            ✅ Answers evaluated  
            ✅ Interview report ready for download
            """
        )
