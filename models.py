class Component:
    
    def __init__(self, part_id, name, manufacturer):
        self.part_id = part_id
        self.name = name
        self.manufacturer = manufacturer

    def get_details(self):
        return f"[{self.part_id}] {self.name} - Mfr: {self.manufacturer}"

class MechanicalPart(Component):
    """Subclass demonstrating Inheritance"""
    def __init__(self, part_id, name, manufacturer, material, weight):
        super().__init__(part_id, name, manufacturer)
        self.material = material
        self.weight = weight

    def get_details(self):
        base = super().get_details()
        return f"{base} | Material: {self.material} | Weight: {self.weight}kg"