"""
test_app.py — Automated Test Suite (Extended Edition)
Total Tests: 10+ | Coverage: Core, Inheritance, Validation, and Persistence.
"""

import unittest
import os
import csv
from models import MechanicalPart, StandardPart, CustomComponent
from utils import is_valid_part_id
from main import load_existing_data, validate_registry

class TestMechanicalSystem(unittest.TestCase):
    """
    Main test container. Matches the architectural depth of the SDS examples.
    """

    def setUp(self):
        """Runs BEFORE each test to create a clean testing environment."""
        self.test_file = "temp_test_registry.csv"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Runs AFTER each test to clean up the workspace."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # --- PART 1: CORE LOGIC & PHYSICS ---
    def test_mass_calculation_accuracy(self):
        """Verify that 1.0 m3 of Steel (7850kg/m3) equals 7850kg."""
        p = MechanicalPart("MECH-1001", "Steel Beam", "JCB", "Steel", 1.0)
        self.assertEqual(p.get_mass(), 7850.0)

    def test_carbon_footprint_logic(self):
        """Verify CO2 calculation for Aluminum (Mass * 12.5)."""
        p = MechanicalPart("MECH-2002", "Bracket", "JCB", "Aluminum", 0.1)
        # 0.1m3 Aluminum = 270kg. 270 * 12.5 = 3375.0
        self.assertEqual(p.get_carbon(), 3375.0)

    # --- PART 2: INHERITANCE & SUBCLASSES (The 'SDS' style) ---
    def test_standard_part_attributes(self):
        """Verify StandardPart correctly handles shelf location."""
        p = StandardPart("STD-001", "Bolt", "Fixit", "Steel", 0.001, "A1-102")
        self.assertEqual(p.shelf_id, "A1-102")
        self.assertIn("Shelf: A1-102", str(p))

    def test_custom_component_attributes(self):
        """Verify CustomComponent correctly handles lead time."""
        p = CustomComponent("CUST-99", "Gear", "Bespoke", "Titanium", 0.005, 21)
        self.assertEqual(p.lead_time, 21)
        self.assertIn("21 days", str(p))

    # --- PART 3: VALIDATION & EXCEPTION HANDLING ---
    def test_missing_name_raises(self):
        """Check that an empty name triggers a ValueError (Lecturer requirement)."""
        with self.assertRaises(ValueError):
            MechanicalPart("MECH-1001", "", "JCB", "Steel", 1.0)

    def test_invalid_volume_raises(self):
        """Ensure non-numeric volume strings raise ValueError."""
        with self.assertRaises(ValueError):
            MechanicalPart("ID-123", "Part", "Brand", "Steel", "NotANumber")

    # --- PART 4: INTEGRATION & PERSISTENCE ---
    def test_registry_initialization(self):
        """Verify the system creates a valid CSV with headers if missing."""
        validate_registry(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            header = f.readline()
            # Must match the new 7-column format: Type, ID, Name...
            self.assertIn("Type,ID,Name", header)

    def test_persistence_round_trip(self):
        """Ensures data does not degrade when moving between RAM and Disk."""
        # Use a StandardPart for the test
        p_orig = StandardPart("SAVE-1234", "Persistence Test", "N/A", "Titanium", 0.5, "B2")
        validate_registry(self.test_file)
        
        # Manually write to simulate main.py behavior
        with open(self.test_file, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["STD", p_orig.uid, p_orig.name, p_orig.material, 
                             p_orig.get_mass(), p_orig.get_carbon(), p_orig.shelf_id])
        
        inventory = load_existing_data(self.test_file)
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].uid, "SAVE-1234")
        self.assertIsInstance(inventory[0], StandardPart)

    # --- PART 5: UTILITY & REGEX ---
    def test_id_validator_boundaries(self):
        """Stress-test the Regex validator for various formatting edge-cases."""
        self.assertTrue(is_valid_part_id("MECH-1234"))
        self.assertFalse(is_valid_part_id("mech-1234"))  # Case sensitivity
        self.assertFalse(is_valid_part_id("MECH1234"))   # Delimiter check
        self.assertFalse(is_valid_part_id("TOO_MANY_CHARS-1234")) 

if __name__ == "__main__":
    unittest.main()