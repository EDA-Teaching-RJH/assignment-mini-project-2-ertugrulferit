"""
models.py — Engineering Object Models
Implements a 3-tier inheritance hierarchy: Base -> Mechanical -> Standard/Custom.
"""

class BaseComponent:
    def __init__(self, uid, name, brand):
        if not name or str(name).strip() == "":
            raise ValueError("Missing name: All components must have a designation.")
        self.uid = uid
        self.name = name
        self.brand = brand

class MechanicalPart(BaseComponent):
    """Base class for all physical parts (Similar to 'Student' class)."""
    MAT_DATA = {
        "STEEL": {"rho": 7850, "co2": 1.9},
        "ALUMINUM": {"rho": 2700, "co2": 12.5},
        "TITANIUM": {"rho": 4430, "co2": 35.0}
    }

    def __init__(self, uid, name, brand, material, volume_m3):
        try:
            self.volume = float(volume_m3)
        except (ValueError, TypeError):
            raise ValueError("Volume must be a numeric value.")
        super().__init__(uid, name, brand)
        self.material = material.upper()
        
        # Fallback to standard density if material is unknown
        self.props = self.MAT_DATA.get(self.material, {"rho": 1000, "co2": 1.0})

    def get_mass(self):
        """Calculates total mass in kilograms (Volume * Density)."""
        return round(self.volume * self.props["rho"], 2)

    def get_carbon(self):
        """Calculates CO2e impact (Mass * Emission Factor)."""
        return round(self.get_mass() * self.props["co2"], 2)

class StandardPart(MechanicalPart):
    """Off-the-shelf components (Similar to 'Undergraduate')."""
    def __init__(self, uid, name, brand, material, volume_m3, shelf_id="A1"):
        super().__init__(uid, name, brand, material, volume_m3)
        self.shelf_id = shelf_id

    def __str__(self):
        return f"[STD] {self.uid:<10} | {self.name:<15} | Shelf: {self.shelf_id}"

class CustomComponent(MechanicalPart):
    """Bespoke CNC components (Similar to 'Postgrad')."""
    def __init__(self, uid, name, brand, material, volume_m3, lead_time=14):
        super().__init__(uid, name, brand, material, volume_m3)
        self.lead_time = lead_time

    def __str__(self):
        return f"[CUSTOM] {self.uid:<10} | {self.name:<15} | Lead: {self.lead_time} days"