from dataclasses import dataclass

@dataclass
class State:
    theta: float = 0.0
    omega: float = 0.0
    integral_error: float = 0.0