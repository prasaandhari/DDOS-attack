import socket
import datetime
import mysql.connector
import yagmail
import psutil

GREEN_MODE = "IDLE"
ENERGY_MODE = "LOW ENERGY"

MAX_ATTEMPTS = 3


def get_energy_usage():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    return cpu, memory


def log_attacker():

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    date = datetime.datetime.now()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="1cloud"
    )

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO attacker1 VALUES ('', %s, %s, %s)",
        (hostname, ip, date)
    )

    conn.commit()
    conn.close()


def send_alert(email):

    mail = "testsam360@gmail.com"
    password = "rddwmbynfcbgpywf"

    yag = yagmail.SMTP(mail, password)

    yag.send(
        to=email,
        subject="Green Cybersecurity Alert",
        contents="Multiple wrong download key attempts detected."
    )


def check_attempts(session):

    global GREEN_MODE, ENERGY_MODE

    if 'attempts' not in session:
        session['attempts'] = 0

    session['attempts'] += 1

    cpu, memory = get_energy_usage()

    if session['attempts'] == 1:

        GREEN_MODE = "MONITOR"
        ENERGY_MODE = "MEDIUM ENERGY"

        return f"Wrong Key - Monitoring | CPU:{cpu}% MEM:{memory}%"

    elif session['attempts'] == 2:

        GREEN_MODE = "MONITOR"
        ENERGY_MODE = "MEDIUM ENERGY"

        return f"Second Wrong Attempt | CPU:{cpu}% MEM:{memory}%"

    elif session['attempts'] >= MAX_ATTEMPTS:

        GREEN_MODE = "ACTIVE_SECURITY"
        ENERGY_MODE = "HIGH ENERGY"

        log_attacker()

        session['attempts'] = 0

        return f"Security Activated | CPU:{cpu}% MEM:{memory}%"


def reset_attempts(session):

    global GREEN_MODE, ENERGY_MODE

    session['attempts'] = 0
    GREEN_MODE = "IDLE"
    ENERGY_MODE = "LOW ENERGY"


def get_green_mode():

    return GREEN_MODE


def get_energy_mode():

    return ENERGY_MODE