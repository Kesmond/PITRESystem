#data_server.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "PITD.db"

@app.route("/view_all_records")
def view_all_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tax_payers")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/get_record", methods=["GET"])
def get_record():
    tfn = request.args.get("tfn")
    if not tfn:
        return jsonify({"error": "TFN parameter is required"}), 400
    
    try:
        tfn = int(tfn)
    except ValueError:
        return jsonify({"error": "TFN must be a number"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Get taxpayer info
    cursor.execute("SELECT fname, lname, email FROM tax_payers WHERE tfn = ?", (tfn,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({"error": "Taxpayer not found"}), 400
    
    fname, lname, email = result
    
    #Get payroll records
    cursor.execute("""
    SELECT gross_salary, tax_levied
                   FROM payroll_records
                   WHERE tfn = ?
                   ORDER BY pay_period
                   """, (tfn,))
    
    biweekly_tax_pairs = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        "tfn": tfn,
        "biweekly_tax_pairs": biweekly_tax_pairs,
        "fname": fname,
        "lname": lname,
        "email": email
    })

def initialise_database():
    #Initialise database with table and data if they don't exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Create table tax_payers if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tax_payers (
                tfn INTEGER PRIMARY KEY,
                id INTEGER,
                fname TEXT,
                lname TEXT,
                email TEXT
    )""")
    
    #Create table payroll_records if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll_records (
                payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tfn INTEGER,
                pay_period INTEGER,
                payday TEXT,
                gross_salary REAL,
                tax_levied REAL,
                net_pay REAL,
                FOREIGN KEY (tfn) REFERENCES tax_payers(tfn)
    )""")
    
    if not cursor.execute("SELECT 1 FROM tax_payers LIMIT 1").fetchone():
        #Sample taxpayers
        taxpayers = [
            (23456789, 123456, 'Abraham', 'Lincoln', 'alincoln@gmail.com'),
            (19283746, 240704, 'Kenneth', 'Esmond', 'kesmond@gmail.com'),
            (97531246, 987654, 'Katie', 'Smith', 'ksmith@gmail.com'),
        ]
        cursor.executemany("INSERT INTO tax_payers VALUES (?, ?, ?, ?, ?)", taxpayers)

        payroll_data = [
            (23456789, 1, '2024-01-02', 1000.0, 200.0, 800.0),
            (23456789, 2, '2024-01-09', 2000.0, 400.0, 1600.0),
            (23456789, 3, '2024-01-16', 1500.0, 300.0, 1200.0),
            (23456789, 4, '2024-01-23', 200.0, 10.0, 190.0),
            (23456789, 5, '2024-01-30', 5000.0, 200.0, 4800.0),
            (19283746, 1, '2024-02-06', 900.0, 200.0, 700.0),
            (19283746, 2, '2024-02-13', 1100.0, 210.0, 890.0),
            (19283746, 3, '2024-02-20', 1200.0, 201.0, 999.0),
            (19283746, 4, '2024-02-27', 1300.0, 203.0, 1097.0),
            (19283746, 5, '2024-03-05', 1400.0, 206.0, 1194.0),
            (97531246, 1, '2024-03-12', 1500.0, 207.0, 1293.0),
            (97531246, 2, '2024-03-19', 2000.0, 180.0, 1820.0),
            (97531246, 3, '2024-03-26', 3000.0, 300.0, 2700.0),
            (97531246, 4, '2024-04-02', 4000.0, 700.0, 3300.0),
            (97531246, 5, '2024-04-09', 5000.0, 650.0, 4350.0),
        ]
        cursor.executemany("""
        INSERT INTO payroll_records
        (tfn, pay_period, payday, gross_salary, tax_levied, net_pay)
        VALUES (?, ?, ?, ?, ?, ?)
        """, payroll_data)

        conn.commit()
    conn.close()

if __name__ == "__main__":
    initialise_database()
    app.run(host="0.0.0.0", port=5001, debug=True)