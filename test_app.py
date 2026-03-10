"""
test_app.py — Automated Test Suite

This suite performs 'Full-Spectrum' testing:
    - Unit Tests: Individual class methods and math logic.
    - Integration Tests: CSV Read/Write round-trips.
    - Validation Tests: Regex and Exception handling.

HOW TO RUN:
    python3 test_app.py
"""

import unittest
import os
import csv
from models import MechanicalPart
from utils import is_valid_part_id
from main import load_existing_data, validate_registry

class TestMechanicalSystem(unittest.TestCase):
    """
    Main test container for the Sustainability Tracker.
    Matches the architectural depth of the lecturer's SDS examples.
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

    # --- PART 1: CORE LOGIC TESTS ---
    def test_mass_calculation_accuracy(self):
        """Verify that 1.0 m3 of Steel (7850kg/m3) equals 7850kg."""
        p = MechanicalPart("MECH-1001", "Steel Beam", "JCB", "Steel", 1.0)
        self.assertEqual(p.get_mass(), 7850.0)

    def test_missing_name_raises(self):
        """Check that an empty name triggers a ValueError (Lecturer requirement)."""
        with self.assertRaises(ValueError):
            MechanicalPart("MECH-1001", "", "JCB", "Steel", 1.0)

    # --- PART 2: INTEGRATION & FILE I/O ---
    def test_registry_initialization(self):
        """Verify the system creates a valid CSV with headers if missing."""
        validate_registry(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            header = f.readline()
            self.assertIn("ID,Name,Material,Mass", header)

    def test_persistence_round_trip(self):
        """Ensures data does not degrade when moving between RAM and Disk."""
        p_orig = MechanicalPart("SAVE-1234", "Persistence Test", "N/A", "Titanium", 0.5)
        validate_registry(self.test_file)
        with open(self.test_file, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([p_orig.uid, p_orig.name, p_orig.material, p_orig.get_mass(), p_orig.get_carbon(), "2026-03-10"])
        
        inventory = load_existing_data(self.test_file)
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].name, "Persistence Test")

    # --- PART 3: UTILITY & REGEX ---
    def test_id_validator_boundaries(self):
        """Stress-test the Regex validator for various formatting edge-cases."""
        self.assertTrue(is_valid_part_id("MECH-1234"))
        self.assertFalse(is_valid_part_id("mech-1234"))  # Lowercase fail
        self.assertFalse(is_valid_part_id("MECH1234"))   # No hyphen fail

if __name__ == "__main__":
    unittest.main()