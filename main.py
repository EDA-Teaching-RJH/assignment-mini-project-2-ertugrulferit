from utils import validate_part_id
from models import MechanicalPart

def main():
    print("--- Engineering Inventory System ---")

    while True:
        pid = input("\nEnter Part ID (or type 'exit' to quit): ")
        
        if pid.lower() == 'exit':
            break
            
        if validate_part_id(pid):
            name = input("Enter Name: ")
            mfr = input("Enter Manufacturer: ")
            mat = input("Enter Material: ")

            try:
                weight_input = input("Enter Weight (kg): ")
                weight = float(weight_input)
            except ValueError:
                print("Invalid weight! Setting weight to 0.0.")
                weight = 0.0
                
            part = MechanicalPart(pid, name, mfr, mat, weight)
            with open("inventory.txt", "a") as file:
                file.write(part.get_details() + "\n")

            print("\nSUCCESS: Part Created and Saved to file!")
            print(part.get_details())
        else:
            print(f"\nERROR: '{pid}' is not a valid format. Use XXXX-1111.")

if __name__ == "__main__":
    main()