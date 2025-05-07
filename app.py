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

@app.route("/systems")
def systems():
    cur=conn.cursor()
    cur.execute("SELECT id, name, image_url FROM systems")
    systems=cur.fetchall()
    cur.close()
    return render_template("systems.html", systems=systems)

@app.route("/system/<int:system_id>")
def system_details(system_id):
    cur=conn.cursor()
    cur.execute("SELECT name,image_url FROM systems WHERE id = %s", (system_id,))
    system=cur.fetchone()
    cur.execute("SELECT spec_key, spec_value FROM system_specs WHERE system_id=%s", (system_id,))
    specs = cur.fetchall()
    cur.close()
    return render_template("system.html",system=system, specs=specs)

@app.route("/admin")
def admin():
    cur=conn.cursor()
    cur.execute("SELECT email FROM emails")
    emails = [row[0] for row in cur.fetchall()]
    cur.close()
    return render_template("admin.html", emails=emails)