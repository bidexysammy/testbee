from flask import Flask, request, render_template, url_for, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from access.jinjaform import simpleForm, loginForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assess.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///answer.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///question.db'

app.config['SECRET_KEY'] = '35cca6badb571c8504927b545d84e022'

db = SQLAlchemy(app)
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin = Admin(app, name='Facilitator')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    consumer = db.Column(db.String(20), nullable=False)
    
class Answer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(20))
    
class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text(1000)) 
    option_one = db.Column(db.String(255))
    option_two = db.Column(db.String(255))
    option_three = db.Column(db.String(255))
    option_four = db.Column(db.String(255))
    response = db.Column(db.String(255))
    options = db.relationship('Option', backref='question')
    
class Option(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Answer, db.session))
admin.add_view(ModelView(Option, db.session))

@app.route("/settest", methods=["GET", "POST"])
def SetTest():
    form = request.form
    if request.method == 'POST':
        question_text = request.form['textarea']
        option_one = request.form['first']
        option_two = request.form['second']
        option_three = request.form['third']
        option_four = request.form['fourth']
        question = Question(question_text=question_text, option_one=option_one, option_two=option_two, option_three=option_three, option_four=option_four)
        db.session.add(question)
        db.session.commit()
        render_template('setquest.html')
    return render_template('setquest.html', form=form)

@app.route("/myquestion", methods=["GET", "POST"])
def myquestion():
    ans = 0 
    question = Question.query.all()
    quest = question
    answer = Answer.query.all()
    form = request.form
    if request.method == 'POST':
        for request.form in answer:
           ans = ans + 1
           result = f"You scored {ans} out of {Question.query.count()}"
        return render_template('myquestion2.html',question=question, quest=quest)
    return render_template('myquestion2.html',question=question, form=form, quest=quest)

@app.route("/homepage", methods=["GET", "POST"])
def home():
    form = simpleForm()
    if request.method == 'POST':
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = request.form['username']
        password = form.password.data
        button = form.consumer.data
        newuser = User(firstname=firstname, lastname=lastname, username=username, password=password, consumer=button)
        db.session.add(newuser)
        db.session.commit()
        if button == 'Student':
            return redirect(url_for('smain'))
        elif button == 'Facilitator':
            return redirect(url_for('fmain'))
    return render_template('assessment2.html', form=form)
      
@app.route("/smain", methods=["GET", "POST"])
@login_required
def smain():
    form=loginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('You have no account yet! Please create one!')
            return render_template('assessment2.html', form=form)
        if user:
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('question'))
    
    return render_template('studentmain.html', form=form)  

@app.route("/fmain", methods=["GET", "POST"])
@login_required
def fmain():
    form=loginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('You have no account yet! Please create one!')
            return render_template('assessment2.html', form=form)
        if user:
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('admin.index'))
    
    return render_template('fmain.html', form=form)  

@app.route("/questionpage", methods=["GET", "POST"])
@login_required
def question():
    form = request.form
    if request.method == 'POST':
        if request.form['paper'] == 'Mathematics':
            return redirect(url_for('maths'))
        elif request.form['paper'] == 'English':
            return redirect(url_for('english'))
        elif request.form['paper'] == 'General Knowledge':
            return redirect(url_for('gk'))
        elif request.form['paper'] == 'General Science':
            return redirect(url_for('gs'))
    return render_template('question.html', form=form)

@app.route("/maths", methods=["GET", "POST"])
def maths():
    form = request.form
    question = request.form.get['textarea']
    option = request.form.get['input']
    new_question = question(question=question, option=option)
    db.session.add(new_question)
    db.session.commit()
    return render_template('maths.html', form=form)

@app.route("/now", methods=["GET", "POST"])
def quest_now():
    return render_template()

@app.route("/see", methods=["GET", "POST"])
def see_all():
    result = '20 ways'
    answer = Answer(result=result)
    db.session.add(answer)
    db.session.commit()
    them = Answer.query.all()
    return render_template("see.html")

@app.route("/table", methods=["GET", "POST"])
def table():
    answers = Answer.query.all()
    return render_template("table.html", answers=answers)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main'))
    
 
if __name__ == '__main__':
    app.run(debug=True)

