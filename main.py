"""
main.py — Mechanical Component Inventory & Sustainability Tracker
VERSION: 2.5.2 (Standard Library Edition)

This module provides a robust CLI for engineering asset management.
It uses only Python's built-in libraries to ensure maximum portability.
"""

import sys      # For command-line argument processing
import csv      # For high-integrity CSV data handling
import os       # For defensive file-system operations
import random   # For simulating dynamic market price fluctuations
import datetime # For recording high-precision timestamps

from utils import is_valid_part_id
from models import StandardPart, CustomComponent, MechanicalPart

def print_success_crane():
    """
    Displays a large-scale engineering crane visual upon successful logging.
    """
    goofycrane = r"""
              __________________________________________
             |                                          |
             |        COMPONENT LOGGED!!! :)            |
             |__________________________________________|
                   | |                          | |
             ______| |__________________________| |__________
            |                                                |
            |   [ CONSTRUCTION IN PROGRESS - DATA SAVED ]    |
            |________________________________________________|
                         | |                  | |
                _________| |__________________| |_________
               |                                          |
               |        INVENTORY CONTROL SYSTEM          |
               |__________________________________________|
                          ||                  ||
                          ||                  ||
                 _________||__________________||_________
                |________________________________________|
    """
    print(goofycrane)

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
    Analyzes the current part and suggests a material alternative.
    """
    materials = ["STEEL", "ALUMINUM", "TITANIUM"]
    alternatives = [m for m in materials if m != current_part.material]
    suggestion = random.choice(alternatives)
    
    print(f"--- Engineering Suggestion for {current_part.name} ---")
    if current_part.material == "STEEL" and suggestion == "ALUMINUM":
        print(f"Switching to ALUMINUM could reduce mass by approx. 65%.")
    elif suggestion == "TITANIUM":
        print(f"TITANIUM would offer higher strength-to-weight for this component.")
    else:
        print(f"Consider {suggestion} for different thermal properties.")
    print("--------------------------------------------------")

def calculate_material_ratios(inventory):
    """
    Generates a visual distribution chart of materials used.
    """
    if not inventory:
        print("\n[!] No parts available for ratio analysis.")
        return

    print("\n" + "█"*45)
    print(f"{'MATERIAL DISTRIBUTION ANALYSIS':^45}")
    print("█"*45)
    
    counts = {}
    for p in inventory:
        counts[p.material] = counts.get(p.material, 0) + 1
    
    for mat, count in counts.items():
        percent = (count / len(inventory)) * 100
        bar = "■" * int(percent / 5)
        print(f"{mat:<10} | {bar:<20} | {percent:>5.1f}%")
    print("█"*45)

def validate_registry(file="registry.csv"):
    if not os.path.exists(file):
        try:
            with open(file, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "ID", "Name", "Material", "Mass_kg", "CO2_kg", "MetaData"])
            print(f"[!] System: Initialized fresh registry at {file}")
            return True
        except Exception as e:
            print(f"CRITICAL FILE ERROR: {e}")
            return False
    return True

def load_existing_data(file="registry.csv"):
    """
    SDS-Style Hydrator: Detects Part Type and recreates specific subclasses.
    """
    parts_list = []
    if not os.path.exists(file): return []
    
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                if not row or len(row) < 7: continue
                # Logic to rebuild specific subclass based on the 'Type' column
                if row[0] == "STD":
                    p = StandardPart(row[1], row[2], "N/A", row[3], 0.0, row[6])
                else:
                    p = CustomComponent(row[1], row[2], "N/A", row[3], 0.0, row[6])
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
            if len(row) >= 6:
                total_m += float(row[4])
                total_c += float(row[5])
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
        print("1. Log Standard Component")
        print("2. Log Custom Component")
        print("3. Generate Sustainability Report")
        print("4. View Material Analytics")
        print("5. System Shutdown")
        
        choice = input("\nSelect Action (1-5): ").strip()

        if choice in ["1", "2"]:
            uid = input("Enter Serial ID (XXXX-0000): ").upper()
            if not is_valid_part_id(uid):
                print(">> ERROR: Invalid ID format.")
                continue

            try:
                name = input("Part Designation: ")
                brand = input("Manufacturer: ")
                mat = input("Material (Steel/Aluminum/Titanium): ")
                vol = input("Design Volume (m^3): ")
                
                if choice == "1":
                    extra = input("Shelf Location: ")
                    new_part = StandardPart(uid, name, brand, mat, vol, extra)
                    p_type = "STD"
                else:
                    extra = input("Lead Time (Days): ")
                    new_part = CustomComponent(uid, name, brand, mat, vol, extra)
                    p_type = "CUSTOM"
                
                get_market_simulation(new_part.material)
                compare_material_efficiency(new_part)

                with open("registry.csv", "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([p_type, new_part.uid, new_part.name, 
                                     new_part.material, new_part.get_mass(), 
                                     new_part.get_carbon(), extra])
                
                inventory.append(new_part)
                print_success_crane() 

            except ValueError as e:
                print(f"\n>> VALIDATION ERROR: {e}")

        elif choice == "3":
            show_report()

        elif choice == "4":
            calculate_material_ratios(inventory)

        elif choice == "5":
            print("Exporting state... Shutdown complete.")
            break
            
        else:
            print("Invalid input. Please choose 1-5.")

if __name__ == "__main__":
    main()