"""
models.py — Engineering Object Models

This module defines the structural hierarchy for mechanical components.
It utilizes Object-Oriented Programming (OOP) to encapsulate physical 
properties and environmental impact calculations.
"""

class BaseComponent:
    """
    The abstract foundation for all physical engineering assets.
    Ensures every part has a unique ID, a designation, and a manufacturer.
    """
    def __init__(self, uid, name, brand):
        # --- LECTURER REQUIREMENT: Validation Guard ---
        if not name or str(name).strip() == "":
            raise ValueError("Missing name: All components must have a designation.")
        
        self.uid = uid
        self.name = name
        self.brand = brand

    def __str__(self):
        return f"Component: {self.name} (ID: {self.uid})"


class MechanicalPart(BaseComponent):
    """
    Specialized model for physical parts. Calculates mass and CO2 impact
    based on material density and manufacturing emission factors.
    """
    MAT_DATA = {
        "STEEL": {"rho": 7850, "co2": 1.9},
        "ALUMINUM": {"rho": 2700, "co2": 12.5},
        "TITANIUM": {"rho": 4430, "co2": 35.0}
    }

    def __init__(self, uid, name, brand, material, volume_m3):
        # Safety check for numeric volume to prevent system crashes
        try:
            self.volume = float(volume_m3)
        except (ValueError, TypeError):
            raise ValueError("Volume must be a numeric value (m^3).")
            
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

    def to_csv_format(self):
        """Prepares the object data for CSV serialization."""
        return [self.uid, self.name, self.material, self.get_mass(), self.get_carbon()]

    def __repr__(self):
        """Professional representation for debugging (SDS Style)."""
        return f"MechanicalPart(uid='{self.uid}', name='{self.name}', mat='{self.material}')"

    def __str__(self):
        """User-friendly summary string."""
        return f"[{self.uid}] {self.name:<20} | {self.material:<10} | {self.get_mass():>8} kg"