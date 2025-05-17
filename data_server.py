#data_server.py
import sqlite3

con = sqlite3.connect("PITD.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE tax_payers (
            id INTEGER PRIMARY KEY,
            tfn INTEGER UNIQUE NOT NULL,
            record_id INTEGER
)
            """)

cur.execute("""
CREATE TABLE payroll_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            taxpayer_TFN INTEGER NOT NULL,
            pay_period INTEGER,
            payday TEXT,
            gross_wage REAL,
            tax_levied REAL,
            net_wage REAL,
            FOREIGN KEY (taxpayer_TFN) REFERENCES tax_payers (tfn)
)
            """)

