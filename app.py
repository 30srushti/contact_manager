from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change_this_secret_in_production"

DB_PATH = Path(__file__).parent / "contacts.db"

# ---------- Database helper functions ----------

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    );
    """)
    conn.commit()
    conn.close()

# initialize DB
init_db()

# ---------- Routes ----------

@app.route("/", methods=["GET"])
def index():  # must be 'index' to match url_for('index')
    q = request.args.get("q", "").strip()
    conn = get_db_connection()
    if q:
        like_q = f"%{q}%"
        rows = conn.execute(
            "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? ORDER BY name",
            (like_q, like_q, like_q)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM contacts ORDER BY name").fetchall()
    conn.close()
    return render_template("index.html", contacts=rows, q=q)

@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        phone = request.form.get("phone","").strip()
        email = request.form.get("email","").strip()

        if not name:
            flash("Name is required.", "danger")
            return redirect(url_for("add_contact"))

        conn = get_db_connection()
        conn.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                     (name, phone, email))
        conn.commit()
        conn.close()
        flash("Contact added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", action="Add", contact=None)

@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    conn = get_db_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    conn.close()

    if contact is None:
        flash("Contact not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name","").strip()
        phone = request.form.get("phone","").strip()
        email = request.form.get("email","").strip()

        if not name:
            flash("Name is required.", "danger")
            return redirect(url_for("edit_contact", contact_id=contact_id))

        conn = get_db_connection()
        conn.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
                     (name, phone, email, contact_id))
        conn.commit()
        conn.close()
        flash("Contact updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", action="Edit", contact=contact)

@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    flash("Contact deleted.", "success")
    return redirect(url_for("index"))

# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True)
