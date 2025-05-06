from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="root",
    host="localhost"
)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email=request.form['email']
        cur = conn.cursor()
        cur.execute("INSERT INTO emails (email) VALUES (%s)", (email,))
        conn.commit()
        cur.close()
        return render_template('thankyou.html', email=email)
    return render_template('index.html')