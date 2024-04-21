class synaptic_model():
    def __init__(self):
        #model is some function that takes in an input voltage from the cells and returns the post synaptic voltage
        self.previous

class stdp_model(synaptic_model):

    #decay rate should be a function relative to a neuron lifespan
    
    
    def __init__(self, pre_neurons, post_neurons):
        #params and initial default values, needs implementation
        params = {"tau_plus": 20, "tau_minus": 20, "W_max": 1.0, "W_min":0, "delta_t": 1, "decay_rate":0.95, "alpha_plus":0.01, "alpha_minus":0.01}
        initial_values = {"W_init" : 0.5, "delta_t": 0.1}
        #network initialization values
        self.pre_neurons = pre_neurons
        self.post_neurons = post_neurons
        
        self.neurotransmitter_modifier

        #stdp initialization params
        self.tau_plus = 20  # Time constant for potentiation
        self.tau_minus = 20  # Time constant for depression

        self.W_max = 1.0  # Maximum synaptic strength
        self.W_min = 0.0  # Minimum synaptic strength
        self.W_init = 0.5  # Initial synaptic weight

        self.delta_t = 1   # Time window for STDP

        self.decay_rate = 0.95  # Memory decay rate
        self.alpha_plus = 0.01  # Potentiation rate
        self.alpha_minus = 0.01  # Depression rate
        
    def propogate_spike(self):
        #synaps
        pass
