import streamlit as st
import requests

st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND = "https://ai-interview-platform-s4j9.onrender.com"
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

st.markdown("""
<style>
.main-title{
    font-size:42px;
    font-weight:800;
    color:#4F8BF9;
}
.subtitle{
    font-size:18px;
    color:#808080;
}
.card{
    background-color:#262730;
    padding:18px;
    border-radius:12px;
    border:1px solid #3b3b3b;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">🤖 AI Interview Platform</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Practice real interviews powered by Generative AI.</p>',
    unsafe_allow_html=True
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📄 Resume Analysis")

with col2:
    st.success("🧠 Gemini AI")

with col3:
    st.warning("🎯 Personalized Questions")

st.divider()

st.markdown("## Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("✅ Resume Uploaded Successfully")
if uploaded_file:

    files = {
        "file": (uploaded_file.name, uploaded_file, "application/pdf")
    }

    if st.button("Generate Interview"):

        response = requests.post(
            f"{BACKEND}/upload-resume/",
            files=files
        )

        data = response.json()
        st.write("Backend Response:", data)
        if "interview_questions"  in data:
            st.session_state["questions"] = 
            data["intervie_questions"]
            st.session_state["current index"] = 0
            st.session_state["scores"] = []
            st.rerun()
        else:
            st.error ("Backend didn't return interview questions")
            st.json()
            st.stop()

           

    

    









if "questions" in st.session_state:

    current = st.session_state["current_index"]

    question = st.session_state["questions"][current]
    progress = (current + 1) / len(st.session_state.questions)
    st.progress(progress)


    st.subheader(f"Question {current+1}/10")

    st.write(question)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        if not answer.strip():
            st.warning("Please enter an answer.")
            st.stop()
        
        

    
        response = requests.post(
            f"{BACKEND}/evaluate-answer/",
            json={
                "question": question,
                "answer": answer
            }
        )

        feedback = response.json()

        st.subheader("AI Feedback")

        st.write(feedback["feedback"])
        if "score" in feedback:
            st.metric(
                "Interview Score",
                f"{feedback['score']}/10"



            )
            st.session_state.scores.append(
                feedback["score"]


            )

        else:
            st.balloons()
            st.success("🎉 Interview Completed!")
            st.markdown("## 📊 Final Interview Report")
    

    

   

    if "scores" in st.session_state and st.session_state.scores:

        avg_score = sum(
            st.session_state.scores
        ) / len(st.session_state.scores)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Average Score",
                f"{avg_score:.2f}/10"
            )

        with col2:
            st.metric(
                "Questions Attempted",
                len(st.session_state.questions)
            )

    st.success("""
    ✅ Resume analyzed  
    ✅ AI questions generated  
    ✅ Answers evaluated  
    ✅ Performance report created
    """)
                         





             









 
           
        
        



   