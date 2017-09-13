from flask import Flask, render_template,request
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisismysecretkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf3yS8UAAAAAEDgFWIeKHal4Vem1HSjDy7br3rr'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf3yS8UAAAAAExePlZihuoFhiZIcZOKWskui3sd'
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///leave.db"
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True,nullable=False)
    password = db.Column(db.String(30),nullable=False)

    def __init__(self,username,password):
        self.username=username
        self.password=password

    def __repr__(self):
        return '{}={}'.format(self.username,self.password)

class LeaveDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sdate = db.Column(db.DateTime,nullable=False)
    edate = db.Column(db.DateTime,nullable=False)

    usr_idR = db.relationship('users', foreign_keys='leavedetail.usr_id')

    def __init__(self,usr_id,sdate,edate):
        self.usr_id = usr_id
        self.sdate = sdate
        self.edate = edate

    def __repr__(self):
        return '{}={}'.format(self.sdate,self.edate)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()


@app.route('/')
#def index():
#    return render_template('welcome.html')
#
@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template( 'welcome.html' ,name=form.username.data)
    return render_template('login.html', form=form)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/plan/', methods=['GET','POST'])
def plan():
    if request.method == 'POST':
        sdate= request.form['sdate']
        edate= request.form['edate']
        if sdate > edate:
            return render_template('plan.html', error='Start date is greater than End date')
        dates=[sdate,edate]
        print dates
        return render_template('plan.html',message='Leave applied from {} to {}'.format(sdate,edate))
    else:
        return render_template('plan.html')

@app.route('/cancel/',methods=['GET','POST'])
def cancel():
    return render_template('cancel.html', list=[])

@app.route('/balance/')
def balance():
    return render_template('balance.html', list=[])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',error=e)

if __name__ == "__main__":
    app.run(debug=True)


