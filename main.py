from utils import is_valid_part_id
from models import MechanicalPart

def show_report():
    """Reads the CSV and calculates the project totals."""
    total_m = 0.0
    total_c = 0.0
    try:
        with open("registry.csv", "r") as f:
            for line in f:
                if not line.strip(): continue # Skip empty lines
                _, _, _, mass, co2 = line.strip().split(",")
                total_m += float(mass)
                total_c += float(co2)
        
        print("\n--- PROJECT SUMMARY ---")
        print(f"Total System Mass: {total_m:.2f} kg")
        print(f"Total Carbon Footprint: {total_c:.2f} kg CO2e")
    except FileNotFoundError:
        print("\n[!] No data found. Log a part first.")

def main():
    while True:
        print("\n1. Log New Part\n2. View Project Totals\n3. Exit")
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
                
                print(f"Success: {part.name} recorded at {part.get_mass()}kg.")
            except ValueError:
                print("Error: Volume must be a number.")

        elif choice == "2":
            show_report()
        elif choice == "3":
            print("Closing system...")
            break

if __name__ == "__main__":
    main()