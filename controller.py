class PIDController:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt

    def compute(self, state, theta_sp):
        error = theta_sp - state.theta

        state.integral_error += error * self.dt

        derivative = -state.omega  # because de/dt = -omega

        delta = (
            self.kp * error +
            self.ki * state.integral_error +
            self.kd * derivative
        )

        return delta