
#population_dict structure
#population_dict = [{"status":disease_obj,"affected_pop":100000},...]

class Region:
    def __init__(self, name, bordering_names, population_dict, researchers_list):
        self.name = name
        self.bordering_names = bordering_names
        self.population = population_dict
        self.total_population = sum([population["affected_pop"] for population in population_dict])
        #self.healthy_population =
