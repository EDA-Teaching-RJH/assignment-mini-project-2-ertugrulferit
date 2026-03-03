from models import MechanicalPart
from utils import validate_part_id
def main():
    print("--- Engineering Inventory System ---")

    while True:
        pid = input("\nEnter Part ID (or type 'exit' to quit): ")
        
        if pid.lower() == 'exit':
            break
            
        if validate_part_id(pid):
            # If the ID is good, ask for the rest of the details
            name = input("Enter Name: ")
            mfr = input("Enter Manufacturer: ")
            mat = input("Enter Material: ")
            
            # Create the object using class
            part = MechanicalPart(pid, name, mfr, mat, 0.0)
            print("\nSUCCESS: Part Created!")
            print(part.get_details())
        else:
            print(f"\nERROR: '{pid}' is not a valid format. Use XXXX-1111.")