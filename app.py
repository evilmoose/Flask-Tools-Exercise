from flask import Flask, render_template, request
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
    # Render start page with title and instructions
    return render_template("start.html", survey=Survey["satisfaction"])

@app.route('/questions/<int:qid>')
def show_question(qid):
    question = Survey["satisfaction"].questions[qid]
    return render_template("question.html", question=question)