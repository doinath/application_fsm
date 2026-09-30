from time import sleep

from .attendance_records import save_record
from .states import State
from .student_data import load_students
from .utils import determine_attendance_status


class RFIDAttendanceSystem:
    """Finite-state machine for simulated RFID attendance scans."""

    def __init__(self, transition_delay=0.5, students=None):
        self.state = State.Q0_IDLE
        self.rfid = None
        self.student = None
        self.scan_time = None
        self.attendance_status = None
        self.transition_delay = transition_delay
        self.students = students if students is not None else load_students()

    def transition(self, new_state, event):
        print(f"\n[{self.state.value}] -- {event} --> [{new_state.value}]")
        if self.transition_delay:
            sleep(self.transition_delay)
        self.state = new_state

    def detect_card(self, rfid, scan_time):
        self.rfid = rfid
        self.scan_time = scan_time
        self.transition(State.Q1_READING, "RFID CARD DETECTED")
        self.read_card()

    def read_card(self):
        self.transition(State.Q2_CARD_READ, "RFID CARD READ")
        self.start_verification()

    def start_verification(self):
        self.transition(State.Q3_VERIFYING, "VERIFYING CARD")
        self.verify_card()

    def verify_card(self):
        if self.rfid in self.students:
            self.student = self.students[self.rfid]
            self.transition(State.Q4_VALID, "VALID ID")
            self.check_time()
        else:
            self.transition(State.Q5_INVALID, "INVALID ID")
            self.error()

    def check_time(self):
        self.attendance_status = determine_attendance_status(self.scan_time)
        status_states = {
            "EARLY": State.Q6_EARLY,
            "ON TIME": State.Q7_ON_TIME,
            "LATE": State.Q8_LATE,
        }
        self.transition(status_states[self.attendance_status], self.attendance_status)
        self.determine_status()

    def determine_status(self):
        self.transition(State.Q9_STATUS, "STATUS DETERMINED")
        self.record_attendance()

    def record_attendance(self):
        save_record(self.rfid, self.student, self.scan_time, self.attendance_status)
        self.transition(State.Q10_RECORDED, "ATTENDANCE RECORDED")
        self.display_record()

    def error(self):
        self.transition(State.Q11_ERROR, "ERROR")
        print("ERROR: RFID card is not registered.")

    def error_persists(self):
        self.transition(State.Q11_ERROR, "ERROR PERSISTS")

    def reset(self):
        self.transition(State.Q0_IDLE, "RESET")
        self.clear_data()

    def ready_for_next_scan(self):
        self.transition(State.Q0_IDLE, "READY FOR NEXT SCAN")
        self.clear_data()

    def clear_data(self):
        self.rfid = None
        self.student = None
        self.scan_time = None
        self.attendance_status = None

    def display_record(self):
        print("\n" + "=" * 50)
        print("ATTENDANCE RECORD")
        print("=" * 50)
        print(f"Student ID : {self.student['id']}")
        print(f"Name       : {self.student['name']}")
        print(f"RFID       : {self.rfid}")
        print(f"Time       : {self.scan_time}")
        print(f"Status     : {self.attendance_status}")
