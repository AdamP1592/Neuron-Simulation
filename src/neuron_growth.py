class branch():
    def __init__(self, growth_params = {}, dt = 0.001):
        self.growth_params = growth_params
        self.dt = dt
        self.sub_branches = 

        if not growth_params:
            growth_params = {
                "length": 2,
                "growth_rate": 0.0003,
                "branching_probability": 0.05,
                "branching_angle_xy" : 0,
                "branching_angle_xz":0,
                "noise_const":0.05
            }
    def add_noise(self, value):
        import random
        noise = self.growth_params["noise_const"]
        
        lower_bound = value * (1 - noise)
        upper_bound = value * (1 + noise)

        random_value = random.randint(0, 100)

        step = (upper_bound-lower_bound)/random_value
        noise_range = range(upper_bound, lower_bound, step)
        
        #new value = ((value range/random_divisor) * random_value) + upper_bound
        new_value = upper_bound - lower_bound
        return 
        
        
    def grow(self, time):
        pass

class growth_tree():
    def __init__(self):
