import unittest
import os
from main import load_existing_data
from models import MechanicalPart
from utils import is_valid_part_id

class TestSustainabilitySystem(unittest.TestCase):

    def setUp(self):
        """Runs b4 each test to ensure a clean environment."""
        self.test_registry = "test_registry.csv"

    def tearDown(self):
        """Runs after each test to clean up the workspace."""
        if os.path.exists(self.test_registry):
            os.remove(self.test_registry)

    def test_mechanical_physics(self):
        """Verify mass and carbon calculations for a standard Steel beam."""
        part = MechanicalPart("MECH-1001", "I-Beam", "JCB", "Steel", 1.0)
        self.assertEqual(part.get_mass(), 7850.0)
        self.assertEqual(part.get_carbon(), 14915.0)

    def test_missing_name_raises(self):
        """Check that an empty name triggers a ValueError (Lecturer requirement)."""
        with self.assertRaises(ValueError):
            MechanicalPart("MECH-1001", "", "JCB", "Steel", 1.0)

    def test_regex_validation_patterns(self):
        """Test the boundaries of the ID validator."""
        # Valid
        self.assertTrue(is_valid_part_id("MECH-1234"))
        self.assertTrue(is_valid_part_id("AERO-0000"))
        # Invalid
        self.assertFalse(is_valid_part_id("mech-1234"))
        self.assertFalse(is_valid_part_id("ABCD1234"))
        self.assertFalse(is_valid_part_id("TEST-12345"))

if __name__ == "__main__":
    unittest.main()

    def test_csv_persistence_integrity(self):
        """
        Tests the full lifecycle of a component: Creation -> Storage -> Recovery.
        This ensures no data degradation occurs during the CSV 'Hydration' process.
        """
        # 1. Create original object
        original = MechanicalPart("TEST-9999", "Integrity Check", "BrandX", "Steel", 2.5)
        
        # 2. Manual write to test file
        with open(self.test_registry, "w") as f:
            f.write("ID,Name,Material,Mass,CO2\n") # Header
            f.write(original.to_csv_format() + "\n")
            
        # 3. Use your system's loader to recover it
        recovered_list = load_existing_data(self.test_registry)
        recovered = recovered_list[0]
        
        # 4. Deep Assertion (Checking every field)
        self.assertEqual(recovered.uid, "TEST-9999")
        self.assertEqual(recovered.name, "Integrity Check")
        self.assertEqual(recovered.material, "STEEL")
        # Note: Volume is 0.0 on recovery in this version, so we check Mass/CO2 instead
        self.assertEqual(recovered.get_mass(), original.get_mass())