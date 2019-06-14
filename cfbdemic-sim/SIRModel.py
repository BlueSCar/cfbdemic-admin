from scipy.integrate import odeint
import numpy as np

class SIRModel:
    def __init__(self,N,infected,contagious,zombified,R0,beta,gamma,name,infected_to_contagious,contagious_to_zombified):
        self.population = N
        self.infected, self.initial_infected = infected + contagious + zombified
        self.latent, self.latent_initial = infected
        self.contagious, self.contagious_initial = contagious
        self.zombified, self.zombified_initial = zombified
        self.recovered, self.initial_recovered = R0
        self.susceptible, self.initial_susceptible = N - infected - contagious - zombified
        self.beta = beta
        self.gamma = gamma
        self.days_elapsed = 0
        self.infected_per_day = [self.infected]
        self.recovered_per_day = [self.recovered]
        self.susceptible_per_day = [self.susceptible]
        self.latent_per_day = [self.latent]
        self.contagious_per_day = [self.contagious]
        self.zombified_per_day = [self.zombified]
        self.days = [0]
        self.name = name
        self.infected_to_contagious = infected_to_contagious
        self.contagious_to_zombified = contagious_to_zombified

    def deriv(t):
        dSdt = -self.beta * self.susceptible * self.infected / self.population
        dIdt = self.beta * self.susceptible * self.infected / self.population - self.gamma * self.infected
        dRdt = self.gamma * self.infected
        return dSdt, dIdt, dRdt

    def iterate_once(self):
        def deriv(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt
        t = [0,1]
        y0 = self.susceptible, self.infected, self.recovered
        ret = odeint(deriv, y0, t, args=(self.population, self.beta, self.gamma))
        self.zombified = self.zombified + self.contagious
        ### NOTE: Need to implement system for tracking who is in what stage and when. Possibly iterate through dictionary which counts down timer for change?
        ### Makes these super simple summary functions easy but could be worth the revamp.
        self.susceptible = ret[1][0]
        self.infected = ret[1][1]
        self.recovered = ret[1][2]
        self.infected_per_day = self.infected_per_day + [self.infected]
        self.recovered_per_day = self.recovered_per_day + [self.recovered]
        self.susceptible_per_day = self.susceptible_per_day + [self.recovered]
        self.latent_per_day = self.latent_per_day + [self.latent]
        self.contagious_per_day = self.contagious_per_day
        self.zombified_per_day = self.zombified_per_day
        self.days_elapsed = self.days_elapsed + 1

    def iterate_multiple(self, days):
        for n in range(1,days+1):
            self.iterate_once()

    def days_list(self):
        return self.days_elapsed

    def infected_per_day(self):
        return self.infected_per_day

    def susceptible_per_day(self):
        return self.susceptible_per_day

    def recovered_per_day(self):
        return self.recovered_per_day

    def __str__(self):
        string = "SIR Model: %s\nPopulation: %i\nInfected: %f\nImmune: %f\nSusceptible: %f\nBeta: %f | Gamma: %f\nDays Elapsed: %d" % (self.name,self.population,self.infected,self.recovered,self.susceptible,
        self.beta,self.gamma,self.days_elapsed)
        return(string)

    def reset(self):
        self.infected = self.initial_infected
        self.recovered = self.initial_recovered
        self.susceptible = self.initial_susceptible
        self.days_elapsed = 0
        self.infected_per_day = [self.infected]
        self.recovered_per_day = [self.recovered]
        self.susceptible_per_day = [self.susceptible]
        self.days = [0]
