class Body:

    def __init__(self, mass, heat_capacity, temperature):
        self.mass = mass                    # kg
        self.heat_capacity = heat_capacity  # J/kg°C
        self.temperature = temperature      # °C

        if self.mass <= 0:
            print("mass must be greater than 0, using 1 kg")
            self.mass = 1
        if self.heat_capacity <= 0:
            print("heat capacity must be greater than 0, using 1 J/kg°C")
            self.heat_capacity = 1
        if self.temperature < 0:
            print("temperature must be 0 or higher, using 0 °C")
            self.temperature = 0

    def add_heat(self, heat):
        # heat is in Joules, can be negative
        delta_temperature = heat / (self.mass * self.heat_capacity)     # ΔT = Q / (m * c)
        self.temperature = self.temperature + delta_temperature         # new T = T + ΔT
        return self.temperature


if __name__ == "__main__":
    body = Body(100, 0.15, 200)

    result = body.add_heat(20)
    print("after adding 20 J:", result)
    print("expected:", 200 + 20 / (100 * 0.15))

    result = body.add_heat(-40)
    print("after adding -40 J:", result)
    print("expected:", 200 + 20 / (100 * 0.15) - 40 / (100 * 0.15))