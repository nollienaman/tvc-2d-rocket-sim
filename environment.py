import numpy as np

class Environment:
    def __init__(self):
        self.wind = 0.0

    def gust(self):
        self.wind = np.random.uniform(-2, 2)

    def torque(self):
        return self.wind