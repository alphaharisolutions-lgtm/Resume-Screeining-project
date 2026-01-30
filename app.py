from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from db.models import db, User

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'recruiter':
                return redirect(url_for('recruiter_dashboard'))
            elif user.role == 'interviewer':
                return redirect(url_for('interviewer_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists')
            return render_template('register.html')
            
        hashed_pw = generate_password_hash(password)
        # Force role to student for public registration
        new_user = User(name=name, email=email, password=hashed_pw, role='student')
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.')
            print(f"Registration error: {e}")
            
    return render_template('register.html')

from db.models import db, User, JobDescription, Resume, ScreeningResult
from utils.file_handler import save_resume, extract_text
from utils.screening_engine import screen_resume

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    jobs = JobDescription.query.filter_by(is_active=True).all()
    # Fetch results for this student
    student_resumes = Resume.query.filter_by(student_id=session['user_id']).all()
    resume_ids = [r.id for r in student_resumes]
    screenings = ScreeningResult.query.filter(ScreeningResult.resume_id.in_(resume_ids)).all() if resume_ids else []
    
    results = []
    for s in screenings:
        res = Resume.query.get(s.resume_id)
        jd = JobDescription.query.get(s.jd_id)
        if res and jd:
            results.append({
                'filename': os.path.basename(res.file_path),
                'jd_title': jd.title,
                'score': s.score,
                'status': s.status,
                'date': s.created_at.strftime('%Y-%m-%d')
            })
        
    stats = {
        'total_uploads': len(results),
        'avg_score': sum([r['score'] for r in results]) // len(results) if results else 0,
        'shortlisted': len([r for r in results if r['status'] == 'shortlisted'])
    }
        
    jobs_json = {str(j.id): {"title": j.title, "description": j.description, "skills": j.skills} for j in jobs}
    return render_template('student_dashboard.html', jobs=jobs, jobs_json=jobs_json, results=results, stats=stats, name=user.name)

@app.route('/student/resumes')
def student_resumes():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    student_resumes = Resume.query.filter_by(student_id=session['user_id']).all()
    resume_ids = [r.id for r in student_resumes]
    screenings = ScreeningResult.query.filter(ScreeningResult.resume_id.in_(resume_ids)).all() if resume_ids else []
    
    results = []
    for s in screenings:
        res = Resume.query.get(s.resume_id)
        jd = JobDescription.query.get(s.jd_id)
        if res and jd:
            results.append({
                'filename': os.path.basename(res.file_path),
                'jd_title': jd.title,
                'score': s.score,
                'status': s.status,
                'date': s.created_at.strftime('%Y-%m-%d')
            })
        
    return render_template('student_resumes.html', results=results, name=user.name)

@app.route('/student/matches')
def student_matches():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    # Only show shortlisted results as matches
    student_resumes = Resume.query.filter_by(student_id=session['user_id']).all()
    resume_ids = [r.id for r in student_resumes]
    matches = ScreeningResult.query.filter(ScreeningResult.resume_id.in_(resume_ids), ScreeningResult.status == 'shortlisted').all() if resume_ids else []
    
    results = []
    for m in matches:
        jd = JobDescription.query.get(m.jd_id)
        if jd:
            results.append({
                'job_title': jd.title,
                'score': m.score,
                'date': m.created_at.strftime('%Y-%m-%d')
            })
    return render_template('student_matches.html', results=results, name=user.name)

@app.route('/recruiter/jds')
def recruiter_jds():
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    jds = JobDescription.query.all()
    return render_template('recruiter_jds.html', jds=jds, name=user.name)

@app.route('/recruiter/applications')
def recruiter_applications():
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    all_results = ScreeningResult.query.order_by(ScreeningResult.score.desc()).all()
    candidates = []
    for s in all_results:
        res = Resume.query.get(s.resume_id)
        if not res: continue
        u = User.query.get(res.student_id)
        jd = JobDescription.query.get(s.jd_id)
        if u and jd:
            candidates.append({'id': s.id, 'name': u.name, 'job': jd.title, 'score': s.score, 'status': s.status})
    return render_template('recruiter_applications.html', candidates=candidates, name=user.name)

@app.route('/interviewer/schedule')
def interviewer_schedule():
    if 'user_id' not in session or session['role'] != 'interviewer':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('interviewer_schedule.html', name=user.name)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    file = request.files.get('resume')
    jd_id = request.form.get('jd_id')
    
    if file:
        path = save_resume(file, app.config['UPLOAD_FOLDER'])
        if path:
            new_resume = Resume(student_id=session['user_id'], filename=file.filename, file_path=path)
            db.session.add(new_resume)
            db.session.commit()
            
            # Extract text and screen
            text = extract_text(path)
            jd = JobDescription.query.get(jd_id)
            jd_text = jd.description if jd else ""
            
            score, feedback = screen_resume(text, jd_text)
            
            # Auto-shortlist logic
            status = 'unseen'
            if jd and score >= jd.auto_shortlist_threshold:
                status = 'shortlisted'
            
            result = ScreeningResult(resume_id=new_resume.id, jd_id=jd_id, score=score, feedback=feedback, status=status)
            db.session.add(result)
            db.session.commit()
            
            flash(f"Resume uploaded. AI Score: {score}%. Status: {status.capitalize()}")
    
    return redirect(url_for('student_dashboard'))

@app.route('/recruiter/dashboard')
def recruiter_dashboard():
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    
    # Fetch candidates who applied to this recruiter's jobs
    my_jds = JobDescription.query.filter_by(recruiter_id=session['user_id']).all()
    jd_ids = [j.id for j in my_jds]
    
    screenings = ScreeningResult.query.filter(ScreeningResult.jd_id.in_(jd_ids)).all()
    candidates = []
    for s in screenings:
        resume = Resume.query.get(s.resume_id)
        if not resume: continue
        user = User.query.get(resume.student_id)
        jd = JobDescription.query.get(s.jd_id)
        interviewer = User.query.get(s.interviewer_id) if s.interviewer_id else None
        
        if user and jd:
            candidates.append({
                'id': s.id,
                'name': user.name,
                'job': jd.title,
                'score': s.score,
                'status': s.status,
                'interviewer_name': interviewer.name if interviewer else 'Not Assigned'
            })
            
    interviewers = User.query.filter_by(role='interviewer').all()
    stats = {
        'active_jds': len(my_jds),
        'total_applicants': len(candidates),
        'shortlisted': len([c for c in candidates if c['status'] == 'shortlisted']),
        'avg_score': sum([c['score'] for c in candidates]) // len(candidates) if candidates else 0
    }
    user = User.query.get(session['user_id'])
    return render_template('recruiter_dashboard.html', candidates=candidates, stats=stats, interviewers=interviewers, name=user.name)

@app.route('/recruiter/shortlist/<int:result_id>', methods=['POST'])
def manual_shortlist(result_id):
    if 'user_id' not in session or session['role'] != 'recruiter':
        return jsonify({'error': 'Unauthorized'}), 403
    
    res = ScreeningResult.query.get(result_id)
    if res:
        res.status = 'shortlisted'
        db.session.commit()
        return jsonify({'success': True, 'status': 'shortlisted'})
    return jsonify({'error': 'Not found'}), 404

@app.route('/recruiter/reject/<int:result_id>', methods=['POST'])
def reject_candidate(result_id):
    if 'user_id' not in session or session['role'] != 'recruiter':
        return jsonify({'error': 'Unauthorized'}), 403
    
    res = ScreeningResult.query.get(result_id)
    if res:
        res.status = 'rejected'
        db.session.commit()
        return jsonify({'success': True, 'status': 'rejected'})
    return jsonify({'error': 'Not found'}), 404

@app.route('/recruiter/assign-interviewer', methods=['POST'])
def assign_interviewer():
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    
    result_id = request.form.get('result_id')
    interviewer_id = request.form.get('interviewer_id')
    
    res = ScreeningResult.query.get(result_id)
    if res:
        res.interviewer_id = interviewer_id
        res.status = 'interview_scheduled' # Automatically update status
        db.session.commit()
        flash('Candidate sent to interviewer!')
    
    return redirect(url_for('recruiter_dashboard'))

@app.route('/recruiter/auto-shortlist-config', methods=['GET', 'POST'])
def auto_shortlist_config():
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    my_jds = JobDescription.query.filter_by(recruiter_id=session['user_id']).all()
    
    if request.method == 'POST':
        jd_id = request.form.get('jd_id')
        threshold = request.form.get('threshold')
        jd = JobDescription.query.get(jd_id)
        if jd and jd.recruiter_id == session['user_id']:
            jd.auto_shortlist_threshold = float(threshold)
            db.session.commit()
            flash(f'Auto-shortlist threshold for {jd.title} updated to {threshold}%')
        return redirect(url_for('auto_shortlist_config'))

    return render_template('recruiter_auto_shortlist.html', jds=my_jds, name=user.name)

@app.route('/post-jd', methods=['POST'])
def post_jd():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    title = request.form.get('title')
    desc = request.form.get('description')
    skills = request.form.get('skills')
    
    new_jd = JobDescription(recruiter_id=session['user_id'], title=title, description=desc, skills=skills)
    db.session.add(new_jd)
    db.session.commit()
    flash('Job Description posted!')
    return redirect(url_for('recruiter_dashboard'))

@app.route('/shortlist/<int:result_id>')
def shortlist(result_id):
    res = ScreeningResult.query.get(result_id)
    if res:
        res.status = 'shortlisted'
        db.session.commit()
    return redirect(url_for('recruiter_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    jobs_count = JobDescription.query.count()
    users_count = User.query.count()
    screenings = ScreeningResult.query.all()
    resumes_processed = len(screenings)
    avg_score = sum([s.score for s in screenings]) / len(screenings) if screenings else 0
    
    roles_count = {
        'student': User.query.filter_by(role='student').count(),
        'recruiter': User.query.filter_by(role='recruiter').count(),
        'interviewer': User.query.filter_by(role='interviewer').count(),
        'admin': User.query.filter_by(role='admin').count()
    }
    
    stats = {
        'users': users_count,
        'jobs': jobs_count,
        'resumes': resumes_processed,
        'avg_score': round(avg_score, 1)
    }
    
    return render_template('admin_dashboard.html', stats=stats, roles=roles_count, name="Admin")

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users, name="Admin")

@app.route('/admin/applications')
def admin_applications_global():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    screenings = ScreeningResult.query.all()
    all_apps = []
    for s in screenings:
        res = Resume.query.get(s.resume_id)
        if not res: continue
        u = User.query.get(res.student_id)
        jd = JobDescription.query.get(s.jd_id)
        if u and jd:
            all_apps.append({
                'name': u.name,
                'job': jd.title,
                'score': s.score,
                'status': s.status,
                'date': s.created_at.strftime('%Y-%m-%d')
            })
    
    return render_template('admin_applications.html', applications=all_apps, name="Admin")

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if user:
        if user.id == session['user_id']:
            return jsonify({'error': 'Cannot delete yourself'}), 400
        
        # The improved data model handles cascading deletes (Resumes, Jobs, and Screenings)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'User not found'}), 404

@app.route('/admin/create-user', methods=['POST'])
def admin_create_user():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email address already exists')
        return redirect(url_for('admin_dashboard'))
    
    hashed_pw = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit()
    flash(f'User {name} created successfully as {role}!')
    return redirect(url_for('admin_dashboard'))

@app.route('/interviewer/dashboard')
def interviewer_dashboard():
    if 'user_id' not in session or session['role'] != 'interviewer':
        return redirect(url_for('login'))
    
    # Fetch candidates assigned to this interviewer
    assigned = ScreeningResult.query.filter_by(interviewer_id=session['user_id']).all()
    candidates = []
    for s in assigned:
        resume = Resume.query.get(s.resume_id)
        if not resume: continue
        u = User.query.get(resume.student_id)
        jd = JobDescription.query.get(s.jd_id)
        if u and jd:
            candidates.append({
                'name': u.name,
                'job': jd.title,
                'score': s.score,
                'feedback': s.feedback if s.feedback else "Strong alignment with required skills.",
                'resume_path': resume.file_path.replace('\\', '/')
            })
    user = User.query.get(session['user_id'])
    return render_template('interviewer_dashboard.html', candidates=candidates, name=user.name)

@app.route('/recruiter/delete-jd/<int:jd_id>', methods=['POST'])
def delete_jd(jd_id):
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    
    jd = JobDescription.query.get(jd_id)
    if jd and jd.recruiter_id == session['user_id']:
        db.session.delete(jd)
        db.session.commit()
        flash('Job Posting deleted successfully!')
    return redirect(url_for('recruiter_jds'))

@app.route('/recruiter/toggle-jd/<int:jd_id>', methods=['POST'])
def toggle_jd(jd_id):
    if 'user_id' not in session or session['role'] != 'recruiter':
        return redirect(url_for('login'))
    
    jd = JobDescription.query.get(jd_id)
    if jd and jd.recruiter_id == session['user_id']:
        jd.is_active = not jd.is_active
        db.session.commit()
        status = "active" if jd.is_active else "inactive"
        flash(f'Job Posting marked as {status}!')
    return redirect(url_for('recruiter_jds'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
