from utils import is_valid_part_id
from models import MechanicalPart

def show_report():
    total_m = 0
    total_c = 0
    try:
        with open("registry.csv", "r") as f:
            for line in f:
# Unpack the CSV columns
                _, _, _, mass, co2 = line.strip().split(",")
                total_m += float(mass)
                total_c += float(co2)
        
        print("\n--- PROJECT SUMMARY ---")
        print(f"Total System Mass: {total_m:.2f} kg")
        print(f"Total Carbon Footprint: {total_c:.2f} kg CO2e")
    except FileNotFoundError:
        print("\n[!] No data found. Please add a part first.")

def main():
    while True:
        print("\n1. Log New Part\n2. View Project Totals\n3. Exit")
        cmd = input("Select action: ")

        if cmd == "1":
            uid = input("Enter ID (e.g. MECH-1234): ")
            if not is_valid_part_id(uid):
                print("Invalid format. Use XXXX-0000.")
                continue

            try:
                name = input("Part Name:")
                brand = input("Manufacturer:")
                mat = input("Material (Steel/Aluminum/Titanium):")
                vol = float(input("Design Volume (m^3):"))

                part = MechanicalPart(uid, name, brand, mat, vol)
                
                with open("registry.csv", "a") as f:
                    f.write(part.to_csv_format() + "\n")
                
                print(f"Success: {part.name} logged.")
            except ValueError:
                print("Error: Volume must be a numeric value.")

        elif cmd == "2":
            show_report()
        elif cmd == "3":
            break

if __name__ == "__main__":
    main()