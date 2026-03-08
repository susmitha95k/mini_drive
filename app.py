import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models import get_db_connection

app = Flask(__name__)
app.config.from_object(Config)

# Create upload folder
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

# ================= LOGIN MANAGER =================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    conn.close()

    if user:
        return User(user["id"], user["username"], user["email"], user["password"])

    return None


# ================= ROUTES =================

@app.route("/")
def home():
    return redirect(url_for("login"))


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            login_user(User(user["id"], user["username"], user["email"], user["password"]))

            return redirect(url_for("dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")


# ================= LOGOUT =================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ================= DASHBOARD =================

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM files WHERE user_id=%s", (current_user.id,))
    files = cur.fetchall()

    total_size = 0

    for file in files:

        if os.path.exists(file["file_path"]):

            size = os.path.getsize(file["file_path"])
            file["size"] = round(size / 1024, 2)

            total_size += size
        else:
            file["size"] = 0

    total_size = round(total_size / (1024 * 1024), 2)

    conn.close()

    return render_template("dashboard.html", files=files, total_size=total_size)


# ================= UPLOAD FILE =================

@app.route("/upload", methods=["POST"])
@login_required
def upload():

    file = request.files["file"]
    access = request.form["access"]

    if file and file.filename != "":

        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

        file.save(filepath)

        share_token = str(uuid.uuid4())[:8]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """INSERT INTO files 
            (filename, file_path, access_type, user_id, share_token) 
            VALUES (%s,%s,%s,%s,%s)""",
            (filename, filepath, access, current_user.id, share_token)
        )

        conn.commit()
        conn.close()

        flash("File uploaded successfully!", "success")

    return redirect(url_for("dashboard"))


# ================= DOWNLOAD =================

@app.route("/download/<int:file_id>")
@login_required
def download(file_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM files WHERE id=%s", (file_id,))
    file = cur.fetchone()

    conn.close()

    if not file:
        return "File not found", 404

    if file["access_type"] == "private" and file["user_id"] != current_user.id:
        return "Access denied", 403

    return send_from_directory(
        Config.UPLOAD_FOLDER,
        file["filename"],
        as_attachment=True
    )


# ================= DELETE FILE =================

@app.route("/delete/<int:file_id>")
@login_required
def delete_file(file_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM files WHERE id=%s", (file_id,))
    file = cur.fetchone()

    if file and file["user_id"] == current_user.id:

        if os.path.exists(file["file_path"]):
            os.remove(file["file_path"])

        cur.execute("DELETE FROM files WHERE id=%s", (file_id,))
        conn.commit()

    conn.close()

    flash("File deleted successfully", "success")

    return redirect(url_for("dashboard"))


# ================= SHARE PUBLIC LINK =================

@app.route("/share/<token>")
def share_file(token):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM files WHERE share_token=%s", (token,))
    file = cur.fetchone()

    conn.close()

    if not file:
        return "File not found"

    return send_from_directory(
        Config.UPLOAD_FOLDER,
        file["filename"],
        as_attachment=True
    )


# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)