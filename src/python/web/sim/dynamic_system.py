class dynamic_system():
    def __init__(self, variables:list, law:function):
        self.variables = variables
        self.law = law

    def get_derivatives(self, input_matrix:list):
        calculated_vars = []
        for i in self.variables: 
            calculated_vars.append(i[1](i[0]))
        self.law(calculated_vars)            

"""

state variables: 

membrane potential = V
activation variable of persistent potasiium current n
which creates a vect (V, n) on the plane [v, n]

instantaneous activation of sodium current is a function of membrane potential

vect is then modeled through time

attractor model with phase portrates

to encapsulate all this I store variables as (variable, function)
to allow all variables to include necessary calculations, 
if none is provided function will be lambda i: i
then you need a unifying law that combines each variable

"""
neuron_dynamics = dynamic_system()