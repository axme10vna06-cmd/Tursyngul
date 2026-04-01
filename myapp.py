import json
import re
from datetime import date, datetime

import streamlit as st

st.set_page_config(
    page_title="Peer Comparison Avoidance Survey",
    page_icon="🧠",
    layout="centered",
)

QUESTIONS = [
    {
        "question": "How often do you measure your success by your own improvement rather than by other people's results?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
    {
        "question": "When setting goals, how much do you focus on your personal starting point and progress?",
        "options": [
            ("Completely focus on my own progress", 1),
            ("Mostly focus on my own progress", 2),
            ("Focus on both equally", 3),
            ("Mostly compare with others", 4),
            ("Fully compare with others", 5),
        ],
    },
    {
        "question": "How often do you feel satisfied when you improve, even if others perform better?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
    {
        "question": "How often do you keep track of your own growth instead of checking where others stand?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
    {
        "question": "How much does personal progress motivate you even without outside recognition?",
        "options": [
            ("Very strongly", 1),
            ("Strongly", 2),
            ("Moderately", 3),
            ("Slightly", 4),
            ("Not at all", 5),
        ],
    },
    {
        "question": "How often do other people's achievements make you question your own worth?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "When someone around you succeeds, how often can you stay focused on your own path?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
    {
        "question": "How often do you compare your academic or work results with those of your peers?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "How often do you feel discouraged after seeing someone else progress faster than you?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "How easy is it for you to appreciate others' success without feeling behind?",
        "options": [
            ("Very easy", 1),
            ("Easy", 2),
            ("Neutral", 3),
            ("Difficult", 4),
            ("Very difficult", 5),
        ],
    },
    {
        "question": "How often do social media posts make you feel that you are not doing enough?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "How often do you compare your lifestyle or achievements with people you see online?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "How well do you manage to remind yourself that what you see online of successful people doesn't show the whole picture?",
        "options": [
            ("Very well", 1),
            ("Well", 2),
            ("Fairly well", 3),
            ("Poorly", 4),
            ("Very poorly", 5),
        ],
    },
    {
        "question": "How often do other people's expectations make you forget your own speed of progress?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "How much does it improve your motivation if you avoid comparisons?",
        "options": [
            ("Improves it very strongly", 1),
            ("Improves it strongly", 2),
            ("Improves it somewhat", 3),
            ("Improves it a little", 4),
            ("Does not help", 5),
        ],
    },
    {
        "question": "How often do you celebrate small victories of yours?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
    {
        "question": "How often do you manage to remind yourself that progress may look different for different people?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
    {
        "question": "How often do you lose motivation due to the feeling that other people are ahead of you?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5),
        ],
    },
    {
        "question": "How confident are you in pursuing your goals without needing to outperform others?",
        "options": [
            ("Very confident", 1),
            ("Confident", 2),
            ("Neutral", 3),
            ("Not very confident", 4),
            ("Not confident at all", 5),
        ],
    },
    {
        "question": "How often do you define what success means to you?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5),
        ],
    },
]


def validate_name(name: str) -> bool:
    pattern = r"^[A-Za-z\s\-']+$"
    return bool(re.fullmatch(pattern, name.strip()))



def calculate_result(total_score: int) -> str:
    if 20 <= total_score <= 35:
        return "Excellent Personal Focus - strong self-growth mindset, very little unhealthy comparison"
    if 36 <= total_score <= 50:
        return "Healthy Progress Orientation - mostly focused on personal goals with only occasional comparison"
    if 51 <= total_score <= 65:
        return "Mild Comparison Tendency - comparison with others occurs but still able to focus on self-progress"
    if 66 <= total_score <= 80:
        return "Moderate Comparison Strain - comparison begins to impact motivation, confidence, satisfaction"
    if 81 <= total_score <= 90:
        return "High Comparison Pressure - frequent comparison with others occurs with reduced self-focus and increasing strain"
    if 91 <= total_score <= 100:
        return "Critical Comparison Pattern - strong dependency on others' achievements with significant impact on self-esteem and motivation"
    return "Invalid total score"


st.title("Peer Comparison Avoidance and Personal Progress Focus Survey")
st.caption("Web version for Streamlit Community Cloud deployment")

page = st.sidebar.radio("Choose section", ["Take survey", "Load saved JSON"])

if page == "Take survey":
    with st.form("survey_form"):
        st.subheader("Participant information")
        full_name = st.text_input("Surname and given name")
        date_of_birth = st.date_input(
            "Date of birth",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=None,
            format="YYYY-MM-DD",
        )
        student_id = st.text_input("Student ID")

        st.subheader("Questions")
        answers = []

        for index, question_data in enumerate(QUESTIONS, start=1):
            option_texts = [text for text, _ in question_data["options"]]
            selected_text = st.radio(
                f"{index}. {question_data['question']}",
                option_texts,
                index=None,
                key=f"q_{index}",
            )
            answers.append((question_data, selected_text))

        submitted = st.form_submit_button("Submit survey")

    if submitted:
        errors = []
        if not full_name.strip() or not validate_name(full_name):
            errors.append("Enter a valid name using only letters, spaces, hyphens, and apostrophes.")
        if not student_id.strip().isdigit():
            errors.append("Student ID must contain digits only.")
        if date_of_birth is None:
            errors.append("Select a valid date of birth.")
        unanswered = [str(i) for i, (_, selected) in enumerate(answers, start=1) if selected is None]
        if unanswered:
            errors.append("Answer all questions before submitting.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            structured_answers = []
            total_score = 0

            for question_data, selected_text in answers:
                selected_score = next(
                    score for text, score in question_data["options"] if text == selected_text
                )
                structured_answers.append(
                    {
                        "question": question_data["question"],
                        "selected_answer": selected_text,
                        "score": selected_score,
                    }
                )
                total_score += selected_score

            psychological_state = calculate_result(total_score)
            result = {
                "full_name": full_name.strip(),
                "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
                "student_id": student_id.strip(),
                "total_score": total_score,
                "psychological_state": psychological_state,
                "answers": structured_answers,
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            st.success("Survey submitted successfully.")
            st.subheader("Result")
            st.write(f"**Name:** {result['full_name']}")
            st.write(f"**Date of Birth:** {result['date_of_birth']}")
            st.write(f"**Student ID:** {result['student_id']}")
            st.write(f"**Total Score:** {result['total_score']}")
            st.write(f"**Psychological State:** {result['psychological_state']}")

            with st.expander("Show answers"):
                for idx, answer in enumerate(result["answers"], start=1):
                    st.write(f"**{idx}. {answer['question']}**")
                    st.write(f"Answer: {answer['selected_answer']}")
                    st.write(f"Score: {answer['score']}")

            json_data = json.dumps(result, indent=4, ensure_ascii=False)
            st.download_button(
                label="Download result as JSON",
                data=json_data,
                file_name="survey_result.json",
                mime="application/json",
            )

else:
    st.subheader("Load saved questionnaire result")
    uploaded_file = st.file_uploader("Upload a JSON result file", type=["json"])

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            st.success("JSON loaded successfully.")
            st.write(f"**Name:** {data.get('full_name', '-')}")
            st.write(f"**Date of Birth:** {data.get('date_of_birth', '-')}")
            st.write(f"**Student ID:** {data.get('student_id', '-')}")
            st.write(f"**Total Score:** {data.get('total_score', '-')}")
            st.write(f"**Psychological State:** {data.get('psychological_state', '-')}")

            answers = data.get("answers", [])
            if answers:
                with st.expander("Show answers"):
                    for idx, answer in enumerate(answers, start=1):
                        st.write(f"**{idx}. {answer.get('question', '')}**")
                        st.write(f"Answer: {answer.get('selected_answer', '')}")
                        st.write(f"Score: {answer.get('score', '')}")
        except json.JSONDecodeError:
            st.error("Invalid JSON file.")
        except Exception as error:
            st.error(f"Error loading file: {error}")
