# 📅 School Schedule Generator

An Artificial Intelligence agent developed in Python to automatically generate and optimize school timetables. This project uses **Constraint Programming (CSP)** to solve complex scheduling problems, ensuring all strict requirements are met while optimizing for quality preferences like consecutive classes and balanced weeks.

> **Academic Context**  
> This application was developed as part of the Artificial Intelligence course in the third year of the degree in Computer Systems Engineering (Licenciatura em Engenharia de Sistemas Informáticos) at Instituto Politécnico do Cávado e do Ave.

---

## 📝 Project Overview

The goal of this project is to create an efficient solution for educational institutions that respects various constraints such as room availability, teacher schedules, and class load distribution.

The problem is modeled as a CSP (Constraint Satisfaction Problem) where the agent searches for a solution that satisfies all **Hard Constraints** and scores highest on **Soft Constraints** (Heuristics).

---

## ⚙️ Prerequisites & Installation

This project requires **Python 3** and the `python-constraint` library.

### 1. Installation
To install the required solver library, run the following command in your terminal:

```bash
pip install python-constraint
```
---

## 🔒 Constraints

The agent applies two types of rules to generate the schedule.

### 1. Hard Constraints
Violating any of these rules invalidates the schedule immediately.

* **No Overlaps:** A teacher cannot teach two classes at once; a room cannot host two classes at once; a class cannot attend two lessons at once.

* **Teacher Availability:** Lessons must be scheduled only during a teacher's available slots.

* **Daily Load:** A class cannot have more than 3 lessons per day.

* **Room Requirements:** Courses requiring a laboratory (e.g., UC14, UC22) are forced into lab01.

* **Split Days:** The two weekly sessions of the same course must occur on different days (promoted to a hard constraint to optimize search efficiency).

### 2. Soft Constraints

These rules are used to score valid solutions to find the "best" one.

* **Compact Week:** Preference for schedules where classes are distributed over exactly 4 days, leaving one day free.

* **Consecutive Lessons:** Preference for minimizing gaps/free blocks between lessons on the same day.

* **Distinct Days:** Reinforces the preference for distributing the workload across different days.

---

## 🚀 How to Run
You can run the project using either the Jupyter Notebook or the standalone Python script.

### Option A: Using Python Script (Recommended)
If you want to run the agent directly from your terminal:

* Open your terminal/command prompt.

* Navigate to the project folder.

* Run the main script:
  
```bash
python Main.py
```

### Option B: Using Jupyter Notebook
If you prefer an interactive environment:

* Open Trabalho_Notebook.ipynb in Jupyter Notebook, JupyterLab, or VS Code.

* Execute all cells sequentially.

* The results will be displayed in the output section of the final cell.


 
