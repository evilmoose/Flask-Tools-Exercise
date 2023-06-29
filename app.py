from curses import flash
from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = "never-tell!"

toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_start_page():
    
    return render_template("start.html", survey=survey["satisfaction"])

@app.route('/questions/<int:qid>')
def show_question(qid):

    if (responses is None):
        return redirect("/")

    if qid != len(responses):
        return redirect(url_for('show_question', qid=len(responses)))
    
    if qid != len(responses):
        flash(f"You're trying to access an invalid question.")
        return redirect(url_for('show_question', qid=len(responses)))

    question = survey["satisfaction"].questions[qid]
    return render_template(f"question.html", question=question)

    

@app.route('/answer', methods=['POST'])
def handle_answer():
    
    answer = request.form['answer']
    responses.append(answer)
    if len(responses) == len(survey["satisfaction"].questions):
        return redirect(url_for('show_thanks'))
    else:
        return redirect(url_for('show_question', qid=len(responses)))
    
@app.route('/thanks')
def show_thanks():
    return render_template("thanks.html")
