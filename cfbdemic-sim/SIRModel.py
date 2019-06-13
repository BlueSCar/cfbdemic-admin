from scipy.integrate import odeint
import numpy as np

class SIRModel:
    def __init__(self,N,I0,R0,beta,gamma):
        self.population = N
        self.infected = I0
        self.recovered = R0
        self.susceptible = N - I0 - R0
        self.beta = beta
        self.gamma = gamma
        self.initial_infected = I0
        self.initial_recovered = R0
        self.initial_susceptible = N - I0 - R0
        self.days_elapsed = 0
        self.infected_per_day = [self.infected]
        self.recovered_per_day = [self.recovered]
        self.susceptible_per_day = [self.susceptible]
        self.days = [0]

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
        self.susceptible = ret[1][0]
        self.infected = ret[1][1]
        self.recovered = ret[1][2]
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
        string = "SIR Model\nPopulation: %i\nInfected: %f\nImmune: %f\nSusceptible: %f\nBeta: %f | Gamma: %f\nDays Elapsed: %d" % (self.population,self.infected,self.recovered,self.susceptible,
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
