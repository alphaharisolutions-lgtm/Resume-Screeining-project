from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    # Relationships for cascading delete
    jobs = db.relationship('JobDescription', backref='recruiter', cascade="all, delete-orphan", lazy=True)
    resumes = db.relationship('Resume', backref='student', cascade="all, delete-orphan", lazy=True)

class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    auto_shortlist_threshold = db.Column(db.Float, default=80.0)
    is_active = db.Column(db.Boolean, default=True)
    posted_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationship for cascading delete
    screenings = db.relationship('ScreeningResult', backref='jd', cascade="all, delete-orphan", lazy=True)

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationship for cascading delete
    screenings = db.relationship('ScreeningResult', backref='resume', cascade="all, delete-orphan", lazy=True)

class ScreeningResult(db.Model):
    __tablename__ = 'screening_results'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    jd_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'))
    score = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text)
    status = db.Column(db.String(50), default='unseen')
    interviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
