2D TVC Rocket Simulator

A real-time 2D rocket attitude control simulator built in Python using NumPy and Matplotlib.
The simulator models rigid-body rotational dynamics of a thrust-vector-controlled rocket and implements a PID-based feedback controller for attitude stabilization and setpoint tracking.

Features
1. 2D thrust vector control (TVC) rocket dynamics
2. PID-based attitude stabilization
3. Interactive setpoint control via keyboard inputs
4. Random wind disturbance injection for disturbance rejection testing
5. Adjustable gravity/thrust conditions
6. Real-time telemetry dashboard:
     rocket angle θ
     angular velocity ω
     gimbal angle δ
7. Modular flight-dynamics-model (FDM) architecture:
     dynamics
     controller
     actuator
     environment
     visualization
