from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def show_start_page():
    
    return render_template("start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def show_question(qid):

    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect('/thanks')
    
    if (len(responses) != qid):
        flash(f"You're trying to access an invalid question.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question=question)

    

@app.route('/answer', methods=['POST'])
def handle_answer():
    
    answer = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thanks')
    else:
        return redirect(f"/questions',{len(responses)}")
    
@app.route('/thanks')
def show_thanks():
    return render_template("thanks.html")
