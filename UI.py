"""
EduNova Academy & International School — Campus Records System
A Streamlit front end over the original JSON-backed student/teacher registry.
Run with:  streamlit run app.py
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
import streamlit as st

DATABASE = "school_data.json"


def load_data():
    data = {"students": [], "teachers": []}
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                data = json.loads(content)
    data.setdefault("students", [])
    data.setdefault("teachers", [])
    for s in data["students"]:
        s.setdefault("grades", {})
    return data


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


def save():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


class Persons(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class Student(Persons):
    def get_role(self):
        return "Student"

    def register(self, name, age, email, roll_no):
        if not Persons.validate_email(email):
            return False, "That email address doesn't look valid."
        if not roll_no.strip():
            return False, "Roll number can't be empty."
        for s in data["students"]:
            if s["roll_no"] == roll_no:
                return False, f"A student with roll number {roll_no} is already registered."
        data["students"].append({
            "name": name,
            "age": age,
            "email": email,
            "roll_no": roll_no,
            "grades": {},
        })
        save()
        return True, f"{name} has been registered as a student."

    def add_grade(self, roll_no, subject, marks):
        for s in data["students"]:
            if s["roll_no"] == roll_no:
                s["grades"][subject] = marks
                save()
                return True, f"Recorded {marks:g} in {subject} for {s['name']}."
        return False, "No student found with that roll number."

    def find(self, roll_no):
        return next((s for s in data["students"] if s["roll_no"] == roll_no), None)


class Teacher(Persons):
    def get_role(self):
        return "Teacher"

    def register(self, name, age, email, subject, emp_id):
        if not Persons.validate_email(email):
            return False, "That email address doesn't look valid."
        if not emp_id.strip():
            return False, "Employee ID can't be empty."
        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                return False, f"A teacher with employee ID {emp_id} is already registered."
        data["teachers"].append({
            "name": name,
            "age": age,
            "email": email,
            "subject": subject,
            "emp_id": emp_id,
        })
        save()
        return True, f"{name} has been registered as a teacher."

    def find(self, emp_id):
        return next((t for t in data["teachers"] if t["emp_id"] == emp_id), None)


student_svc = Student()
teacher_svc = Teacher()

st.set_page_config(
    page_title="EduNova Academy & International School | Campus Records",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
    --ink:#14213D;
    --ink-soft:#1F3157;
    --parchment:#F7F4EC;
    --paper:#FFFFFF;
    --emerald:#1F6F54;
    --emerald-deep:#134A38;
    --brass:#B8862E;
    --brass-soft:#F1E4C2;
    --slate:#5B6478;
    --brick:#A6432F;
    --line:#E1DACB;
}

html, body, [class*="css"], .stMarkdown, p, span, div, label { font-family:'Inter',sans-serif; }
h1,h2,h3,h4, .display-font { font-family:'Fraunces',serif; }
.mono, .mono * { font-family:'IBM Plex Mono',monospace !important; }

.stApp{ background:var(--parchment); }
[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:1.6rem; max-width:1150px; }

/* Sidebar */
[data-testid="stSidebar"]{
    background:var(--ink);
    border-right:3px solid var(--brass);
}
[data-testid="stSidebar"] *{ color:#EDE7D6 !important; }
[data-testid="stSidebar"] .stRadio label{
    font-size:0.98rem;
    padding:0.35rem 0.2rem;
    border-radius:4px;
    transition:background 0.15s ease;
}
[data-testid="stSidebar"] .stRadio label:hover{ background:rgba(255,255,255,0.06); }
[data-testid="stSidebar"] input[type="radio"]{ accent-color:var(--brass); }
[data-testid="stSidebar"] hr{ border-color:rgba(237,231,214,0.25); }

.crest{
    width:64px; height:64px; border-radius:50%;
    background:var(--ink-soft); border:2px solid var(--brass);
    display:flex; align-items:center; justify-content:center;
    font-family:'Fraunces',serif; font-weight:700; font-size:1.35rem;
    color:var(--brass-soft); margin:0 auto 0.6rem auto;
}
.sidebar-school-name{
    text-align:center; font-family:'Fraunces',serif; font-weight:600;
    font-size:1.02rem; line-height:1.25; margin-bottom:0.1rem;
}
.sidebar-tagline{
    text-align:center; font-size:0.72rem; letter-spacing:0.08em;
    text-transform:uppercase; color:#B9AF95 !important; margin-bottom:1.1rem;
}
.sidebar-footer{
    font-size:0.7rem; color:#8D93A6 !important; text-align:center;
    margin-top:2rem; line-height:1.4;
}

/* Letterhead */
.letterhead{
    display:flex; align-items:center; gap:1rem;
    border-bottom:3px double var(--brass);
    padding-bottom:0.9rem; margin-bottom:1.6rem;
}
.letterhead .crest{ margin:0; flex-shrink:0; }
.letterhead h1{
    font-size:1.75rem; color:var(--ink); margin:0; line-height:1.15; font-weight:700;
}
.letterhead .sub{
    color:var(--slate); font-size:0.92rem; margin-top:0.15rem;
}

/* Section headings */
.section-title{
    font-family:'Fraunces',serif; font-weight:600; color:var(--ink);
    font-size:1.3rem; margin-bottom:0.15rem;
}
.section-kicker{
    text-transform:uppercase; letter-spacing:0.1em; font-size:0.72rem;
    color:var(--brass); font-weight:600; margin-bottom:0.2rem;
}
.section-desc{ color:var(--slate); font-size:0.9rem; margin-bottom:1.1rem; }

/* Forms as record cards */
[data-testid="stForm"]{
    background:var(--paper);
    border:1px solid var(--line);
    border-left:4px solid var(--emerald);
    border-radius:8px;
    padding:1.6rem 1.6rem 0.8rem 1.6rem;
    box-shadow:0 1px 4px rgba(20,33,61,0.07);
}
.teacher-form [data-testid="stForm"]{ border-left-color:var(--brass); }

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"]{
    border-radius:5px !important; border-color:var(--line) !important;
}
label{ color:var(--ink) !important; font-weight:500 !important; font-size:0.88rem !important; }

/* Buttons */
.stButton>button, .stFormSubmitButton>button{
    background:var(--emerald); color:#fff !important; border:none;
    border-radius:5px; font-weight:600; padding:0.5rem 1.3rem;
    transition:background 0.15s ease;
}
.stButton>button:hover, .stFormSubmitButton>button:hover{ background:var(--emerald-deep); color:#fff !important; }

/* Custom alerts */
.alert{ border-radius:6px; padding:0.7rem 1rem; margin:0.6rem 0 1rem 0; font-size:0.92rem; border-left:4px solid; }
.alert-success{ background:#EAF3EE; border-color:var(--emerald); color:var(--emerald-deep); }
.alert-error{ background:#F7EAE7; border-color:var(--brick); color:var(--brick); }

/* Stat cards */
.stat-card{
    background:var(--paper); border:1px solid var(--line); border-radius:8px;
    padding:1.1rem 1.2rem; box-shadow:0 1px 4px rgba(20,33,61,0.06); text-align:left;
}
.stat-num{ font-family:'Fraunces',serif; font-weight:700; font-size:2.1rem; color:var(--ink); line-height:1; }
.stat-label{ text-transform:uppercase; letter-spacing:0.07em; font-size:0.72rem; color:var(--slate); margin-top:0.35rem; font-weight:600; }
.stat-accent-emerald .stat-num{ color:var(--emerald); }
.stat-accent-brass .stat-num{ color:var(--brass); }

/* Record card (student / teacher detail) */
.record-card{
    background:var(--paper); border:1px solid var(--line); border-radius:8px;
    padding:1.4rem 1.6rem; box-shadow:0 1px 4px rgba(20,33,61,0.07); margin-top:0.5rem;
}
.record-card.student{ border-left:4px solid var(--emerald); }
.record-card.teacher{ border-left:4px solid var(--brass); }
.record-header{ display:flex; align-items:center; gap:1rem; margin-bottom:1rem; }
.avatar{
    width:52px; height:52px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-family:'Fraunces',serif; font-weight:700; font-size:1.2rem; color:#fff;
}
.avatar.student{ background:var(--emerald); }
.avatar.teacher{ background:var(--brass); }
.record-name{ font-family:'Fraunces',serif; font-weight:600; font-size:1.2rem; color:var(--ink); }
.record-sub{ color:var(--slate); font-size:0.85rem; }
.field-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:0.55rem 1.5rem; margin-bottom:0.9rem; }
.field-label{ text-transform:uppercase; font-size:0.68rem; letter-spacing:0.07em; color:var(--slate); font-weight:600; }
.field-value{ font-size:0.95rem; color:var(--ink); }
.avg-badge{
    display:inline-block; background:var(--brass-soft); color:#7A5A16;
    font-family:'IBM Plex Mono',monospace; font-weight:600; font-size:0.85rem;
    padding:0.2rem 0.7rem; border-radius:20px; margin-top:0.3rem;
}

/* Dataframe wrapper */
.table-wrap{ border:1px solid var(--line); border-radius:8px; overflow:hidden; box-shadow:0 1px 4px rgba(20,33,61,0.06); }
[data-testid="stDataFrame"]{ border-radius:8px; }
</style>
""", unsafe_allow_html=True)


def alert_success(msg):
    st.markdown(f'<div class="alert alert-success">✓ {msg}</div>', unsafe_allow_html=True)


def alert_error(msg):
    st.markdown(f'<div class="alert alert-error">✗ {msg}</div>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="crest">EA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-school-name">EduNova Academy<br>&amp; International School</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Campus Records System</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠  Dashboard",
            "🧑‍🎓  Register Student",
            "🧑‍🏫  Register Teacher",
            "📊  Add Grade",
            "🔍  Find Student",
            "🔍  Find Teacher",
            "📚  Full Directory",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        f'<div class="sidebar-footer">{len(data["students"])} students · {len(data["teachers"])} teachers<br>on record</div>',
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="letterhead">
    <div class="crest">EA</div>
    <div>
        <h1>EduNova Academy &amp; International School</h1>
        <div class="sub">Campus Records System — students, teachers &amp; academic performance</div>
    </div>
</div>
""", unsafe_allow_html=True)

if page.startswith("🏠"):
    st.markdown('<div class="section-kicker">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">A snapshot of the current campus roster.</div>', unsafe_allow_html=True)

    all_marks = [m for s in data["students"] for m in s["grades"].values()]
    overall_avg = sum(all_marks) / len(all_marks) if all_marks else 0
    graded_subjects = {sub for s in data["students"] for sub in s["grades"]}

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label, accent in [
        (c1, len(data["students"]), "Students Enrolled", "emerald"),
        (c2, len(data["teachers"]), "Teachers on Staff", "brass"),
        (c3, f"{overall_avg:.1f}", "Campus Average", "emerald"),
        (c4, len(graded_subjects), "Subjects Tracked", "brass"),
    ]:
        col.markdown(f"""
        <div class="stat-card stat-accent-{accent}">
            <div class="stat-num">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Recently Registered Students</div>', unsafe_allow_html=True)
        if data["students"]:
            df = pd.DataFrame(data["students"])[["roll_no", "name", "age"]].tail(6).iloc[::-1]
            df.columns = ["Roll No.", "Name", "Age"]
            st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
            st.dataframe(df, hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No students registered yet.")

    with right:
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Recently Registered Teachers</div>', unsafe_allow_html=True)
        if data["teachers"]:
            df = pd.DataFrame(data["teachers"])[["emp_id", "name", "subject"]].tail(6).iloc[::-1]
            df.columns = ["Emp. ID", "Name", "Subject"]
            st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
            st.dataframe(df, hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No teachers registered yet.")

elif page.startswith("🧑‍🎓"):
    st.markdown('<div class="section-kicker">Admissions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Register a Student</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Add a new student to the campus roster.</div>', unsafe_allow_html=True)

    with st.form("register_student", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        age = c2.number_input("Age", min_value=3, max_value=100, step=1, value=15)
        c3, c4 = st.columns(2)
        email = c3.text_input("Email Address")
        roll_no = c4.text_input("Roll Number")
        submitted = st.form_submit_button("Register Student")

    if submitted:
        ok, msg = student_svc.register(name.strip(), int(age), email.strip(), roll_no.strip())
        alert_success(msg) if ok else alert_error(msg)

elif page.startswith("🧑‍🏫"):
    st.markdown('<div class="section-kicker">Faculty</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Register a Teacher</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Add a new teacher to the faculty directory.</div>', unsafe_allow_html=True)

    st.markdown('<div class="teacher-form">', unsafe_allow_html=True)
    with st.form("register_teacher", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        age = c2.number_input("Age", min_value=18, max_value=100, step=1, value=30)
        c3, c4 = st.columns(2)
        email = c3.text_input("Email Address")
        subject = c4.text_input("Subject Taught")
        emp_id = st.text_input("Employee ID")
        submitted = st.form_submit_button("Register Teacher")
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        ok, msg = teacher_svc.register(name.strip(), int(age), email.strip(), subject.strip(), emp_id.strip())
        alert_success(msg) if ok else alert_error(msg)

elif page.startswith("📊"):
    st.markdown('<div class="section-kicker">Academics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add a Grade</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Record a subject mark for a registered student.</div>', unsafe_allow_html=True)

    if not data["students"]:
        st.info("Register a student first before adding grades.")
    else:
        options = {f'{s["name"]}  ·  Roll No. {s["roll_no"]}': s["roll_no"] for s in data["students"]}
        with st.form("add_grade", clear_on_submit=True):
            choice = st.selectbox("Student", list(options.keys()))
            c1, c2 = st.columns(2)
            subject = c1.text_input("Subject")
            marks = c2.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5, value=75.0)
            submitted = st.form_submit_button("Save Grade")

        if submitted:
            ok, msg = student_svc.add_grade(options[choice], subject.strip(), float(marks))
            alert_success(msg) if ok else alert_error(msg)

elif page.startswith("🔍  Find Student"):
    st.markdown('<div class="section-kicker">Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Find a Student</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Look up a student\'s record by roll number.</div>', unsafe_allow_html=True)

    if not data["students"]:
        st.info("No students registered yet.")
    else:
        options = {f'{s["name"]}  ·  Roll No. {s["roll_no"]}': s["roll_no"] for s in data["students"]}
        choice = st.selectbox("Student", list(options.keys()))
        s = student_svc.find(options[choice])

        if s:
            grades = s["grades"]
            avg = sum(grades.values()) / len(grades) if grades else 0
            initial = s["name"][:1].upper() or "?"

            fields_html = "".join(
                f'<div><div class="field-label">{k}</div><div class="field-value">{v}</div></div>'
                for k, v in [("Roll No.", s["roll_no"]), ("Age", s["age"]), ("Email", s["email"])]
            )

            st.markdown(f"""
            <div class="record-card student">
                <div class="record-header">
                    <div class="avatar student">{initial}</div>
                    <div>
                        <div class="record-name">{s['name']}</div>
                        <div class="record-sub">Student</div>
                    </div>
                </div>
                <div class="field-grid">{fields_html}</div>
                <div class="avg-badge mono">Average: {avg:.1f}</div>
            </div>
            """, unsafe_allow_html=True)

            if grades:
                st.write("")
                gdf = pd.DataFrame(list(grades.items()), columns=["Subject", "Marks"])
                st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
                st.dataframe(gdf, hide_index=True, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.caption("No grades recorded yet.")

elif page.startswith("🔍  Find Teacher"):
    st.markdown('<div class="section-kicker">Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Find a Teacher</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Look up a teacher\'s record by employee ID.</div>', unsafe_allow_html=True)

    if not data["teachers"]:
        st.info("No teachers registered yet.")
    else:
        options = {f'{t["name"]}  ·  {t["subject"]}  ·  ID {t["emp_id"]}': t["emp_id"] for t in data["teachers"]}
        choice = st.selectbox("Teacher", list(options.keys()))
        t = teacher_svc.find(options[choice])

        if t:
            initial = t["name"][:1].upper() or "?"
            fields_html = "".join(
                f'<div><div class="field-label">{k}</div><div class="field-value">{v}</div></div>'
                for k, v in [("Employee ID", t["emp_id"]), ("Age", t["age"]), ("Subject", t["subject"]), ("Email", t["email"])]
            )

            st.markdown(f"""
            <div class="record-card teacher">
                <div class="record-header">
                    <div class="avatar teacher">{initial}</div>
                    <div>
                        <div class="record-name">{t['name']}</div>
                        <div class="record-sub">Teacher · {t['subject']}</div>
                    </div>
                </div>
                <div class="field-grid">{fields_html}</div>
            </div>
            """, unsafe_allow_html=True)

elif page.startswith("📚"):
    st.markdown('<div class="section-kicker">Registry</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Full Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Every record currently on file.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Students", "Teachers"])

    with tab1:
        if data["students"]:
            rows = []
            for s in data["students"]:
                grades = s["grades"]
                avg = sum(grades.values()) / len(grades) if grades else 0
                rows.append({
                    "Roll No.": s["roll_no"], "Name": s["name"], "Age": s["age"],
                    "Email": s["email"], "Subjects Graded": len(grades), "Average": round(avg, 1),
                })
            st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No students registered yet.")

    with tab2:
        if data["teachers"]:
            st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(data["teachers"])[["emp_id", "name", "age", "subject", "email"]]
                         .rename(columns={"emp_id": "Emp. ID", "name": "Name", "age": "Age",
                                           "subject": "Subject", "email": "Email"}),
                         hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No teachers registered yet.")