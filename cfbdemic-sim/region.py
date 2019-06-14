import SIRModel

#borders_dict = {}

class Region:
    def __init__(self, name, borders, sir_model, researchers_list):
        self.name = name
        self.borders = borders
        self.model = sir_model
        self.population = sir_model.population

    def sim_days():
