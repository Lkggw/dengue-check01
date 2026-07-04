# 🦟 Dengue Cases Analysis System

A comprehensive system for tracking and analyzing dengue patient cases with web interface, database management, and geographic mapping.

## Features

✅ **Patient Management** - Add, edit, view, and delete patient records  
✅ **SQLite Database** - Persistent data storage  
✅ **Web Interface** - Beautiful Flask-based dashboard  
✅ **Geographic Mapping** - Visualize patient locations on interactive map  
✅ **Address Geocoding** - Automatic address-to-coordinates conversion using OpenStreetMap  
✅ **Responsive Design** - Mobile-friendly interface

## Quick Start

### Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Web Application
```bash
python app.py
```

Then open your browser: `http://localhost:5000`

## Project Structure

```
├── app.py                 # Flask web application
├── main.py               # CLI application
├── database.py           # Database operations
├── requirements.txt      # Dependencies
└── templates/            # HTML templates
    ├── base.html, index.html, add.html, edit.html, map.html
```

## Web Features

- 📊 **Dashboard** - View all patients at a glance
- ➕ **Add Patient** - Register new dengue patients
- ✏️ **Edit Patient** - Update patient information
- 🗑️ **Delete Patient** - Remove records
- 🗺️ **Map View** - Visualize patient locations

## Technologies

- Python 3.8+, Flask
- SQLite Database
- Folium & OpenStreetMap for mapping
- HTML5, CSS3, JavaScript

## License

MIT License 
