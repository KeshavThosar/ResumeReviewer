from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from .utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '995bc82054adf8ddea92cd10d99afbdef6b02a99aa1fb0c8'
app.config['UPLOAD_FOLDER'] = '/uploads'


@app.route('/')
def index():
    return redirect('/review')


# ...

@app.route('/review', methods=['GET', 'POST'])
def get_review():
    job_role = ''
    job_description = ''
    messages = []
    if request.method == 'POST':    
        f = request.files['resume']
        resume_filename = secure_filename(f.filename)
        f.save(resume_filename)

        job_role = request.form['job_role']
        job_description = request.form['job_description']
        resume_info = get_text_from_pdf(resume_filename)   

        response = process_resume(job_role, job_description, resume_info)
        

        for idx in range(len(response['questions'])):
            messages.append({
                'Question': response['questions'][idx], 
                'Answer': response['answers'][idx]
            })
    
    print(messages)
    return render_template('response.html', messages=messages, message_len=len(messages), info={'job_role': job_role, 'job_description': job_description})
