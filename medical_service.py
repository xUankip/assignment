from datetime import datetime
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="medical_service"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def add_patients_and_doctors():
    conn = connect_db()
    if conn is None:
        return None
    cursor = conn.cursor()

    for i in range(3):
        name = input(f"Enter patient {i+1} name: ")
        dob = input(f"Enter patient {i+1} dob: ")
        gender = input(f"Enter patient {i+1} gender: ")
        address = input(f"Enter patient {i+1} address: ")
        phone = input(f"Enter patient {i+1} phone number: ")
        email = input(f"Enter patient {i+1} email: ")
        cursor.execute("""
                INSERT INTO patients (full_name, date_of_birth, gender, address, phone_number, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, dob, gender, address, phone, email))
    for i in range(5):
        name = input(f"Enter doctor {i+1} name: ")
        specialization = input(f"Enter doctor {i+1} specialization: ")
        phone = input(f"Enter doctor {i+1} phone number: ")
        email = input(f"Enter doctor {i+1} email: ")
        year_of_experience = input(f"Enter doctor {i+1} year of experience: ")
        cursor.execute("""
                    INSERT INTO doctors (full_name, specialization, phone_number, email, years_of_experience)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, specialization, phone, email, year_of_experience))

    conn.commit()
    cursor.close()
    conn.close()

def add_appointments():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    for i in range(3):
        patient_id = int(input(f"Enter patient id for appointment {i+1}: "))
        doctor_id = int(input(f"Enter doctor id for appointment {i+1}: "))
        appointment_date = input(f"Enter appointment date (YYYY-MM-DD HH:MM:SS) of patient for appointment {i+1}: ")
        reason = input(f"Enter the reason for appointment {i + 1}: ")
        cursor.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason)
                    VALUES (%s, %s, %s, %s)
                """, (patient_id, doctor_id, appointment_date, reason))

    conn.commit()
    cursor.close()
    conn.close()

def generate_report():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    query = """SELECT p.full_name AS patient_name, p.date_of_birth, p.gender, p.address, 
               d.full_name AS doctor_name, a.reason, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """
    cursor.execute(query)
    result = cursor.fetchall()
    print("\nNo  Patient Name    Birthday  Gender  Address  Doctor Name   Reason   Date")
    for i, row in enumerate(result, start=1):
        print(f"{i} {row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}")
    cursor.close()
    conn.close()

def get_today_appointments():
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    query = """
            SELECT p.full_name AS patient_name, p.date_of_birth, p.gender, 
                   d.full_name AS doctor_name, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE DATE(a.appointment_date) = %s
        """
    cursor.execute(query, (today,))
    result = cursor.fetchall()
    print("\n{:<10} {:<5} {:<20} {:<12} {:<8} {:<20} {:<10} {:<10}".format(
        "Address", "No", "Patient Name", "Birthday", "Gender", "Doctor Name", "Status", "Note"))
    print("=" * 100)

    for i, row in enumerate(result, start=1):
        print("{:<10} {:<5} {:<20} {:<12} {:<8} {:<20} {:<10} {:<10}".format(
            "Ha Noi", i, row[0], row[1], row[2], row[3], row[4], "Pending"))
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # add_patients_and_doctors()
    # add_appointments()
    # generate_report()
    get_today_appointments()
