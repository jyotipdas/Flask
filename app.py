from flask import Flask, render_template,request, url_for, redirect, session, g
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  check_password_hash
from flask_login import LoginManager, login_required, login_user,UserMixin, logout_user,current_user
from datetime import datetime
from sqlalchemy import text
import atexit
from apscheduler.scheduler import Scheduler

app = Flask(__name__)
cron = Scheduler(daemon=True)
cron.start()

app.config['SECRET_KEY'] = ';Y8m4e#PUP\qQR]+"`ZAM(&td{8utWN?CtHXg6X(-z!$XP4?(t)~g4Kk9xgr8}ZaH]eGx(:uvNE}GVp;'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf3yS8UAAAAAEDgFWIeKHal4Vem1HSjDy7br3rr'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf3yS8UAAAAAExePlZihuoFhiZIcZOKWskui3sd'
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///leave.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    balance = db.Column(db.Integer)
    leaves = db.relationship('LeaveDetail', backref='user', lazy='dynamic')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class LeaveDetail(db.Model):
    __tablename__ = 'leavedetail'
    id = db.Column(db.Integer, primary_key=True)
    sdate = db.Column(db.DateTime,nullable=False)
    edate = db.Column(db.DateTime,nullable=False)
    days = db.Column(db.Integer,nullable=False)
    a_time = db.Column(db.DateTime,nullable=False)
    usr_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()


@app.route('/')
@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() :
        db_usr = Users.query.filter_by(username=form.username.data).first()
        if db_usr:
            if check_password_hash(db_usr.password,form.password.data):
                login_user(db_usr, remember=True)

                return render_template('welcome.html', name=form.username.data)
            else:
                return render_template('login.html',form=form, error='Password is not matching...')

    return render_template('login.html', form=form)

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/plan/', methods=['GET','POST'])
@login_required
def plan():
    if request.method == 'POST':
        if request.form['sdate'] > request.form['edate'] :
            return render_template('plan.html', error='Start date is greater than End date')
        sdate = datetime.strptime(str(request.form['sdate']),'%Y-%m-%d')
        edate = datetime.strptime(str(request.form['edate']),'%Y-%m-%d')
        days = int(request.form['days'])
        balance = Users.query.filter_by(id=current_user.get_id()).first()
        dbbalance= balance.balance
        ctime=datetime.now()
        if int(days) <= dbbalance :
            updated_balance = dbbalance - int(days)
            balance.balance = updated_balance
            leave = LeaveDetail(sdate=sdate, edate=edate,days=days,a_time=ctime,
                            user = current_user )
            db.session.add(leave)
            db.session.commit()
            request.form = {}
            return render_template('plan.html',message='Leave applied from {} to {} for {} days'.format(sdate,edate,
                                                                                                        days))
        else:
            balance = balance.balance
            return render_template('plan.html', error='You have only {} no of leaves'.format(balance))

    else:
        return render_template('plan.html')

@app.route('/log/',methods=['GET','POST'])
@login_required
def log():
    results = db.engine.execute(text("select username,sdate,edate,days from users join leavedetail on users.id = "
                                     "leavedetail.usr_id where users.id = {}".format(1)))

    return render_template('log.html', list=results)

@app.route('/balance/')
@login_required
def balance():
    balance = Users.query.filter_by(id=current_user.get_id()).first()
    list = balance.balance
    return render_template('balance.html', list=list)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',error=e)

@cron.interval_schedule(hours=0, start_date='2017-09-20 18:00')
def job_function():
    user = Users.query.filter_by(id=current_user.get_id()).first()
    balance = user.balance
    new_balance = balance + 2
    user.balance = new_balance
    db.session.commit()

atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == "__main__":
    app.run(debug=True)


