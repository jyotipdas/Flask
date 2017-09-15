from flask import Flask, render_template,request, url_for, redirect, session, g
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  check_password_hash
from flask_login import LoginManager, login_required, login_user,UserMixin, logout_user,current_user
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisismysecretkey'
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
    leaves = db.relationship('LeaveDetail', backref='user', lazy='dynamic')

#    def __init__(self,username,password):
#        self.username=username
#        self.password=password
#
#    def __repr__(self):
#        return '{}={}'.format(self.username,self.password)
#
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class LeaveDetail(db.Model):
    __tablename__ = 'leavedetail'
    id = db.Column(db.Integer, primary_key=True)
    sdate = db.Column(db.DateTime,nullable=False)
    edate = db.Column(db.DateTime,nullable=False)
    days = db.Column(db.Integer)
    usr_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #usr_idR = db.relationship('users', foreign_keys='leavedetail.usr_id')

#    def __init__(self,usr_id,sdate,edate):
#        self.usr_id = usr_id
#        self.sdate = sdate
#        self.edate = edate
#
#    def __repr__(self):
#        return '{}={}'.format(self.sdate,self.edate)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()


@app.route('/')
#def index():
#    return render_template('welcome.html')
#
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
def welcome():
    return render_template('welcome.html')

@app.route('/plan/', methods=['GET','POST'])
@login_required
def plan():
    if request.method == 'POST':
        if request.form['sdate'] > request.form['edate'] :
            return render_template('plan.html', error='Start date is greater than End date')
        print request.form['sdate'], request.form['edate'],request.form['days']
        sdate = datetime.strptime(str(request.form['sdate']),'%Y-%m-%d')
        edate = datetime.strptime(str(request.form['edate']),'%Y-%m-%d')
        days = request.form['days']
        leave = LeaveDetail(sdate=sdate, edate=edate,days=days,
                            user = current_user )
        db.session.add(leave)
        db.session.commit()
        request.form = {}
        return render_template('plan.html',message='Leave applied from {} to {} for {} days'.format(sdate,edate,days))
    else:
        return render_template('plan.html')

@app.route('/cancel/',methods=['GET','POST'])
@login_required
def cancel():

    return render_template('cancel.html', list=[])

@app.route('/balance/')
@login_required
def balance():
    return render_template('balance.html', list=[])

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',error=e)

if __name__ == "__main__":
    app.run(debug=True)


