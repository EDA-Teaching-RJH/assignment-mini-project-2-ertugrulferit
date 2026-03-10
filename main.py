"""
main.py — Mechanical Component Inventory & Sustainability Tracker
VERSION: 2.0.0 (Extended Enterprise Edition)
"""

import os
import csv
import datetime # Adds a professional 'timestamp' feature
from utils import is_valid_part_id
from models import MechanicalPart

def validate_registry(file="registry.csv"):
    """Ensures the database file is ready for use (Defensive Programming)."""
    if not os.path.exists(file):
        try:
            with open(file, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Material", "Mass", "CO2", "Date_Added"])
            print(f"[!] System: Initialized new encrypted registry.")
            return True
        except Exception as e:
            print(f"File System Error: {e}")
            return False
    return True

def get_detailed_analytics(inventory):
    """
    NEW FEATURE: Adds a deeper 'Calculated Field' analysis layer.
    This demonstrates advanced data processing over a list of objects.
    """
    if not inventory:
        print("Analytics unavailable: Inventory is empty.")
        return

    print("\n--- ADVANCED COMPONENT ANALYTICS ---")
    materials_count = {}
    for part in inventory:
        materials_count[part.material] = materials_count.get(part.material, 0) + 1
    
    for mat, count in materials_count.items():
        percentage = (count / len(inventory)) * 100
        print(f"Material Distribution [{mat}]: {count} items ({percentage:.1f}%)")
    
    avg_mass = sum(p.get_mass() for p in inventory) / len(inventory)
    print(f"Average Component Mass: {avg_mass:.2f} kg")
    print("------------------------------------\n")

def load_existing_data(file="registry.csv"):
    """Parses the CSV and rebuilds objects in memory (Hydration)."""
    parts_list = []
    if not validate_registry(file):
        return []

    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            for row in reader:
                if not row: continue
                # Re-create object (Using your original structure)
                p = MechanicalPart(row[0], row[1], "N/A", row[2], 0.0)
                parts_list.append(p)
        print(f"[System Boot] {len(parts_list)} records synchronized.")
    except Exception as e:
        print(f"Warning: Synchronization failed. {e}")
    return parts_list

def show_report(file="registry.csv"):
    """Aggregates totals and generates a formatted UI report."""
    total_m = 0.0
    total_c = 0.0
    count = 0
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                total_m += float(row[3])
                total_c += float(row[4])
                count += 1
        
        print("\n" + "╔" + "═"*38 + "╗")
        print(f"║ {'PROJECT SUSTAINABILITY REPORT':^36} ║")
        print("╠" + "═"*38 + "╣")
        print(f"║ Total Components: {count:>18} ║")
        print(f"║ Total System Mass: {total_m:>15.2f} kg ║")
        print(f"║ Total CO2 Impact: {total_c:>16.2f} kg ║")
        print("╚" + "═"*38 + "╝")
    except Exception:
        print("\n[!] Error: Registry empty or inaccessible.")

def main():
    current_inventory = load_existing_data()

    while True:
        print("\n--- MECHANICAL INVENTORY CONTROL SYSTEM ---")
        print("1. Log New Component")
        print("2. Run Project Sustainability Report")
        print("3. Execute Component Search")
        print("4. View Advanced Material Analytics") # New Menu Item
        print("5. System Shutdown")
        
        choice = input("\nSelect Action (1-5): ")

        if choice == "1":
            uid = input("Enter Serial ID (XXXX-0000): ").upper()
            if not is_valid_part_id(uid):
                print(">> ERROR: Invalid format.")
                continue

            try:
                name = input("Part Name: ")
                brand = input("Manufacturer: ")
                mat = input("Material (Steel/Aluminum/Titanium): ")
                vol = input("Design Volume (m^3): ")
                
# Convert volume to float to catch errors
                new_part = MechanicalPart(uid, name, brand, mat, float(vol))
                
                # Using CSV module for professional writing
                with open("registry.csv", "a", newline='') as f:
                    writer = csv.writer(f)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    writer.writerow([
                        new_part.uid, new_part.name, new_part.material, 
                        new_part.get_mass(), new_part.get_carbon(), now
                    ])
                
                current_inventory.append(new_part)
                print(f">> SUCCESS: {new_part.name} recorded.")
            except ValueError as e:
                print(f">> SYSTEM ERROR: {e}")

        elif choice == "2":
            show_report()

        elif choice == "3":
            query = input("Search term (Name or ID): ").lower()
            found = False
            for p in current_inventory:
                if query in p.name.lower() or query in p.uid.lower():
                    print(f"-> Found: {p.uid} | {p.name} ({p.material})")
                    found = True
            if not found:
                print("No results.")

        elif choice == "4":
            get_detailed_analytics(current_inventory)

        elif choice == "5":
            print("Exporting state... Shutdown complete.")
            break
        
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()