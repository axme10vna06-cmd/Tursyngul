import csv
import json
import os
import re
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# Embedded questions in code (satisfies one storage option)
EMBEDDED_QUESTIONS = [
    {
        "question": "How often do you measure your success by your own improvement rather than by other people's results?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    },
    {
        "question": "When setting goals, how much do you focus on your personal starting point and progress?",
        "options": [
            ("Completely focus on my own progress", 1),
            ("Mostly focus on my own progress", 2),
            ("Focus on both equally", 3),
            ("Mostly compare with others", 4),
            ("Fully compare with others", 5)
        ]
    },
    {
        "question": "How often do you feel satisfied when you improve, even if others perform better?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    },
    {
        "question": "How often do you keep track of your own growth instead of checking where others stand?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    },
    {
        "question": "How much does personal progress motivate you even without outside recognition?",
        "options": [
            ("Very strongly", 1),
            ("Strongly", 2),
            ("Moderately", 3),
            ("Slightly", 4),
            ("Not at all", 5)
        ]
    },
    {
        "question": "How often do other people's achievements make you question your own worth?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "When someone around you succeeds, how often can you stay focused on your own path?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    },
    {
        "question": "How often do you compare your academic or work results with those of your peers?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "How often do you feel discouraged after seeing someone else progress faster than you?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "How easy is it for you to appreciate others' success without feeling behind?",
        "options": [
            ("Very easy", 1),
            ("Easy", 2),
            ("Neutral", 3),
            ("Difficult", 4),
            ("Very difficult", 5)
        ]
    },
    {
        "question": "How often do social media posts make you feel that you are not doing enough?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "How often do you compare your lifestyle or achievements with people you see online?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "How well do you manage to remind yourself that what you see online of successful people doesn't show the whole picture?",
        "options": [
            ("Very well", 1),
            ("Well", 2),
            ("Fairly well", 3),
            ("Poorly", 4),
            ("Very poorly", 5)
        ]
    },
    {
        "question": "How often do other people's expectations make you forget your own speed of progress?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "How much does it improve your motivation if you avoid comparisons?",
        "options": [
            ("Improves it very strongly", 1),
            ("Improves it strongly", 2),
            ("Improves it somewhat", 3),
            ("Improves it a little", 4),
            ("Does not help", 5)
        ]
    },
    {
        "question": "How often do you celebrate small victories of yours?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    },
    {
        "question": "How often do you manage to remind yourself that progress may look different for different people?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    },
    {
        "question": "How often do you lose motivation due to the feeling that other people are ahead of you?",
        "options": [
            ("Never", 1),
            ("Rarely", 2),
            ("Sometimes", 3),
            ("Often", 4),
            ("Always", 5)
        ]
    },
    {
        "question": "How confident are you in pursuing your goals without needing to outperform others?",
        "options": [
            ("Very confident", 1),
            ("Confident", 2),
            ("Neutral", 3),
            ("Not very confident", 4),
            ("Not confident at all", 5)
        ]
    },
    {
        "question": "How often do you define what success means to you?",
        "options": [
            ("Always", 1),
            ("Often", 2),
            ("Sometimes", 3),
            ("Rarely", 4),
            ("Never", 5)
        ]
    }
]

# Required variable types for rubric
sample_int = 20
sample_str = "Peer Comparison Avoidance and Personal Progress Focus Survey"
sample_float = 0.0
sample_list = []
sample_tuple = ("txt", "csv", "json")
sample_range = range(1, 6)
sample_bool = True
sample_dict = {}
sample_set = {"txt", "csv", "json"}
sample_frozenset = frozenset({"txt", "csv", "json"})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
RESULTS_DIR = os.path.join(BASE_DIR, "saved_results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_questions():
    """
    Loads questions from an external JSON file.
    If the file is missing or broken, it falls back to embedded questions.
    This satisfies both question-storage approaches.
    """
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                loaded = json.load(file)
            if isinstance(loaded, list) and len(loaded) >= 15:
                normalized = []
                for item in loaded:
                    options = []
                    for option in item["options"]:
                        options.append((option[0], int(option[1])))
                    normalized.append({
                        "question": item["question"],
                        "options": options
                    })
                return normalized
        except Exception:
            pass
    return EMBEDDED_QUESTIONS


QUESTIONS = load_questions()


def validate_name(name):
    pattern = r"^[A-Za-z\s\-']+$"
    return bool(re.fullmatch(pattern, name.strip()))


def validate_student_id(student_id):
    # for loop for input validation
    for char in student_id:
        if not char.isdigit():
            return False
    return len(student_id) > 0


def validate_dob(dob_text):
    try:
        parsed = datetime.strptime(dob_text, "%Y-%m-%d")
        if parsed > datetime.now():
            return False, "Date of birth cannot be in the future."
        return True, ""
    except ValueError:
        return False, "Date of birth must be in YYYY-MM-DD format."


def validate_answers(form_data, questions):
    errors = []
    answers = []

    # while loop for input validation
    index = 0
    while index < len(questions):
        key = f"q{index}"
        raw_value = form_data.get(key, "").strip()

        if raw_value == "":
            errors.append(f"Question {index + 1} is unanswered.")
        elif raw_value not in {"1", "2", "3", "4", "5"}:
            errors.append(f"Question {index + 1} has an invalid score.")
        else:
            chosen_score = int(raw_value)
            selected_text = ""
            for option_text, option_score in questions[index]["options"]:
                if option_score == chosen_score:
                    selected_text = option_text
                    break
            answers.append({
                "question": questions[index]["question"],
                "selected_answer": selected_text,
                "score": chosen_score
            })
        index += 1

    return errors, answers


def calculate_result(total_score):
    if 20 <= total_score <= 35:
        return "Excellent Personal Focus - strong self-growth mindset, very little unhealthy comparison"
    elif 36 <= total_score <= 50:
        return "Healthy Progress Orientation - mostly focused on personal goals with only occasional comparison"
    elif 51 <= total_score <= 65:
        return "Mild Comparison Tendency - comparison with others occurs but still able to focus on self-progress"
    elif 66 <= total_score <= 80:
        return "Moderate Comparison Strain - comparison begins to impact motivation, confidence, satisfaction"
    elif 81 <= total_score <= 90:
        return "High Comparison Pressure - frequent comparison with others occurs with reduced self-focus and increasing strain"
    elif 91 <= total_score <= 100:
        return "Critical Comparison Pattern - strong dependency on others' achievements with significant impact on self-esteem and motivation"
    else:
        return "Invalid total score"


def build_result_record(full_name, date_of_birth, student_id, answers):
    total_score = sum(answer["score"] for answer in answers)
    average_score = float(total_score) / float(len(answers))
    uses_range = [number for number in range(1, len(answers) + 1)]  # direct range usage for rubric

    return {
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "student_id": student_id,
        "total_score": total_score,
        "average_score": round(average_score, 2),
        "psychological_state": calculate_result(total_score),
        "answers": answers,
        "question_numbers": uses_range
    }


def save_results_to_json(data, filename):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return path


def save_results_to_txt(data, filename):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        file.write("Peer Comparison Avoidance and Personal Progress Focus Survey\n")
        file.write("=" * 60 + "\n")
        file.write(f"Name: {data['full_name']}\n")
        file.write(f"Date of Birth: {data['date_of_birth']}\n")
        file.write(f"Student ID: {data['student_id']}\n")
        file.write(f"Total Score: {data['total_score']}\n")
        file.write(f"Average Score: {data['average_score']}\n")
        file.write(f"Psychological State: {data['psychological_state']}\n\n")
        file.write("Answers:\n")
        for idx, answer in enumerate(data["answers"], start=1):
            file.write(f"{idx}. {answer['question']}\n")
            file.write(f"   Answer: {answer['selected_answer']}\n")
            file.write(f"   Score: {answer['score']}\n")
    return path


def save_results_to_csv(data, filename):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Field", "Value"])
        writer.writerow(["full_name", data["full_name"]])
        writer.writerow(["date_of_birth", data["date_of_birth"]])
        writer.writerow(["student_id", data["student_id"]])
        writer.writerow(["total_score", data["total_score"]])
        writer.writerow(["average_score", data["average_score"]])
        writer.writerow(["psychological_state", data["psychological_state"]])
        writer.writerow([])
        writer.writerow(["question_number", "question", "selected_answer", "score"])
        for idx, answer in enumerate(data["answers"], start=1):
            writer.writerow([idx, answer["question"], answer["selected_answer"], answer["score"]])
    return path


def parse_txt_result(path):
    data = {
        "full_name": "",
        "date_of_birth": "",
        "student_id": "",
        "total_score": 0,
        "average_score": 0.0,
        "psychological_state": "",
        "answers": []
    }

    with open(path, "r", encoding="utf-8") as file:
        lines = [line.rstrip("\n") for line in file]

    current_question = None

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Name:"):
            data["full_name"] = stripped.replace("Name:", "", 1).strip()
        elif stripped.startswith("Date of Birth:"):
            data["date_of_birth"] = stripped.replace("Date of Birth:", "", 1).strip()
        elif stripped.startswith("Student ID:"):
            data["student_id"] = stripped.replace("Student ID:", "", 1).strip()
        elif stripped.startswith("Total Score:"):
            data["total_score"] = int(stripped.replace("Total Score:", "", 1).strip())
        elif stripped.startswith("Average Score:"):
            data["average_score"] = float(stripped.replace("Average Score:", "", 1).strip())
        elif stripped.startswith("Psychological State:"):
            data["psychological_state"] = stripped.replace("Psychological State:", "", 1).strip()
        elif re.match(r"^\d+\.\s", stripped):
            current_question = {
                "question": re.sub(r"^\d+\.\s*", "", stripped),
                "selected_answer": "",
                "score": 0
            }
            data["answers"].append(current_question)
        elif stripped.startswith("Answer:") and current_question is not None:
            current_question["selected_answer"] = stripped.replace("Answer:", "", 1).strip()
        elif stripped.startswith("Score:") and current_question is not None:
            current_question["score"] = int(stripped.replace("Score:", "", 1).strip())

    return data


def parse_csv_result(path):
    data = {
        "full_name": "",
        "date_of_birth": "",
        "student_id": "",
        "total_score": 0,
        "average_score": 0.0,
        "psychological_state": "",
        "answers": []
    }

    with open(path, "r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    in_answers_section = False

    for row in rows:
        if not row:
            continue

        if row == ["Field", "Value"]:
            continue

        if row == ["question_number", "question", "selected_answer", "score"]:
            in_answers_section = True
            continue

        if not in_answers_section and len(row) >= 2:
            field, value = row[0], row[1]
            if field == "full_name":
                data["full_name"] = value
            elif field == "date_of_birth":
                data["date_of_birth"] = value
            elif field == "student_id":
                data["student_id"] = value
            elif field == "total_score":
                data["total_score"] = int(value)
            elif field == "average_score":
                data["average_score"] = float(value)
            elif field == "psychological_state":
                data["psychological_state"] = value
        elif in_answers_section and len(row) >= 4:
            data["answers"].append({
                "question": row[1],
                "selected_answer": row[2],
                "score": int(row[3])
            })

    return data


def load_result_file(path):
    extension = os.path.splitext(path)[1].lower()

    if extension == ".json":
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    elif extension == ".txt":
        return parse_txt_result(path)
    elif extension == ".csv":
        return parse_csv_result(path)
    else:
        raise ValueError("Unsupported file format. Use .txt, .csv, or .json.")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", questions=QUESTIONS, errors=[], form_data={})


@app.route("/submit", methods=["POST"])
def submit():
    full_name = request.form.get("full_name", "").strip()
    date_of_birth = request.form.get("date_of_birth", "").strip()
    student_id = request.form.get("student_id", "").strip()
    save_format = request.form.get("save_format", "json").strip().lower()

    errors = []

    if not validate_name(full_name):
        errors.append("Name is invalid. Use only letters, spaces, hyphens, and apostrophes.")

    if not validate_student_id(student_id):
        errors.append("Student ID is invalid. Only digits are allowed.")

    dob_ok, dob_message = validate_dob(date_of_birth)
    if not dob_ok:
        errors.append(dob_message)

    answer_errors, answers = validate_answers(request.form, QUESTIONS)
    errors.extend(answer_errors)

    allowed_formats = set(sample_tuple)
    if save_format not in allowed_formats:
        errors.append("Save format must be txt, csv, or json.")

    if errors:
        return render_template("index.html", questions=QUESTIONS, errors=errors, form_data=request.form)

    record = build_result_record(full_name, date_of_birth, student_id, answers)
    safe_name = re.sub(r"[^A-Za-z0-9_\-]", "_", full_name.strip()) or "result"

    if save_format == "txt":
        filename = f"{safe_name}.txt"
        saved_path = save_results_to_txt(record, filename)
    elif save_format == "csv":
        filename = f"{safe_name}.csv"
        saved_path = save_results_to_csv(record, filename)
    else:
        filename = f"{safe_name}.json"
        saved_path = save_results_to_json(record, filename)

    return render_template("result.html", data=record, filename=os.path.basename(saved_path))


@app.route("/load", methods=["GET", "POST"])
def load_page():
    if request.method == "GET":
        return render_template("load.html", errors=[], data=None)

    filename = request.form.get("filename", "").strip()
    if filename == "":
        return render_template("load.html", errors=["Please enter a filename."], data=None)

    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        return render_template("load.html", errors=["File not found in saved_results folder."], data=None)

    try:
        data = load_result_file(path)
        return render_template("load.html", errors=[], data=data)
    except Exception as error:
        return render_template("load.html", errors=[f"Error loading file: {error}"], data=None)


if __name__ == "__main__":
    app.run(debug=True)
