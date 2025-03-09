class synapse():
    #primary setup of values
    pre_synaptic_neurons = []
    pre_connectivity_weights = [] #modifiers on the sending of communication

    post_synaptic_neurons = []
    post_connectivity_weights = []
    
    max_conductance, min_conductance = 0, 0
    s = 0
    input_sensitivity = 0.1

    from gate import hhgate as gate
    syn_gate = gate()

    def __init__(self, dt, params= {"g": 0.1, "e":0, "g_max": 1.0}):
        g_max = 0.1
    def update(self):
        
    
        
        for i in range(len(self.pre_synaptic_neurons)):
            input_neuron = self.pre_synaptic_neurons[i]
            #modifier for resistivity
            weight = self.pre_connectivity_weights[i]

            input_total += input_neuron.v * weight
        #
            
        

    def update(self):
        ds = self.alpha * self.tau() * (1 - self.s) - (self.beta * s)