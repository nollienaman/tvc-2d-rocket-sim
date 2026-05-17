import numpy as np

class RocketDynamics:
    def __init__(self, I, T, l):
        self.I = I
        self.T = T
        self.l = l

    def step(self, state, delta, wind_torque, dt):
        tau_tvc = self.T * self.l * np.sin(delta)

        alpha = (tau_tvc + wind_torque) / self.I

        state.omega += alpha * dt
        state.theta += state.omega * dt

        return state