CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL -- student, recruiter, admin
);

CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    recruiter_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    skills TEXT NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE screening_results (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id),
    jd_id INTEGER REFERENCES job_descriptions(id),
    score FLOAT NOT NULL,
    feedback TEXT,
    status VARCHAR(50) DEFAULT 'unseen', -- unseen, shortlisted, rejected
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
