class Body:

    def __init__(self, mass, heat_capacity, temperature):
        if mass <= 0:
            raise ValueError("mass must be greater than 0")
        if heat_capacity <= 0:
            raise ValueError("heat capacity must be greater than 0")
        if temperature < 0:
            raise ValueError("temperature must be 0 or higher")

        self.mass = mass                    
        self.heat_capacity = heat_capacity  
        self.temperature = temperature      