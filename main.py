"""
main.py — Mechanical Component Inventory & Sustainability Tracker

This module serves as the primary User Interface (UI). It coordinates
data flow between the user, the OOP models, and the CSV registry.

KEY FEATURES:
    - Data Persistence: Loads existing records on startup (Hydration).
    - Regex Validation: Uses utils.py to verify ID formats.
    - Search Logic: Filters the registry by part name.
    - Error Handling: Catches ValueErrors to prevent system crashes.
"""

import os
from utils import is_valid_part_id
from models import MechanicalPart

def load_existing_data(file="registry.csv"):
    """
    Reads the CSV and rebuilds the objects in memory (Hydration).
    Matches the pattern of load_students() in the lecturer's example.
    """
    parts_list = []
    try:
        if not os.path.exists(file):
            return []
        with open(file, "r") as f:
            for line in f:
                if not line.strip(): continue 
# Unpack: ID, Name, Material, Mass, CO2
                d = line.strip().split(",")
# Re-create object (Volume is 0.0 as it's not stored in this version)
                p = MechanicalPart(d[0], d[1], "N/A", d[2], 0.0)
                parts_list.append(p)
        print(f"\n[System Boot] {len(parts_list)} records synchronized from {file}.")
    except Exception as e:
        print(f"Warning: Could not load registry. {e}")
    return parts_list

def show_report(file="registry.csv"):
    """Aggregates totals from the CSV database."""
    total_m = 0.0
    total_c = 0.0
    try:
        with open(file2, "r") as f:
            for line in f:
                if not line.strip(): continue
                _, _, _, mass, co2 = line.strip().split(",")
                total_m += float(mass)
                total_c += float(co2)
        
        print("\n" + "="*30)
        print("   PROJECT SUSTAINABILITY REPORT")
        print("="*30)
        print(f"Total Mass:        {total_m:.2f} kg")
        print(f"Total CO2 Impact:  {total_c:.2f} kg CO2e")
        print("="*30)
    except FileNotFoundError:
        print("\n[!] Error: No registry found. Please log a part first.")

def main():
# Run the system and keep the inventory in memory for quick access
    current_inventory = load_existing_data()

    while True:
        print("\n--- MECHANICAL INVENTORY MENU ---")
        print("1. Log New Component")
        print("2. Generate Registered Parts Report")
        print("3. Search by Part Name")
        print("4. Shutdown System")
        
        choice = input("\nSelect Action (1-4): ")

        if choice == "1":
            uid = input("Enter Serial ID (e.g., XXXX-0000): ")
            if not is_valid_part_id(uid):
                print(">> ERROR: Invalid ID format. Use 4 CAPS-4 Digits.")
                continue

            try:
                name = input("Part Name: ")
                brand = input("Manufacturer: ")
                mat = input("Material (Steel/Aluminum/Titanium): ")
                vol = input("Design Volume (m^3): ")
                
# Convert volume to float here to catch errors
                new_part = MechanicalPart(uid, name, brand, mat, float(vol))
                
                with open("registry.csv", "a") as f:
                    f.write(new_part.to_csv_format() + "\n")
                
                current_inventory.append(new_part)
                print(f">> SUCCESS: {new_part.name} added to parts registry.")

            except ValueError as e:
# Catches both empty names and non-numeric volumes
                print(f">> SYSTEM ERROR: {e}")

        elif choice == "2":
            show_report()

        elif choice == "3":
            query = input("Enter search term: ").lower()
            found = False
            print("\n--- SEARCH RESULTS ---")
            for part in active_inventory:
                if query in part.name.lower() or query in part.uid.lower():
                    print(f"Match: {part.uid} | {part.name} ({part.material})")
                    found = True
            if not found:
                print("No matching components found.")

        elif choice == "4":
            print("Shutting down. Data logged into registry.csv.")
            break

if __name__ == "__main__":
    main()