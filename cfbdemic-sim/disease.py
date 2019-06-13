class Disease:
    def __init__(self, name = "Healthy", infected_to_contagious = None, contagious_to_zombified = None, transmission_rate = None):
        self.name = name
        self.infected_to_contagious = infected_to_contagious
        self.contagious_to_zombified = contagious_to_zombified,
        self.transmission = transmission

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == self.other.name

    def __str__(self):
        return self.name
