from flask import Flask, request, render_template_string
import sqlite3, os

app = Flask(__name__)

# ❌ Hardcoded secret (SAST will catch this)
SECRET_KEY = "supersecretpassword123"
DB_PASSWORD = "admin123"

def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, email TEXT)")
    conn.execute("INSERT INTO users VALUES (1,'Alice','alice@example.com')")
    conn.execute("INSERT INTO users VALUES (2,'Bob','bob@example.com')")
    conn.commit()
    return conn

@app.route("/")
def index():
    return "<h1>Vulnerable App</h1><a href='/search?q=Alice'>Search users</a>"
# ❌ SQL Injection vulnerability
@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    # Never do this — use parameterised queries instead
    query = f"SELECT * FROM users WHERE name = '{q}'"
    rows = conn.execute(query).fetchall()
    return str(rows)

# ❌ XSS vulnerability
@app.route("/greet")
def greet():
    name = request.args.get("name", "stranger")
    # Never render user input directly into HTML
    return render_template_string(f"<h1>Hello {name}!</h1>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)