from enum import Enum


class State(Enum):
    Q0_IDLE = "q0_idle"
    Q1_READING = "q1"
    Q2_CARD_READ = "q2"
    Q3_VERIFYING = "q3"
    Q4_VALID = "q4"
    Q5_INVALID = "q5"
    Q6_EARLY = "q6"
    Q7_ON_TIME = "q7"
    Q8_LATE = "q8"
    Q9_STATUS = "q9_status"
    Q10_RECORDED = "q10"
    Q11_ERROR = "q11"

