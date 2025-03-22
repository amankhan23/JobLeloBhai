from flask import Flask, render_template,jsonify


app = Flask(__name__)

jobs=[
    {
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Bengaluru, India',
    'salary': 'Rs. 10,00,000'
  },
  {
    'id': 2,
    'title': 'Service Engineer',
    'location': 'Delhi, India',
    'salary': 'Rs. 15,00,000'
  },
  {
    'id': 3,
    'title': 'Frontend Engineer',
    'location': 'Remote'
  },
  {
    'id': 4,
    'title': 'Backend Engineer',
    'location': 'San Francisco, USA',
    'salary': '$150,000'
  }
]


@app.route('/')

def Title():
    return render_template('index.html',Jobs=jobs)
                             

@app.route('/admin')

def admin():
    return render_template('admin.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)