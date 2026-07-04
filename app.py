from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    init_database, add_patient, get_all_patients, 
    get_patient_by_name, update_patient, delete_patient
)
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dengue-tracker-secret'

# Initialize database on startup
init_database()

@app.route('/')
def index():
    """Home page - Dashboard with all patients."""
    patients = get_all_patients()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    """Add a new patient record."""
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        address = request.form.get('address')
        
        if add_patient(name, age, address):
            return redirect(url_for('index'))
        else:
            return render_template('add.html', error="Patient already exists or invalid data")
    
    return render_template('add.html')

@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_record(name):
    """Edit an existing patient record."""
    patient = get_patient_by_name(name)
    
    if not patient:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_age = request.form.get('age')
        new_address = request.form.get('address')
        
        if update_patient(name, new_age, new_address):
            return redirect(url_for('index'))
        else:
            return render_template('edit.html', patient=patient, error="Failed to update record")
    
    return render_template('edit.html', patient=patient)

@app.route('/delete/<name>', methods=['POST'])
def delete_record(name):
    """Delete a patient record."""
    delete_patient(name)
    return redirect(url_for('index'))

@app.route('/api/patients')
def api_patients():
    """API endpoint to get all patients as JSON."""
    patients = get_all_patients()
    return jsonify(patients)

@app.route('/map')
def show_map():
    """Display patients on a map."""
    patients = get_all_patients()
    return render_template('map.html', patients=patients)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
