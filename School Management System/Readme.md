**
# 🎓 EduNova Academy & International School

### Campus Records Management System

A simple and modern **School Management System** built with **Python, Streamlit, JSON, Pandas, and Object-Oriented Programming (OOP)**.

The application provides an interactive dashboard for managing **students, teachers, grades, and academic records** through a clean web-based interface.

---

## 📌 Project Overview

**EduNova Academy & International School — Campus Records System** is designed to manage basic school records digitally.

The application allows users to:

* Register students
* Register teachers
* Add student grades
* Search student records
* Search teacher records
* View complete student and teacher directories
* Calculate student average marks
* View overall campus statistics
* Store records permanently in a JSON file

The project uses **Streamlit** to convert the Python-based school management system into an interactive web application.

---

## ✨ Features

### 🏠 Dashboard

The dashboard provides an overview of the school's current records.

It displays:

* Total students enrolled
* Total teachers
* Overall academic average
* Number of subjects being tracked
* Recently registered students
* Recently registered teachers

The dashboard calculates the overall average from the grades stored for students.

---

### 🧑‍🎓 Register Student

Users can register a new student by entering:

* Full Name
* Age
* Email Address
* Roll Number

The system validates the email address and prevents duplicate roll numbers.

Each student record contains:

```text
Name
Age
Email
Roll Number
Grades
```

---

### 🧑‍🏫 Register Teacher

Teachers can be added to the school directory using:

* Full Name
* Age
* Email Address
* Subject
* Employee ID

The system validates the email and prevents duplicate employee IDs.

---

### 📊 Add Grade

Grades can be added to any registered student.

The user selects:

* Student
* Subject
* Marks

Marks are restricted between **0 and 100**.

The application automatically updates the student's grade record and saves the changes to the database.

---

### 🔍 Find Student

Students can be searched using their roll number.

The student record displays:

* Name
* Roll Number
* Age
* Email
* Grades
* Average Marks

The average is calculated automatically from the student's recorded grades.

---

### 🔍 Find Teacher

Teachers can be searched using their Employee ID.

The system displays:

* Name
* Employee ID
* Age
* Subject
* Email

---

### 📚 Full Directory

The Full Directory provides two sections:

**Students**

* Roll Number
* Name
* Age
* Email
* Subjects Graded
* Average

**Teachers**

* Employee ID
* Name
* Age
* Subject
* Email

---

## 🧠 OOP Concepts Used

This project demonstrates several important **Object-Oriented Programming concepts in Python**.

### 1. Abstract Base Class

The project uses an abstract `Persons` class as the base class for students and teachers.

```python
class Persons(ABC):
```

It defines common behavior that subclasses must implement.

### 2. Inheritance

Both `Student` and `Teacher` inherit from `Persons`.

```python
class Student(Persons):
```

```python
class Teacher(Persons):
```

This allows both classes to share common functionality.

### 3. Abstraction

Abstract methods such as `get_role()` define methods that subclasses need to implement.

### 4. Encapsulation

Student and teacher operations are organized inside their respective classes rather than keeping all functionality in one large block of code.

### 5. Static Method

The project uses a static method for email validation:

```python
@staticmethod
def validate_email(email):
    return "@" in email and "." in email
```

---

## 🛠️ Technologies Used

| Technology   | Purpose                      |
| ------------ | ---------------------------- |
| 🐍 Python    | Main programming language    |
| 🎨 Streamlit | Web application interface    |
| 📊 Pandas    | Tables and data presentation |
| 🗃️ JSON     | Data storage                 |
| 🧠 OOP       | Project architecture         |
| 📁 pathlib   | File and database handling   |
| 🔤 ABC       | Abstract classes and methods |

---

## 📂 Project Structure

```text
EduNova-Academy/
│
├── UI.py
├── School_Management_System.py
├── school_data.json
├── README.md
└── screenshot.png
```

### File Description

**`UI.py`**

Contains the Streamlit interface, dashboard, forms, navigation, search pages, directory, styling, and application logic.

**`School_Management_System.py`**

Contains the original Python-based student and teacher registry using OOP and JSON storage.

**`school_data.json`**

Stores student and teacher records in JSON format.

**`README.md`**

Project documentation for GitHub.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/EduNova-Academy.git
```

### 2. Open the Project Folder

```bash
cd EduNova-Academy
```

### 3. Install Required Libraries

```bash
pip install streamlit pandas
```

### 4. Run the Application

Since the Streamlit interface is contained in `UI.py`, run:

```bash
streamlit run UI.py
```

The application will open in your browser.

---

## 💾 Data Storage

The application uses a JSON file as its database:

```text
school_data.json
```

The application loads the existing data when it starts and saves new or updated records back into the JSON file.

The data is organized into two main sections:

```json
{
    "students": [],
    "teachers": []
}
```

Students also contain a `grades` object for storing subject-wise marks.

---

## 🔄 Application Workflow

```text
                    ┌──────────────────────┐
                    │   EduNova Academy    │
                    │   Campus Records     │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
          Student Records              Teacher Records
                │                             │
        ┌───────┴───────┐               ┌─────┴─────┐
        │               │               │           │
    Register        Add Grades      Register     Search
        │               │               │           │
        └───────┬───────┘               └─────┬─────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                        school_data.json
```

---

## 🎨 User Interface

The application uses a custom Streamlit design with:

* Dark navy sidebar
* Gold/brass accents
* Academic-style typography
* Dashboard cards
* Student and teacher record cards
* Responsive tables
* Registration forms
* Navigation sidebar

The Streamlit interface defines custom colors, typography, forms, buttons, cards, and record layouts using CSS.

---

## 📊 Main Navigation

The application contains the following pages:

```text
🏠 Dashboard
🧑‍🎓 Register Student
🧑‍🏫 Register Teacher
📊 Add Grade
🔍 Find Student
🔍 Find Teacher
📚 Full Directory
```

These navigation options are implemented through the Streamlit sidebar.

---

## 🔐 Data Validation

The application includes basic validation for:

* Email addresses
* Empty roll numbers
* Duplicate student roll numbers
* Empty employee IDs
* Duplicate teacher employee IDs
* Grade range between 0 and 100

For example, duplicate student roll numbers are rejected before a new record is created.

---

## 🚀 Future Improvements

The project can be extended with more advanced school-management features.

Possible improvements include:

* 🔐 Admin login system
* 👨‍👩‍👧 Parent accounts
* 📅 Attendance management
* 💰 Fee management
* 📝 Examination management
* 📈 Student performance charts
* 📄 Report card generation
* 📧 Email notifications
* 🗄️ MySQL/PostgreSQL database
* ✏️ Edit student and teacher records
* 🗑️ Delete records
* 🔎 Advanced search and filtering
* 📱 Improved mobile responsiveness
* 📥 Export records to Excel/PDF
* 🔒 Role-based authentication

---

## 🎯 Learning Objectives

This project was created to practice and demonstrate:

* Python programming
* Object-Oriented Programming
* Abstract classes
* Inheritance
* Static methods
* JSON file handling
* Data persistence
* Streamlit
* Pandas
* Form handling
* Data validation
* Basic UI/UX design
* Building a Python project into a web application

---

## 👨‍💻 Author

**Saurav Singh**

This project was created as a learning project to practice **Python, OOP, Streamlit, JSON, and Pandas** while building a practical School Management System.

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is open-source and available for educational and personal use.
