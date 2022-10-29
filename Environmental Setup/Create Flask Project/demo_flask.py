from flask import Flask, jsonify, request
from flask import Flask, render_template
import html

app = Flask(__name__)
@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
  
        data = "Team name: PNT2022TMID17680"
        return render_template('home.html',data = data)
  
if __name__ == '__main__':
  
    app.run()