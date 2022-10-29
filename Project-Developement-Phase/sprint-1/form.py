from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , IntegerField
from wtforms.validators import InputRequired, Length, ValidationError , NumberRange , EqualTo
from CURD import get_user_by_username


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(),Length(min=8,max=30)], render_kw={"placeholder": "username"})

    first_name = StringField(validators=[
                           InputRequired(), Length(min=8,max=30) ], render_kw={"placeholder": "first name"})

    last_name = StringField(validators=[
                           InputRequired(),Length(min=1,max=30) ], render_kw={"placeholder": "last name"})

    age = IntegerField(validators=[InputRequired()],render_kw = {"placeholder" : "age"})

    phone = IntegerField(validators=[InputRequired(),NumberRange(min=1000000000,max=9999999999)],render_kw = {"placeholder" : "phone"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20),EqualTo("confirm",message='password must match')], render_kw={"placeholder": "Password"})

    confirm = PasswordField("Confirm"
                            , render_kw={"placeholder": "confirm password"})

    weight = IntegerField(validators=[InputRequired()],render_kw = {"placeholder" : "weight"})

    blood_group = StringField(validators=[
                           InputRequired(), Length(min=1,max=10) ], render_kw={"placeholder": "Blood Group"})

    submit = SubmitField('Register')



    def validate_username(self, username):
        existing_user_username = get_user_by_username(username.data)
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=40)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class AdminLoginForm(FlaskForm):
    username = StringField(validators=[
                            InputRequired(),Length(min=4,max=10) ],render_kw={"placeholder":"Admin-ID"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=40)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


