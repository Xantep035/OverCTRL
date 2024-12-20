from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)")
    conn.close()

@app.route("/")
def index():
    with sqlite3.connect("database.db") as conn:
        notes = conn.execute("SELECT id, content FROM notes").fetchall()
    return render_template("index.html", notes=notes)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add", methods=["POST"])
def add_note():
    note = request.form.get("note")
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    return redirect("/")

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
