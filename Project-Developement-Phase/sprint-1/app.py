
from CURD import add_admin, connect_db ,add_user, get_admin_by_id,get_user_by_id , get_user_by_username , get_admin_by_username
from flask import Flask, render_template, url_for, redirect ,request,make_response
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
# from flask_login_multi.login_manager import LoginManager
from flask_bcrypt import Bcrypt
from form import LoginForm , RegisterForm , AdminLoginForm
import getpass

# from views import admin_app ,set_bcrypt , admin
app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# admin_app = Blueprint('admin_app', __name__)
# user_app = Blueprint('user_app', __name__)

# app.register_blueprint(admin_app,url_prefix="/")
# app.register_blueprint(user_app,url_prefix="/")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return get_user_by_id(int(id))


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    error=""

    print(request.method)

    if request.method == "POST":

        user = get_user_by_username(form.username.data)
        if user:
            flag = bcrypt.check_password_hash(user.password.strip(), form.password.data)
            print(flag)
            if flag:
                print("password is true")
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                error = ["Username/Password invalid"]

    return render_template('login.html', form=form ,error =error)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html',user=current_user)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        add_user(
            username=form.username.data, password=hashed_password,
            first_name = form.first_name.data, last_name = form.last_name.data,
            age = form.age.data, phone =form.phone.data,
            blood_group = form.blood_group.data , weight = form.weight.data
            )
        return redirect(url_for('login'))
    else:
        print(form.errors)
        print("issuse")
    return render_template('register.html', form=form)


def create_admin():
    while(1):
        print("Creating a admin account ")
        admin_id = input("Enter ur new Admin-ID ")
        admin = get_admin_by_username(admin_id)
        if admin:
            print("Admin-Id Already Exist.")
        else:
            break

    for i in range(3):
        paswd = getpass.getpass("Enter password : ")
        cpasswd = getpass.getpass("Confirm password : ")
        if paswd == cpasswd:
            paswd= bcrypt.generate_password_hash(paswd)
            add_admin(admin_id,paswd)
            break
        else:
            print("Password mismatch")


def login_admin(user,pas):
    res = make_response(render_template("admin-panel.html",user=user),200)
    res.set_cookie("token",value="{}-{}".format(user.id,pas))

    return res


@app.route("/admin",methods=["GET","POST"])
def admin():
    form = AdminLoginForm()
    error=""

    print(request.method)

    if request.method == "POST":

        user = get_admin_by_username(form.username.data)
        if user:
            flag = bcrypt.check_password_hash(user.password.strip(), form.password.data)
            print(flag)
            if flag:
                print("password is true")
                # login_user(user)
                return login_admin(user,user.password.strip())
                # return redirect(url_for('admin_panel'))
            else:
                error = ["Username/Password invalid"]

    return render_template('admin.html', form=form ,error =error)


@app.route("/admin-panel")
# @login_required
def admin_panel():
    token = request.cookies.get("token")
    # print(l)
    if token:
        id = token.split("-")[0]
        user = get_admin_by_id(id)
        return render_template("admin-panel.html",user=user)
    else:
        return redirect(url_for("admin"))


@app.route("/admin-logout")
def admin_logout():
    # logout_user()
    res = make_response(redirect(url_for("admin")),302)
    res.set_cookie('token', '', max_age=0)
    return res
    # return redirect(url_for('admin'))


if __name__ == "__main__":
    connect_db()
    app.run()
    # create_admin()


