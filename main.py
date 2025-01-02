from flask import Flask, render_template, request, jsonify
from helper_files.utils import *



app = Flask(__name__)
session_agent = Telegram_Session_Handler()

@app.route("/")
def home():
    return render_template("landing_page.html")

@app.route("/get_login_otp", methods=["POST"])
def get_login_otp():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
