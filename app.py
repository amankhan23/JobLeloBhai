from flask import Flask, render_template, jsonify, abort, redirect, session, request, url_for
from database import engine, load_jobs_from_db, add_job, load_job_from_db,load_job_from
from sqlalchemy import text
import os
app = Flask(__name__)
app.secret_key= "Amanwjde8yd4tfgccnwdf9u"

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def Title():
    jobs = load_jobs_from_db()
    return render_template('index.html', jobs=jobs)

@app.route('/admin-dash')
def admindash():
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin-dash.html')
    else:
        return redirect(url_for('login'))

@app.route('/add_jobs')  # Corrected route name
def add_job_form():
    return render_template('add_jobs.html')

@app.route('/delete_jobs')
def delete_jobs():
    jobs = load_jobs_from_db()
    return render_template('delete_job.html', jobs=jobs)

@app.route('/delete_jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM jobs WHERE id = :job_id"), {"job_id": job_id})
            conn.commit()
        print(job_id)
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_job', methods=['GET', 'POST'])
def adding_job():
    add_jobs_from_db = add_job()
    return render_template('admin-dash.html', add_jobs_from_db=add_jobs_from_db)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['logged_in'] = True  # Set session variable
            return redirect(url_for('admindash'))
        else:
            return render_template('admin.html', error='Invalid username or password')
    else:
        return render_template('admin.html')

@app.route('/jobs/<int:id>')
def show_job(id):
    jobs = load_job_from_db(id)
    print(type(jobs))
    return render_template('job_desc.html', job=jobs)

@app.route('/application/<int:id>') # Changed route and added job_id parameter.
def Apply_job(id): # added job_id parameter.
    job = load_job_from_db(id)
    return render_template('application_form.html', job=job)


@app.route('/apply', methods=['GET', 'POST']) # Corrected route.
def apply_job():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        resume_file = request.files['resume']
        cover_letter = request.form['cover_letter']

        if resume_file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)

            with engine.connect() as conn:
                query = text(
                    "INSERT INTO Applications (full_name, email, phone, resume_filename, cover_letter) " #added job_id column.
                    "VALUES (:full_name, :email, :phone, :resume_filename, :cover_letter)"
                )
                conn.execute(
                    query,
                    {
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "resume_filename": resume_file.filename,
                        "cover_letter": cover_letter,
                    },
                )
                conn.commit()
            return render_template('application_success.html')
        else:
            return "Resume file is required."
    else:
        return render_template('application_form.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
server = app