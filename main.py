from flask import Flask, render_template
from helper_files.utils import Helper
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)
