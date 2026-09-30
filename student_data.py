import json
from pathlib import Path


DEFAULT_STUDENTS = {
    "RFID001": {"id": "2026-001", "name": "Juan Dela Cruz"},
    "RFID002": {"id": "2026-002", "name": "Maria Santos"},
    "RFID003": {"id": "2026-003", "name": "Pedro Reyes"},
}

DATA_FILE = Path(__file__).with_name("students.json")


def load_students():
    """Load registered RFID cards, creating the data file on first run."""
    if not DATA_FILE.exists():
        save_students(DEFAULT_STUDENTS)
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_students(students):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=2)


def register_student(rfid, student_id, name):
    students = load_students()
    if rfid in students:
        raise ValueError("That RFID card is already registered.")
    students[rfid] = {"id": student_id, "name": name}
    save_students(students)
    return students[rfid]
