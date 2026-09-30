import json
from datetime import datetime
from pathlib import Path


RECORDS_FILE = Path(__file__).with_name("attendance_records.json")


def load_records():
    if not RECORDS_FILE.exists():
        return []
    with RECORDS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_record(rfid, student, scan_time, status):
    records = load_records()
    records.append(
        {
            "recorded_at": datetime.now().isoformat(timespec="seconds"),
            "student_id": student["id"],
            "name": student["name"],
            "rfid": rfid,
            "scan_time": scan_time,
            "status": status,
        }
    )
    with RECORDS_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def display_records():
    records = load_records()
    if not records:
        print("\nNo attendance records yet.")
        return

    print("\n=== ATTENDANCE HISTORY ===")
    for record in records:
        print(
            f"{record['recorded_at']} | {record['student_id']} | "
            f"{record['name']} | {record['rfid']} | "
            f"{record['scan_time']} | {record['status']}"
        )

