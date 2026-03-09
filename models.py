class MechanicalPart:
    """
    Represents a physical mechanical component with sustainability tracking.
    
    Attributes:
        uid (str): Unique ISO-standard identifier.
        name (str): The common name of the part.
        material (str): Used to look up density and CO2 factors.
        volume (float): Measured in cubic meters.
    """
class BaseComponent:
    def __init__(self, uid, name, brand):
        self.uid = uid
        self.name = name
        self.brand = brand

class BaseComponent:
    def __init__(self, uid, name, brand):
        # Guard 1: Base level
        if not name or str(name).strip() == "":
            raise ValueError("Missing name")
        self.uid = uid
        self.name = name
        self.brand = brand

class MechanicalPart(BaseComponent):
    MAT_DATA = {
        "STEEL": {"rho": 7850, "co2": 1.9},
        "ALUMINUM": {"rho": 2700, "co2": 12.5},
        "TITANIUM": {"rho": 4430, "co2": 35.0}
    }

    def __init__(self, uid, name, brand, material, volume_m3):
        # Guard 2: Direct level (This is what the test hits first)
        if not name or str(name).strip() == "":
            raise ValueError("Missing name")
            
        super().__init__(uid, name, brand)
        self.material = material.upper()
        self.volume = float(volume_m3)
        self.props = self.MAT_DATA.get(self.material, {"rho": 1000, "co2": 1.0})

    def get_mass(self):
        return round(self.volume * self.props["rho"], 2)

    def get_carbon(self):
        return round(self.get_mass() * self.props["co2"], 2)

    def to_csv_format(self):
        """Prepare the part's data in a CSV-friendly string format."""
        return f"{self.uid},{self.name},{self.material},{self.get_mass()},{self.get_carbon()}"