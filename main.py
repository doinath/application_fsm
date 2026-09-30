from .attendance_system import RFIDAttendanceSystem
from .attendance_records import display_records
from .states import State
from .student_data import load_students, register_student
from .utils import validate_time


def display_cards(students):
    print("\nAttendance schedule:")
    print("  EARLY   - before 07:30")
    print("  ON TIME - 07:30 through 08:00")
    print("  LATE    - after 08:00")
    print("\nRegistered RFID cards:")
    for number, (rfid, student) in enumerate(students.items(), start=1):
        print(f"[{number}] {rfid} - {student['name']}")
    print("[R] Register a new student/card")
    print("[H] View attendance history")
    print("[0] Exit")


def register_from_input():
    rfid = input("New RFID code: ").strip().upper()
    student_id = input("Student ID: ").strip()
    name = input("Student name: ").strip()
    if not rfid or not student_id or not name:
        print("All fields are required.")
        return
    try:
        register_student(rfid, student_id, name)
        print(f"Registered {rfid} for {name}.")
    except ValueError as error:
        print(f"Registration failed: {error}")


def handle_error_state(system):
    while system.state == State.Q11_ERROR:
        print("\n[1] Error persists")
        print("[2] Reset system")
        choice = input("Select: ").strip()

        if choice == "1":
            system.error_persists()
        elif choice == "2":
            system.reset()
        else:
            print("Invalid selection.")


def main():
    while True:
        students = load_students()
        system = RFIDAttendanceSystem(students=students)
        print("\n=== RFID ATTENDANCE SIMULATOR ===")
        display_cards(students)

        choice = input("Select RFID card: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        if choice.upper() == "R":
            register_from_input()
            continue
        if choice.upper() == "H":
            display_records()
            input("\nPress ENTER to continue...")
            continue

        cards = list(students)
        if not choice.isdigit() or not 1 <= int(choice) <= len(cards):
            print("Invalid selection.")
            continue
        rfid = cards[int(choice) - 1]

        scan_time = input("Enter simulated scan time (HH:MM): ").strip()
        if not validate_time(scan_time):
            print("Invalid time. Use a 24-hour HH:MM value, such as 07:45.")
            continue

        system.detect_card(rfid, scan_time)

        if system.state == State.Q11_ERROR:
            handle_error_state(system)
        elif system.state == State.Q10_RECORDED:
            input("\nPress ENTER to return to idle...")
            system.ready_for_next_scan()


if __name__ == "__main__":
    main()
