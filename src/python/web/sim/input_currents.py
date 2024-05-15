class input_current():
    def __init__(self, params = []):
        self.needed_params = []
        self.set_params(params)
        pass
    def get_current(self, t):
        return 0
    def set_params(self, params = []):
        self.params = params

class square_current():
    #input params = [voltage]
    def __init__(self, params = [0]):
        self.needed_params = ["voltage"]
        self.set_params(params)
    #returns the square pulse at v
    def get_current(self, t):
        return self.v
    def set_params(self, params = []):
        self.v = params[0]

class sin_current():
    #params = [max voltage, frequency]
    def __init__(self, params = [0,0]):
        self.needed_params = ["Max Voltage, Frequency(mHz)"]
        self.set_params(params)
    def get_current(self, t):
        import math
        return (self.amplitude * math.sin(math.pi * t * self.frequency) + self.amplitude)
    def set_params(self, params = []):
        
        self.amplitude = params[0]/2
        self.frequency = params[1]
        