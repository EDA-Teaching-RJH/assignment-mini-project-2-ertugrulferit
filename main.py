"""
main.py — Mechanical Component Inventory & Sustainability Tracker
VERSION: 2.3.0 (Standard Library Edition)

This module provides a robust CLI for engineering asset management.
It uses only Python's built-in libraries to ensure maximum portability.
"""

import sys      # For command-line argument processing
import csv      # For high-integrity CSV data handling
import os       # For defensive file-system operations
import random   # For simulating dynamic market price fluctuations
import datetime # For recording high-precision timestamps

from utils import is_valid_part_id
from models import MechanicalPart

def get_market_simulation(material):
    """
    Simulates a live market price fetch using the random module.
    Demonstrates how to handle external data logic without dependencies.
    """
    price_map = {"STEEL": (2, 5), "ALUMINUM": (5, 10), "TITANIUM": (20, 50)}
    base_range = price_map.get(material.upper(), (1, 10))
    simulated_price = random.uniform(base_range[0], base_range[1])
    
    print(f"\n[Market Insight] Current {material} Index: ${simulated_price:.2f}/kg")
    return simulated_price

def compare_material_efficiency(current_part):
    """
    NEW FUNCTION: Analyzes the current part and suggests a material alternative.
    Similar to the lecturer's 'Recommended Song' but uses engineering logic.
    """
    materials = ["STEEL", "ALUMINUM", "TITANIUM"]
    # Pick a random alternative that isn't the current material
    alternatives = [m for m in materials if m != current_part.material]
    suggestion = random.choice(alternatives)
    
    # Simple logic: Aluminum is always lighter than Steel
    print(f"--- Engineering Suggestion for {current_part.name} ---")
    if current_part.material == "STEEL" and suggestion == "ALUMINUM":
        print(f"Switching to ALUMINUM could reduce mass by approx. 65%.")
    elif suggestion == "TITANIUM":
        print(f"TITANIUM would offer higher strength-to-weight for this component.")
    else:
        print(f"Consider {suggestion} for different thermal properties.")
    print("--------------------------------------------------")

def validate_registry(file="registry.csv"):
    """Defensive check to ensure the data persistence layer is initialized."""
    if not os.path.exists(file):
        try:
            with open(file, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Material", "Mass_kg", "CO2_kg", "Timestamp"])
            print(f"[!] System: Initialized fresh registry at {file}")
            return True
        except Exception as e:
            print(f"CRITICAL FILE ERROR: {e}")
            return False
    return True

def load_existing_data(file="registry.csv"):
    """Synchronizes the in-memory state with the CSV storage (Hydration)."""
    parts_list = []
    if not os.path.exists(file): return []
    
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                if not row or len(row) < 5: continue
                p = MechanicalPart(row[0], row[1], "N/A", row[2], 0.0)
                parts_list.append(p)
        print(f"[System Boot] {len(parts_list)} records synchronized.")
    except Exception as e:
        print(f"Synchronization Warning: {e}")
    return parts_list

def show_report(file="registry.csv"):
    """Aggregates and formats the project sustainability report."""
    total_m, total_c, count = 0.0, 0.0, 0
    if not os.path.exists(file): 
        print("\n[!] No data found to generate report.")
        return
        
    with open(file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            total_m += float(row[3])
            total_c += float(row[4])
            count += 1
            
    print("\n" + "="*45)
    print(f"{'PROJECT SUSTAINABILITY REPORT':^45}")
    print("="*45)
    print(f" Total Components Logged: {count:>15}")
    print(f" Total System Mass:      {total_m:>12.2f} kg")
    print(f" Total Carbon Footprint: {total_c:>12.2f} kg CO2e")
    print("="*45 + "\n")

def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "report":
            show_report()
            sys.exit()
        elif mode == "list":
            inv = load_existing_data()
            for p in inv: print(p)
            sys.exit()

    validate_registry()
    inventory = load_existing_data()

    while True:
        print("\n--- MECHANICAL INVENTORY CONTROL SYSTEM ---")
        print("1. Log New Component")
        print("2. Generate Sustainability Report")
        print("3. Component Search Engine")
        print("4. System Shutdown")
        
        choice = input("\nSelect Action (1-4): ").strip()

        if choice == "1":
            uid = input("Enter Serial ID (XXXX-0000): ").upper()
            if not is_valid_part_id(uid):
                print(">> ERROR: Invalid ID format.")
                continue

            try:
                name = input("Part Designation: ")
                brand = input("Manufacturer: ")
                mat = input("Material (Steel/Aluminum/Titanium): ")
                vol = input("Design Volume (m^3): ")
                
                new_part = MechanicalPart(uid, name, brand, mat, vol)
                
                get_market_simulation(new_part.material)
                
                # --- CALL THE NEW COMPARISON FUNCTION ---
                compare_material_efficiency(new_part)

                with open("registry.csv", "a", newline='') as f:
                    writer = csv.writer(f)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    writer.writerow(new_part.to_csv_format() + [now])
                
                inventory.append(new_part)
                print(f"\n>> SUCCESS: {name} registered in system.")

            except ValueError as e:
                print(f"\n>> VALIDATION ERROR: {e}")

        elif choice == "2":
            show_report()

        elif choice == "3":
            query = input("Search term: ").lower()
            results = [p for p in inventory if query in p.name.lower() or query in p.uid.lower()]
            print(f"\n--- Search Results ({len(results)} found) ---")
            for p in results: print(p)

        elif choice == "4":
            print("Exporting state... Shutdown complete.")
            break
            
        else:
            print("Invalid input. Please choose 1-4.")

if __name__ == "__main__":
    main()