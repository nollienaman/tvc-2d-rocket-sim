import numpy as np

class GimbalActuator:
    def __init__(self, limit_deg=15):
        self.limit = np.radians(limit_deg)

    def apply(self, delta_cmd):
        return np.clip(delta_cmd, -self.limit, self.limit)