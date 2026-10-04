from pathlib import Path
import sqlite3

from flask import Flask, g, render_template, request

app = Flask(__name__)
app.config["DATABASE"] = str(Path(__file__).with_name("doctors.db"))


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        g._database = db
    return db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("_database", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            experience INTEGER NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            clinic_address TEXT,
            license_number TEXT,
            availability TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()
    db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        doctor_data = {
            "name": request.form.get("name", "").strip(),
            "specialization": request.form.get("specialization", "").strip(),
            "experience": request.form.get("experience", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "clinic_address": request.form.get("clinic_address", "").strip(),
            "license_number": request.form.get("license_number", "").strip(),
            "availability": request.form.get("availability", "").strip(),
        }

        required_fields = [
            "name",
            "specialization",
            "experience",
            "email",
            "phone",
        ]

        if any(not doctor_data[field] for field in required_fields):
            message = "Please complete all required fields."
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO doctors (
                    name, specialization, experience, email, phone,
                    clinic_address, license_number, availability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doctor_data["name"],
                    doctor_data["specialization"],
                    int(doctor_data["experience"]),
                    doctor_data["email"],
                    doctor_data["phone"],
                    doctor_data["clinic_address"],
                    doctor_data["license_number"],
                    doctor_data["availability"],
                ),
            )
            db.commit()
            message = "Doctor registered successfully!"

    db = get_db()
    doctors = db.execute(
        "SELECT * FROM doctors ORDER BY created_at DESC"
    ).fetchall()

    return render_template("index.html", doctors=doctors, message=message)


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
