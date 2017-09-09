from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismysecretkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf3yS8UAAAAAEDgFWIeKHal4Vem1HSjDy7br3rr'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf3yS8UAAAAAExePlZihuoFhiZIcZOKWskui3sd'
app.config['TESTING'] = True


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    recaptcha = RecaptchaField()


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html',form=form)

@app.route('/reset/')
def reset():
    return render_template('reset.html')


if __name__ == "__main__":
    app.run(debug=True)


