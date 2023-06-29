from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension

from surveys import Survey, satisfaction_survey as survey

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_start_page():
    
    return render_template("start.html", survey=Survey["satisfaction"])

@app.route('/questions/<int:qid>')
def show_question(qid):
    question = Survey["satisfaction"].questions[qid]
    return render_template("question.html", question=question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    
    answer = request.form['answer']
    responses.append(answer)
    if len(responses) == len(surveys["satisfaction"].questions):
        return redirect(url_for('show_thanks'))
    else:
        return redirect(url_for('show_question', qid=len(responses)))