# 🎓 Student Guide: AI Resume Screening & Ranking System

Welcome to the **AI Resume Screening & Ranking System**! This project is a sophisticated blend of **Natural Language Processing (NLP)**, **Deep Learning (DL)**, and **Web Development**. It solves the real-world problem of high-volume hiring by using AI to intelligently match candidates to job descriptions.

---

## 🚀 1. Project Overview
This is an end-to-end recruitment platform where:
*   **Students** upload resumes and see how well they match open jobs.
*   **Recruiters** post jobs, set auto-shortlist thresholds, and manage candidates.
*   **Interviewers** review shortlisted candidates and provide feedback.
*   **Admins** monitor the entire system's analytics.

### Why is this "AI-Powered"?
Unlike traditional systems that just look for keywords (e.g., "Java"), our system uses:
1.  **SBERT (Sentence-BERT)**: To understand the *meaning* behind sentences. It knows that a "MERN Stack Developer" is similar to a "React and Node.js Engineer."
2.  **LSTM (Long Short-Term Memory)**: A type of Recurrent Neural Network (RNN) that analyzes the chronological sequence of a candidate's experience.

---

## 🛠 2. Technology Stack
*   **Backend**: Flask (Python)
*   **Database**: SQLite with SQLAlchemy ORM
*   **AI/ML Framework**: PyTorch
*   **NLP Model**: Sentence-Transformers (`all-MiniLM-L6-v2`)
*   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, Plotly.js (for charts)
*   **Document Parsing**: `pdfminer.six` (for PDFs) and `python-docx` (for Word docs)

---

## 🏗 3. System Architecture
### The AI Pipeline
1.  **Text Extraction**: The system reads your PDF/DOCX and converts it into raw text.
2.  **Vectorization**: SBERT converts the text into a 384-dimensional vector (a list of numbers that represents the text's meaning).
3.  **Scoring Engine**:
    *   **70% Weight**: Cosine Similarity (checks how close the resume meaning is to the job description).
    *   **30% Weight**: LSTM Prediction (analyzes the pattern and structure of the resume).
4.  **Feedback**: The system generates automated feedback based on the final score.

---

## ⚙️ 4. Local Setup (Step-by-Step)

### Prerequisites
*   Python 3.8 or higher installed.
*   Basic knowledge of the terminal/command prompt.

### Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/alphaharisolutions-lgtm/Resume-Screeining-project.git
    cd Resume-Screeining-project
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    *   **Windows**: `venv\Scripts\activate`
    *   **Mac/Linux**: `source venv/bin/activate`

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Initialize the Database**:
    The system automatically creates the `project.db` file in the `instance/` folder when you first run the app.

6.  **Run the Application**:
    ```bash
    python app.py
    ```
    Open your browser and go to: `http://127.0.0.1:5000`

---

## � 5. Terminal Management (Global Usage)
If you are running this system on another machine, you can manage users directly via the terminal without needing to use the Web UI.

### Create a New User
Use `add_user.py` to create admins, recruiters, or interviewers quickly:
```bash
python add_user.py "Name" email@example.com password role
```
*   **Roles**: `admin`, `recruiter`, `interviewer`, `student`

### Reset Admin Password
If you get "Invalid Credentials", use `reset_admin.py` to restore accessibility:
```bash
python reset_admin.py
```
*(Sets `admin@example.com` password to `admin123`)*

---

## �👥 6. User Roles & Credentials
To test the system, you can register as a student. For other roles, use the default credentials or create them via the Admin panel.

| Role | Access Level | Key Features |
| :--- | :--- | :--- |
| **Student** | Candidate | Upload resumes, View AI match scores, Track application status. |
| **Recruiter** | HR / Hiring Manager | Post JDs, Manually shortlist/reject, Assign candidates to interviewers. |
| **Interviewer** | Technical Lead | View technical feedback, review candidate resumes, manage schedules. |
| **Admin** | System Manager | View system-wide stats, manage all users, monitor model performance. |

---

## 📊 6. Key Features to Explore
*   **Auto-Shortlisting**: As a Recruiter, go to "Auto-Shortlist Config" and set a threshold (e.g., 85%). Any student who uploads a resume with a score higher than this is automatically moved to the "Shortlisted" list!
*   **Interactive Analytics**: Check the Admin Dashboard to see Pie Charts of user distributions and bar graphs of system performance.
*   **Deep NLP Feedback**: Look at the "Feedback" column after uploading a resume—it’s generated based on the AI's confidence score.

---

## 🔮 7. Future Learning Path
If you want to take this project further, consider:
1.  **Vector Databases**: Use **FAISS** or **Milvus** to handle millions of resumes efficiently.
2.  **OCR Integration**: Add **Tesseract OCR** to read resumes that are scanned as images.
3.  **LLM Integration**: Use **OpenAI (GPT-4)** or **Llama 3** to generate even more detailed, human-like feedback for candidates.

---
**Happy Coding!** 🚀
If you have questions, feel free to ask!
