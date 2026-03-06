import unittest
from utils import is_valid_part_id
from models import MechanicalPart

class TestEngineeringSystem(unittest.TestCase):
    def test_logic(self):
        # 1m3 Steel should be 7850kg mass and 14915.0kg CO2
        part = MechanicalPart("TEST-1234", "Beam", "JCB", "Steel", 1.0)
        self.assertEqual(part.get_mass(), 7850.0)
        self.assertEqual(part.get_carbon(), 14915.0)

    def test_validation(self):
        self.assertTrue(is_valid_part_id("MECH-9999"))
        self.assertFalse(is_valid_part_id("mech-9999"))

if __name__ == "__main__":
    unittest.main()