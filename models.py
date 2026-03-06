class BaseComponent:
    #Parent class for all inventory items.
    def __init__(self, uid, name, brand):
        self.uid = uid
        self.name = name
        self.brand = brand

class MechanicalPart(BaseComponent):
    #Subclass for physical parts requiring mass and impact calculations.
    
    #Material properties: Density (kg/m^3) | Carbon Intensity (kgCO2/kg)
    MAT_DB = {
        "STEEL": {"rho": 7850, "co2_factor": 1.9},
        "ALUMINUM": {"rho": 2700, "co2_factor": 12.5},
        "TITANIUM": {"rho": 4430, "co2_factor": 35.0}
    }

    def __init__(self, uid, name, brand, material, volume_m3):
        super().__init__(uid, name, brand)
        self.material = material.upper()
        self.volume = volume_m3
        # Fetch properties or use defaults for unknown materials
        self.stats = self.MAT_DB.get(self.material, {"rho": 1000, "co2_factor": 1.0})

    def calculate_mass(self):
        return round(self.volume * self.stats["rho"], 3)

    def calculate_co2(self):
        return round(self.calculate_mass() * self.stats["co2_factor"], 2)

    def to_csv_format(self):
        """Returns a comma-separated string for file storage."""
        return f"{self.uid},{self.name},{self.material},{self.calculate_mass()},{self.calculate_co2()}"