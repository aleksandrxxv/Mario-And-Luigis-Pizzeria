from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "Secret key"

@app.route('/')
def index():
    return render_template('index.html')





