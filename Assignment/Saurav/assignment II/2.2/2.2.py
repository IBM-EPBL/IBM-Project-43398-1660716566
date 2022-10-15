
from flask import Flask, render_template, url_for, redirect ,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , IntegerField
from wtforms.validators import InputRequired, Length, ValidationError , NumberRange , EqualTo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(20),nullable=False)
    last_name = db.Column(db.String(10),nullable=True)
    age = db.Column(db.Integer)
    phone = db.Column(db.Integer)


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


    submit = SubmitField('Register')



    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error=""

    print(request.method)

    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(user.password)
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form ,error =error)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # user = load_user(current_user)
    print("session and cookies :" , dict(request.cookies)['session'])

    return render_template('dashboard.html',user=current_user,session=dict(request.cookies)['session'])


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data, password=hashed_password,
            first_name = form.first_name.data, last_name = form.last_name.data,
            age = form.age.data, phone =form.phone.data
            )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        print(form.errors)
        print("issuse")
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run()
