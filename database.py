from sqlalchemy import create_engine,text
from flask import request,render_template
from app import engine
engine = create_engine("mysql+pymysql://avnadmin:AVNS_rVbb6wGYObC02zGW_CN@joblelo-joblelobhai.f.aivencloud.com:19883/defaultdb?charset=utf8mb4")
def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all():
            jobs.append(dict(row._mapping))    
        return jobs
def add_job():
    if request.method == 'POST':
        tittle = request.form['title']
        location = request.form['location']
        salary = request.form['salary']
        currency = request.form['currency']
        responsibilities = request.form['responsibilities']
        requirements = request.form['requirements']

        with engine.connect() as conn:
            query = text(
                "INSERT INTO jobs (tittle, location, salary, currency, resposnsiblities, requirements) "
                "VALUES (:tittle, :location, :salary,:currency, :responsibilities, :requirements)"
            )
            conn.execute(
                query,
                {
                    "tittle": tittle,
                    "location": location,
                    "salary": salary,
                    "currency": currency,
                    "responsibilities": responsibilities,
                    "requirements": requirements,
                },
            )
            conn.commit()  # Commit the transaction separately
        return render_template('admin-dash.html')
    else:
        return render_template('admin-dash.html')
    
def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"), {"val": id})
        rows= result.all()
        if len(rows)==0:
             return None
        else:
              print(load_job_from_db)
              return dict(rows[0]._mapping)
        
        
def load_job_from(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"), {"val": id})
        jobs = []
        for row in result.all():
            jobs.append(dict(row._mapping)) 
              
        return jobs
        
    
        
