import sqlite3
from datetime import datetime

DATABASE_FILE = "dengue_cases.db"

def init_database():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            age TEXT NOT NULL,
            address TEXT NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DATABASE_FILE}\n")

def add_patient(name, age, address):
    """Add a new patient record to the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (name, age, address)
            VALUES (?, ?, ?)
        ''', (name, age, address))
        
        conn.commit()
        conn.close()
        print("Patient record added successfully!\n")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Patient '{name}' already exists in the database.\n")
        return False
    except Exception as e:
        print(f"Error adding patient: {e}\n")
        return False

def get_all_patients():
    """Retrieve all patient records from the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients')
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error retrieving patients: {e}\n")
        return []

def get_patient_by_name(name):
    """Retrieve a specific patient by name."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    except Exception as e:
        print(f"Error retrieving patient: {e}\n")
        return None

def update_patient(name, age, address):
    """Update an existing patient record."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE patients
            SET age = ?, address = ?
            WHERE name = ?
        ''', (age, address, name))
        
        if cursor.rowcount == 0:
            print(f"Error: Patient '{name}' not found.\n")
            return False
        
        conn.commit()
        conn.close()
        print("Patient record updated successfully!\n")
        return True
    except Exception as e:
        print(f"Error updating patient: {e}\n")
        return False

def delete_patient(name):
    """Delete a patient record from the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM patients WHERE name = ?', (name,))
        
        if cursor.rowcount == 0:
            print(f"Error: Patient '{name}' not found.\n")
            return False
        
        conn.commit()
        conn.close()
        print("Patient record deleted successfully!\n")
        return True
    except Exception as e:
        print(f"Error deleting patient: {e}\n")
        return False
