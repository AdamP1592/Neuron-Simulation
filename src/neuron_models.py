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
    class gate():
        alpha, beta, state = 0, 0, 0

        def update(self, dt):
            alpha_state = self.alpha * (1 - self.state)
            beta_state = self.beta * self.state

            self.state += dt * (alpha_state - beta_state)
        def set_infinite_state(self):
            self.state = self.alpha / (self.alpha + self.beta)

    n_gate, m_gate, h_gate = gate(), gate(), gate()
    #implement gate class
    def __init__(self, inital_voltage = 0, dt = 0.0001):
        #used for storing past derivatives for the ion channels and overall voltages
        self.derivatives = []

        self.steady_voltage = 0
        self.resistance_L = 0.3

        self.v = inital_voltage

        self.input_current = 0
        self.membrane_cap = 1.0
        self.dt = dt

        #fixed conductances
        self.gK = 36.0
        self.gNa = 120.0
        self.gLeak = 0.3

        #membrane potentials
        self.eK = -82
        self.eNa = 45
        self.eLeak = -59.387
        
        #self.calc_resting_voltage()
        self.update_gates(self.v)
        self.gating_varibles_setup()

    def alpha_n(self, v):
        return 0.01 * ((10 - v) / (math.exp((10 - v) / 10) - 1))

    def beta_n(self, v):
        return 0.125 * (math.exp(-v / 80.0))

    def alpha_m(self, v):
        return 0.1*((25 - v) / (math.exp((25 - v) / 10.0) - 1))

    def beta_m(self, v):
        return 4.0 * (math.exp(-v/18.0))

    def alpha_h(self, v):
        return 0.07 * (math.exp(- v / 20.0))

    def beta_h(self, v):
        return 1.0/(1.0 + (math.exp((30.0 - v) / 10.0)))
    
    def gating_varibles_setup(self):
        self.n_gate.set_infinite_state()
        self.m_gate.set_infinite_state()
        self.h_gate.set_infinite_state()

    def update_gate_voltages(self, dt):
        #updates voltages
        self.n_gate.update(dt)
        self.m_gate.update(dt)
        self.h_gate.update(dt)

    def update_gates(self, v):
        #updates gate constants
        self.n_gate.alpha = self.alpha_n(v)
        self.n_gate.beta = self.beta_n(v)

        self.m_gate.alpha = self.alpha_m(v)
        self.m_gate.beta = self.beta_m(v)

        self.h_gate.alpha = self.alpha_h(v)
        self.h_gate.beta = self.beta_h(v)


    def update_v(self, input_current, dt):
        #calculates totals for each ion channel
        self.i_k = self.gK * (self.n_gate.state ** 4) * (self.v - self.eK)
        self.i_na = self.gNa * (self.m_gate.state ** 3) * self.h_gate.state * (self.v - self.eNa)
        self.i_leak = self.gLeak * (self.v - self.eLeak)
        
        #adds the sum total of all input currents to the current total voltage
        total_current = input_current - self.i_k - self.i_na - self.i_leak
        dvdt = total_current/self.membrane_cap

        self.derivatives.append(dvdt)
        self.v += dvdt * dt

    def iterate(self, input_current = False):
        #updates the current states given an input current over the duration over the current timestep 
        
        #needs to have a function for input current over time so as to get more accurate stimulation response

        #sum up all input currents from other neurons

        #updates cell voltage
        self.update_gates(self.v)
        self.update_v(input_current, self.dt) 
        self.update_gate_voltages(self.dt)

        input_current = 0

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import time
    import math

    t = 0
    t_max = 200
    dt = 0.01
    v_initial = 0
    eNa, eK, eLeak = 115, -35, 10.6
    gNa, gK, gLeak = 100, 5, 0.3

    Cm = 1

    resting_potential = -70
    
    n1 = hodgkin_huxley(v_initial, dt)
    
    n1.gK = gK
    n1.gNa = gNa
    n1.gLeak = gLeak
    n1.eK = eK
    n1.eNa = eNa
    n1.eLeak = eLeak
    n1.membrane_cap = Cm
 
    var = 1
    
    sin_current = lambda t :5 * math.sin(2 * math.pi * 0.1 * t)
    current = 20


    current_times = [70, 130]

    x, y = [], []
    y_shifted = []
    m,n,h = [], [], []

    fig, ax = plt.subplots(3, 1)

    while(t + dt <= t_max):

         
        var += 1 
        v = current  * (t > current_times [0]  and t < current_times[1])
        n1.iterate(v)
        x.append(t)
        m.append(n1.m_gate.state)
        n.append(n1.n_gate.state)
        h.append(n1.h_gate.state)
        y.append(n1.v + resting_potential)

        t += dt
    #print(voltages, "\n \n", n, "\n \n", m, "\n \n", h)
    #print(n1.eK, n1.gK, n1.eNa, n1.gNa, n1.eLeak, n1.gLeak)
    #print(voltages[-20:], n[-20:], m[-20:], h[-20])

    ax[0].set_xlabel("time")
    ax[0].set_ylabel("Membrane Potential")
    ax[0].plot(x, y)

    ax[1].plot(x, m)
    ax[1].plot(x, n)
    ax[1].plot(x, h)
    ax[2].plot(x, n1.derivatives)
    plt.show()


    
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

    