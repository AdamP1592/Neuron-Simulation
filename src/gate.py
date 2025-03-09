class hhgate():
    alpha, beta, state = 0, 0, 0

    def update(self, dt):
        numerator = self.__get_infinite_state() - self.state
        tau = self.__get_tau()
        self.state += dt * numerator / tau

        """
        historical implementation
        alpha_state = self.alpha * (1 - self.state)
        beta_state = self.beta * self.state

        self.state += dt * (alpha_state - beta_state)"""
    def set_infinite_state(self):
        self.state = self.__get_infinite_state()
    def __get_infinite_state(self):
        return self.alpha * self.__get_tau()
    def __get_tau(self):
        return 1 / (self.alpha + self.beta)