from io import BytesIO

from flask import Flask, render_template, request, send_file ,redirect , url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        user_name = request.form.get('username')
        upload = Upload(username = user_name ,filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return redirect("/home")
    return render_template('index.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)


@app.route("/home")
def home():
   l = Upload.query.all()
   return render_template("home.html",users = l)

if __name__ =="__main__":
   app.run()