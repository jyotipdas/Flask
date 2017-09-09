from flask import Flask,render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import InputRequired

app=Flask(__name__)

app.config['SECRET_KEY'] = 'kjwbdvndvsnvnv'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf3yS8UAAAAAEDgFWIeKHal4Vem1HSjDy7br3rr'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf3yS8UAAAAAExePlZihuoFhiZIcZOKWskui3sd'
app.config['TESTING'] = True

#class LoginForm(FlaskForm):
#    username = StringField('username', validators=[InputRequired()])
#    password = PasswordField('password', validators=[InputRequired()])
#    recaptcha = RecaptchaField()

class MyForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    textarea = TextAreaField('Textarea')
    radios = RadioField('Radios', default='option1',
                        choices=[('option1','Option1 is this'),('option2','Option2 may be '
                                                                                                'something '
                                                                                       'else')])
    selects = SelectField('Select',choices=[('1','1'),('2','2')])

@app.route('/form',methods = ['GET','POST'])
def form():
    form = MyForm()

#    if form.validate_on_submit():
#        return '<h1>The username is {} and password is {}.'.format(form.username.data,form.password.data)

    return render_template('form.html',form=form )






if __name__ == "__main__":
    app.run()