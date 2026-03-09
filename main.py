from utils import is_valid_part_id
from models import MechanicalPart

def show_report():
    """Reads the CSV and calculates the project totals."""
    total_m = 0.0
    total_c = 0.0
    try:
        with open("registry.csv", "r") as f:
            for line in f:
                if not line.strip(): continue 
                _, _, _, mass, co2 = line.strip().split(",")
                total_m += float(mass)
                total_c += float(co2)
        
        print("\n--- PROJECT SUMMARY ---")
        print(f"Total System Mass: {total_m:.2f} kg")
        print(f"Total Carbon Footprint: {total_c:.2f} kg CO2e")
    except FileNotFoundError:
        print("\n[!] No data found. Log a part first.")

def load_existing_data():
    """Hydrates the system with existing parts from the CSV."""
    parts_list = []
    try:
        with open("registry.csv", "r") as f: 
            for line in f:
                if not line.strip(): continue
                d = line.strip().split(",")
                p = MechanicalPart(d[0], d[1], "N/A", d[2], 0.0)
                parts_list.append(p)
        print(f"\n[System Boot] {len(parts_list)} existing records loaded.")
    except FileNotFoundError:
        print("\n[System Boot] No existing registry found. Starting fresh.")
    return parts_list

def main():
    # RUN HYDRATION AT STARTUP
    current_inventory = load_existing_data()

    while True:
        print("\n1. Log New Part\n2. View Project Totals\n3. Search Parts\n4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            uid = input("Enter ID (XXXX-0000): ")
            if not is_valid_part_id(uid):
                print("Invalid format. Please use 4 CAPS-4 Digits.")
                continue

            try:
                name = input("Part Name: ")
                brand = input("Manufacturer: ")
                mat = input("Material (Steel/Aluminum/Titanium): ")
                vol = float(input("Design Volume (m^3): "))

                part = MechanicalPart(uid, name, brand, mat, vol)
                
                with open("registry.csv", "a") as f:
                    f.write(part.to_csv_format() + "\n")
                
                # Add to the live inventory list too!
                current_inventory.append(part)
                print(f"Success: {part.name} recorded.")
            except ValueError:
                print("Error: Volume must be a number.")

        elif choice == "2":
            show_report()

        elif choice == "3": # Changed from 3 to 3 (Search)
            search_name = input("Enter part name to search: ").lower()
            found = False
            try:
                with open("registry.csv", "r") as f:
                    for line in f:
                        if search_name in line.lower():
                            print(f"Found Match: {line.strip()}")
                            found = True
                if not found: print("No matching parts in registry.")
            except FileNotFoundError:
                print("Registry is empty.")

        elif choice == "4": # Changed from 3 to 4 (Exit)
            print("Closing system...")
            break

if __name__ == "__main__":
    main()