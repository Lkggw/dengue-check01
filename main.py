import webbrowser
import folium
import requests
from database import init_database, add_patient, get_all_patients, get_patient_by_name, update_patient, delete_patient

def geocode_osm(address):
    """Converts a text address to Lat/Lng coordinates using the OpenStreetMap Nominatim API."""
    url = "https://openstreetmap.org"
    headers = {
        "User-Agent": "DengueTrackerApp/1.0 (kithnuke001@gmail.com)"
    }
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data["lat"]), float(data["lon"])
    except Exception as e:
        print(f"OSM Geocoding network error: {e}")
    return None




def show_plotted_demographics():
    """Converts patient addresses to coordinates using OSM and maps them."""
    patients = get_all_patients()
    if not patients:
        print("No patient records available to plot on a map.\n")
        return

    print("Analyzing addresses via OpenStreetMap API and generating map...")
    
    valid_coords = []
    markers_to_add = []

    for patient in patients:
        name = patient['name']
        address = patient['address']
        age = patient['age']
        
        coords = geocode_osm(address)
        
        if coords:
            lat, lng = coords
            valid_coords.append((lat, lng))
            
            popup_html = f"<b>Patient:</b> {name}<br><b>Age:</b> {age}<br><b>Address:</b> {address}"
            
            markers_to_add.append({
                'pos': [lat, lng],
                'popup': folium.Popup(popup_html, max_width=250),
                'tooltip': f"Dengue Case: {name}"
            })
        else:
            print(f"Could not locate address on OSM for patient: {name} ({address})")

    # Render map if coordinates were successfully resolved
    if valid_coords:
        avg_lat = sum(c[0] for c in valid_coords) / len(valid_coords)
        avg_lng = sum(c[1] for c in valid_coords) / len(valid_coords)
        
        # folium naturally uses OpenStreetMap base layers by default
        dengue_map = folium.Map(location=[avg_lat, avg_lng], zoom_start=12)

        for marker in markers_to_add:
            folium.Marker(
                location=marker['pos'],
                popup=marker['popup'],
                tooltip=marker['tooltip'],
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(dengue_map)

        map_filename = "dengue_demographics.html"
        dengue_map.save(map_filename)
        print(f"Map compiled via OpenStreetMap! Launching {map_filename}...\n")
        webbrowser.open(map_filename)
    else:
        print("Failed to resolve any physical addresses into coordinates. Map generation aborted.\n")





            

    

def enter_records():
    name = input("Enter the name of the patient: ")
    age = input("Enter the age of the patient: ")
    address = input("Enter the address: ")
    add_patient(name, age, address)

def update_records():
    name_check = input("Enter the name of the Record holder, to change or update its content: ")
    patient = get_patient_by_name(name_check)
    if patient:
        print("Record found. Update the details:")
        new_age = input("Enter new age: ")
        new_address = input("Enter new address: ")
        update_patient(name_check, new_age, new_address)
    else:
        print("Record not found. Please check the name and try again.\n")

def show_records():
    patients = get_all_patients()
    if patients:
        print("\nAll Records:")
        for patient in patients:
            print(f"Name: {patient['name']}, Age: {patient['age']}, Address: {patient['address']}, Added: {patient['date_added']}")
        print()
    else:
        print("No records found.\n")

def delete_records():
    name_check = input("Enter the name of the Record holder, to delete its content: ")
    delete_patient(name_check)
if __name__ == "__main__":
    init_database()
    
    off = 0
    while off != 1:
        print("Welcome to Dengue Cases Analysis System")
        off = int(input("To Continue with the system, press '0' and to log off press '1': "))
        if off == 1:
            print("Thank you for using the Dengue Cases Analysis System. Goodbye!\n")
            break
        else:
            print("1. Enter Record\n2. Update Record\n3. Show all records\n4. Show plotted Demographics\n5. Delete records ")
            switch_mode = int(input("Select an option (1-5): "))
            if switch_mode == 1:
                enter_records()

            elif switch_mode == 2:
                update_records()
            elif switch_mode == 3:
                show_records()
            elif switch_mode == 4:
                show_plotted_demographics()
            elif switch_mode == 5:
                delete_records()
            else:
                print("Invalid option. Please select a valid option (1-5).\n")



