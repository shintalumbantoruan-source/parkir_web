from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Parkir Web!"

if __name__ == "__main__":
    app.run(debug=True)
