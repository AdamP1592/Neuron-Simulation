import math
class neuron():
    def __init__(self):
        pass
    def set_vars(self, vars = []): 
        pass
    #returns the mebrane potential after a given amount of time
    def calculate(self, voltage_in=0, time=0):
        pass
class charlie_neuron():
    def __init__(self, intrins_firing_rate, synaptic_conductance_fn, reversal_potential, membrane_potential_in_phase, gaussian_noise, phase_resetting_curve):
        self.omega = intrins_firing_rate
        self.gt = synaptic_conductance_fn
        self.e_rev = reversal_potential
        self.v_phi = membrane_potential_in_phase
        self.i_n = gaussian_noise
        self.prc = phase_resetting_curve

    def calculate(self, time, dt):
        inner = (self.gt(time)* (self.e_rev- self.v_phi)) + self.i_n
        phase_change_dt = (self.omega  + (inner * self.prc))
        return phase_change_dt

    def set_prc(self, components, scalar):
        sum_total = 0
    
        for comp_values in components:
            skew = 0
            
class hodgkin_huxley(neuron):

    #implement gate class
    def __init__(self, inital_voltage = 0, dt = 0.0001):

        self.v = inital_voltage

        self.input_current = 0
        self.membrane_cap = 1.0
        self.dt = dt

        #conductances
        self.gK = 36.0
        self.gNa = 120.0
        self.gLeak = 0.3

        #membrane potentials
        self.Vk = -82
        self.Vna = 45
        self.Vleak = -59.387

        tau_n = 1/(self.alpha_n() + self.beta_n())
        tau_m = 1/(self.alpha_m() + self.beta_m())
        tau_h = 1/(self.alpha_h() + self.beta_h())
        
        self.n = self.alpha_n() * tau_n
        self.m = self.alpha_m() * tau_m
        self.h = self.alpha_h() * tau_h
    def __str__(self):
        return str(self.v)
        
    def add_synaptic_input(self, input_current):
        self.input_current += input_current
        
    def calculate_derivatives(self):
        #calculates each channel current
        self.i_k = self.gK * (self.n**4) * (self.Vk - self.v)
        self.i_na = self.gNa * (self.m**3) * self.h *(self.Vna - v)
        self.i_leak = self.gLeak * (self.Vleak - self.v)
        
        #adds the sum total of all input currents to the current total voltage
        total_current = self.input_current + self.i_k + self.i_na + self.i_leak
        
        #calcs derivatives for all channels as well as the derivative of the voltage
        dvdt = (total_current)/self.membrane_cap
        dndt = self.alpha_n() * (1.0 - self.n) - self.beta_n() * self.n
        dmdt = self.alpha_m() * (1.0 - self.m) - self.beta_m() * self.m
        dhdt = self.alpha_h() * (1.0 - self.h) - self.beta_h() * self.h
        
        #returns each derivative
        return dvdt, dndt, dmdt, dhdt
    def update(self, input_current = 0):
        #updates the current states given an input current over the duration over the current timestep 
        
        #needs to have a function for input current over time so as to get more accurate stimulation response

        self.input_current += input_current
        dvdt, dndt, dmdt, dhdt = self.calculate_derivatives() 

        self.v += dvdt * self.dt
        self.n += dndt * self.dt
        self.m += dmdt * self.dt
        self.h += dhdt * self.dt

        self.input_current = 0
    def alpha_m(self):
        v = self.v
        return 0.1*(v + 40.0) / (1.0 - (math.exp(-(v + 45.0) / 10.0)))

    def beta_m(self):
        v = self.v
        return 4.0 * (math.exp (-(v + 75.0)/18.0))

    def alpha_h(self):
        v = self.v
        return 0.07 * (math.exp(-(v + 70.0) / 20.0))

    def beta_h(self):
        v = self.v
        return 1.0/(1.0 + (math.exp(-(v + 35.0) / 10.0)))

    def alpha_n(self):
        v = self.v
        return (0.01 * (v + 60.0)) / (1.0 - (math.exp(-(v + 60.0) / 10.0)))

    def beta_n(self):
        v = self.v
        return 0.125 * (math.exp(-(v + 70.0) / 80.0))

class network_node():
    def __init__(self, neuron):
        self.neuron = neuron
        
if __name__ == '__main__':
    dt = 0.0001
    n1 = hodgkin_huxley()
    var = 1
    for i in range(20000):
        v = 20
        var += 1 
        print("In volt:{}, Soma volt:{}".format(v, n1))
        n1.update(v)


    
    
#each neuron will be 3 vectors, 1 point, and internal dynamics
#the point is the cell  body, the vectors are
#synaptic vector, axonal vector, and dendritic vector
#synaptic vector overlap will act as a modifier on the stdp rule
#axonal vector will either be mono or bidirectional, and will solely act 
#by branching out until connection is formed with a dendritic tree or
#the neuron can't grow anymore(cornered/reaches max length)
#The overlap between a dendritic vector and a axonal vector is
#where I will be determining connectivity, however it is important to note
#this is only 1 of 3 kinds of axonal connection. 


#axon max length is defined by a combination of enviornmental constraints and 
#natural growth constraints of neuron. 
#connections will be determined by checking each dendrite and axon vectors for overlap.
#axons vectors will naturally "repel" eachother by increasing

    