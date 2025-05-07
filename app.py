from flask import Flask, render_template, request, redirect,url_for
import psycopg2,base64,os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/postgres')
conn = psycopg2.connect(DATABASE_URL)

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

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
        # Encode user input to "hide" it (fake security)
        encoded_term = base64.b64encode(search_term.encode()).decode()
        return redirect(url_for('search_results', q=encoded_term))
    return redirect('/')

@app.route('/search/results')
def search_results():
    encoded_query = request.args.get('q', '')
    try:
        # Decode the input (but still unsafe!)
        decoded_query = base64.b64decode(encoded_query).decode('utf-8')
    except:
        decoded_query = ""
    
    cur = conn.cursor()
    # UNSAFE: Direct string interpolation (SQLi possible)
    cur.execute(f"SELECT * FROM systems WHERE name LIKE '%{decoded_query}%'")
    results = cur.fetchall()
    cur.close()
    return render_template('search_results.html', results=results, query=decoded_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)