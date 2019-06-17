from scipy.integrate import odeint
import numpy as np

"""
This class models the effects of a disease in a given population. This is
adopted from an earlier script which defined a generic SIR model, but it has
been extensively modeled so to work with the parameters of the CFBDemic disease.

An SIR model, or a Susceptible, Infected, and Recovered model, is a model of
disease spread over time. Given a fixed population N, an initial number of
nfected and immune sub-populations, a mean recovery time for a disease, and a
model of the average rate of contact for infected individuals, the progression
of a disease through a population can be modelled using differential equations.

The main constraints of an SIR model are as follows.

S = S(t) - the number of susceptible individuals
I = I(t) - the number of infected individuals
R = R(t) - the number of recovered individuals, who are assumed to be immune

N = S + I + R = S(t) + I(t) + R(t) - the population is unchanged at any time t*

* People may leave the "physical" population in this instance by dying of the
disease - however, for the purposes of modeling, they are assumed to have
"recovered" only in the sense that they are incapable of recieving the disease.
For potentially lethal diseases, a better term may be "Immune".

Based on these constraints, we can derive the following differential equations.

S'(t) = - β S(t) I(t) / N
I'(t) = β S(t) I(t) / N - γ I(t)
R'(t) = γ I(t)

... where β represents the average number of contacts that are capable of
spreading the disease, such that β S(t) represents the number of Susceptible
individuals that are generated from a single Infected individual, and γ
represents the average fraction of the Infected population that will
become Recovered as a result of the progression of the disease (for example, if
the mean recovery time of the disease is three days, then 1/3rd of the Infected
population will recover on any given day).

We can use the odeint function from the scipy.integrate package to integrate
over these differential equations and approximate the values of each
sub-population under the given assumptions.

We have to modify our assumptions and the model slightly in order to accurately
model the diseases present in CFBDemic. A CFBDemic disease differs from an ideal
SIR Model disease in the following ways:

    * An SIR Model disease has three states - Susceptible, Infected, and
      Recovered. The behaviors of each state are as listed below:

        * Susceptible - This portion of the population can obtain the disease,
          but has not done so yet.
        * Infected - This portion of the population has the disease and can
          spread it freely to the Susceptible sub-population. When the Infected
          sub-population of a population reaches zero, the disease is gone.
        * Recovered - This portion of the population can no longer be given the
          disease by a member of the Infected sub-population. Can be considered
          an absorbing state.

     While the general scheme of a CFBDemic disease falls into the above
     categories, there are a number of differences in behaviors for each stage.
     Note that the progression of states is linear and in this order, as it is
     for an SIR model.

        * Susceptible - There is no difference for this stage between the
          corresponding sup-population for an SIR model.
        * Latent - Called "Infected" by the terminology of the game, this
          sub-population has the disease, but is incapable of spreading the
          disease to the susceptible sub-population. This sub-population acts
          like the Recovered population in that they are immune to contracting
          the disease nor do they share the disease.
        * Contagious - This sub-population is capable of spreading the disease,
          and act as the "Infected" of the SIR model.
        * Zombified - This sub-population is also believed to be capable of
          spreading the disease, and can also be classified as the corresponding
          "Infected" of the SIR model - however, it is this stage that acts as
          an absorbing state - instead of "Recovering", users are themselves
          contagious until cured.

   * As a result of the above progression of stages, whereas an SIR model
     disease moves as follows:

        Susceptible -> Infected -> Recovered

     In the same terms, a CFBDemic disease moves instead as:

        Susceptible -> Recovered -> Infected

     Note that there is functionally little difference between the Contagious
     and Zombified sub-populations in the eyes of the SIR model. This
     distinction is made for a mechanic of CFBDemic where users may be treated
     to reverse the stages of the disease.

   * An SIR model usually has a non-zero value of γ, such that eventually, every
     individual in the infected population can no longer spread the disease.
     However, CFBDemic diseases have, as an absorbing state, a contagious state.
     In modeling CFBDemic diseases, γ must be 0, as the only way to return
     individuals to non-contagious states is to treat them using the
     aforementioned game mechanic.

     This is obviously not to say that there is no progression between stages.
     Rather, CFBDemic diseases instead proceed through stages at a linear rate.
     If an individual joins the Infected sub-population, they become Contagious
     a fixed number of days after the day that they joind the Infected
     sub-population, and so on.

In modeling CFBDemic diseases, our principal consideration is that the
proportions of each sub-population change according to rules that are not
incorporated in these differential equations. To attack this problem, we adopt
the following approaches:

    * We identify the "Healthy" sub-population as the Susceptible population,
      the "Contagious" and "Zombified" sub-populations as the Infected
      population for the purposes of an SIR model.
    * We use an iterative dictionary to keep track of which sub-populations are
      at each stage of the disease and how long it is until they transition to
      the subsequent stage.
    * We integrate the given differential equations of the SIR model over one
      day at a time as so to model the spread. Then, we take each sub-population
      and progress them through hte disease as neccesary. For multiple days,
      rather than integrate over a range of time, we repeat the above process.
      Note that while this is relatively unrealistic for a real-world disease,
      for CFBDemic (where the game is incremeneted in discrete units) it is
      wholly appropriate. Each change is noted in the iterative dictionary.


"""

class disease:
    def __init__(self,name,N,infected,contagious,zombified,beta,infected_to_contagious,contagious_to_zombified):
        self.initial_infected = infected
        self.initial_contagious = contagious
        self.initial_zombified = zombified
        self.population = N #Initial population
        self.beta = beta #effective contact rate
        #The tracking dictionary. Note that for conveniences' sake, this script
        #is hardcoded such that the healthy population is always at index 0 in
        #this list, and the zombified population is always at index 1. All other
        #sub-populations are added and removed as they progress.
        self.tracking_dict = [{'id':'healthy_pop','pop':N - infected - contagious - zombified,'status':'Healthy','day':0},
                              {'id':'zombified_pop','pop':zombified,'status':'Zombified','day':0},
                              {'id':'sub_pop_1','pop':infected,'status':'Infected','day':0},
                              {'id':'sub_pop_2','pop':contagious,'status':'Contagious','day':0}]
        self.name = name
        self.infected_to_contagious = infected_to_contagious #How long it takes for an infected individual to become contagious
        self.contagious_to_zombified = contagious_to_zombified #How long it takes a contagious individual to become a zombie
        self.days = 0
        self.healthy = self.population - self.initial_infected - self.initial_contagious - self.initial_zombified
        self.infected = self.initial_infected
        self.contagious = self.initial_contagious
        self.zombified = self.initial_zombified

    def __str__(self):
        string = """SIR Model: %s
                    Population: %f
                    Healthy: %f
                    Infected: %f
                    Contagious: %f
                    Zombified: %f
                    Beta: %f | Gamma: %f
                    Days Elapsed: %d""" % (self.name,
                    self.population,
                    sum([item['pop'] for item in self.tracking_dict if item['status'] == 'Healthy']),
                    sum([item['pop'] for item in self.tracking_dict if item['status'] == 'Infected']),
                    sum([item['pop'] for item in self.tracking_dict if item['status'] == 'Contagious']),
                    sum([item['pop'] for item in self.tracking_dict if item['status'] == 'Zombified']),
                    self.beta, 0.0,
                    self.tracking_dict[0]['day'])
        return(string)

    #This is the main function for simulating the change in the population
    def iterate_once(self):
        #This subfunction calculates the instantaneous rates of change for the
        #variables of a generic SIR model.
        def deriv(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt
        t = [0,1] #This asks the function to iterate from the initial condition one day.
        contagious_temp = sum([val['pop'] for val in self.tracking_dict if val['status'] in ['Contagious','Zombified']]) #This grabs the entire contagious sub-population from the tracking dictionary
        infected_temp = sum([val['pop'] for val in self.tracking_dict if val['status'] == 'Infected']) #This grabs the infected, or "Immune" sub-population from the tracking dictionary.
        susceptible = self.population - contagious_temp - infected_temp
        y0 = susceptible, contagious_temp, infected_temp
        ret = odeint(deriv, y0, t, args=(self.population, self.beta, 0)) #This iterates once over the given time interval. Note that γ = 0 here as the recovery time of a CFBDemic disease is zero.
        self.days = self.days + 1
        self.tracking_dict[0]['pop'] = ret[1][0] #This updates the uninfected population, which shrinks as a result of these efforts
        self.tracking_dict = self.tracking_dict + [{'id':'sup_pop_'+str(self.days + 2),'pop':ret[1][1] - contagious_temp,'status':'Infected','day':0}] #There are a new group of infected indiviudals as a result of the spread of disease after the iteration.
        #This takes each sub-population and checks to see if it needs to be added to the absorbing state or incremeneted to a new state.
        for item in self.tracking_dict:
            #checks if an infected sub-population should be changed to a contagious one
            if item['status'] == 'Infected' and item['day'] == self.infected_to_contagious:
                item['status'] = 'Contagious'
                item['day'] = 0
            #checks if a contagious sub-population should be changed to a zombified one
            elif item['status'] == 'Contagious' and item['day'] == self.contagious_to_zombified:
                self.tracking_dict[1]['pop'] = self.tracking_dict[1]['pop'] + item['pop']
                self.tracking_dict.remove(item) #removes that dictionary from the list because it's merged with the zombified population
            item['day'] = item['day'] + 1 #increments the days for all items
        self.infected = sum([val['pop'] for val in self.tracking_dict if val['status'] == 'Infected'])
        self.contagious = sum([val['pop'] for val in self.tracking_dict if val['status'] == 'Contagious'])
        self.zombified = sum([val['pop'] for val in self.tracking_dict if val['status'] == 'Zombified'])
        self.healthy = self.population - self.infected - self.contagious - self.zombified

    #use this function to iterate over multiple days.
    #N.B. do not modify the iterate_once function to change the interval of the integration! just use this, please
    def iterate_multiple(self, days):
        for n in range(1,days+1):
            self.iterate_once()

    def reset(self):
                self.tracking_dict = [{'id':'healthy_pop','pop':self.population - self.initial_infected - self.initial_contagious - self.initial_zombified,'status':'Healthy','day':0},
                                      {'id':'zombified_pop','pop':self.initial_zombified,'status':'Zombified','day':0},
                                      {'id':'sub_pop_1','pop':self.initial_infected,'status':'Infected','day':0},
                                      {'id':'sub_pop_2','pop':self.initial_contagious,'status':'Contagious','day':0}]
                self.days = 0
