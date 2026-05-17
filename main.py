import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

from state import State
from dynamics import RocketDynamics
from controller import PIDController
from actuator import GimbalActuator
from environment import Environment


# =========================
# Simulation setup
# =========================
dt = 0.01

state = State()

dynamics = RocketDynamics(I=1.0, T=10.0, l=1.0)
controller = PIDController(kp=3.0, ki=10.0, kd=2.0, dt=dt)
actuator = GimbalActuator(limit_deg=15)
env = Environment()

state.setpoint = 0.0  # initial target angle


# =========================
# Figure + GridSpec layout
# =========================
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)

ax_rocket = fig.add_subplot(gs[0, :])
ax_theta  = fig.add_subplot(gs[1, 0])
ax_omega  = fig.add_subplot(gs[1, 1])
ax_delta  = fig.add_subplot(gs[1, 2])
ax_info   = fig.add_subplot(gs[2, :])

ax_info.axis("off")


# =========================
# History buffers
# =========================
history_size = 400

time = []
theta_hist = []
omega_hist = []
delta_hist = []


# =========================
# Rocket drawing
# =========================
def draw_rocket(ax, theta):
    ax.clear()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 3)
    ax.set_aspect('equal')
    ax.set_title("2D TVC Rocket Simulation")

    # rocket body line
    body = np.array([[0, 0], [0, 2]])

    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    rotated = rot @ body

    ax.plot(rotated[0], rotated[1], linewidth=4)

    # nozzle direction indicator
    nozzle = np.array([[0, 0], [0.5*np.sin(state.delta), -0.5]])
    ax.plot(nozzle[0], nozzle[1], linewidth=2)


# =========================
# Keyboard controls
# =========================
def on_key(event):
    if event.key == 'left':
        state.setpoint -= np.radians(5)

    elif event.key == 'right':
        state.setpoint += np.radians(5)

    elif event.key == 'w':
        env.wind = np.random.uniform(-3, 3)

    elif event.key == 'g':
        dynamics.T = 10.0 if dynamics.T == 8.0 else 8.0

    elif event.key == 'r':
        state.theta = 0
        state.omega = 0
        state.integral_error = 0


fig.canvas.mpl_connect('key_press_event', on_key)


# =========================
# Main update loop
# =========================
def update(frame):
    global state

    # ---- environment ----
    wind_torque = env.torque()

    # ---- control ----
    delta_cmd = controller.compute(state, state.setpoint)
    state.delta = actuator.apply(delta_cmd)

    # ---- physics ----
    state = dynamics.step(state, state.delta, wind_torque, dt)

    # ---- time ----
    t = frame * dt

    time.append(t)
    theta_hist.append(np.degrees(state.theta))
    omega_hist.append(np.degrees(state.omega))
    delta_hist.append(np.degrees(state.delta))

    # trim history
    if len(time) > history_size:
        time.pop(0)
        theta_hist.pop(0)
        omega_hist.pop(0)
        delta_hist.pop(0)

    # =========================
    # Rocket view
    # =========================
    draw_rocket(ax_rocket, state.theta)

    # =========================
    # Telemetry plots
    # =========================
    ax_theta.clear()
    ax_omega.clear()
    ax_delta.clear()

    ax_theta.plot(time, theta_hist)
    ax_omega.plot(time, omega_hist)
    ax_delta.plot(time, delta_hist)

    ax_theta.set_title("Angle θ (deg)")
    ax_omega.set_title("Angular Velocity ω (deg/s)")
    ax_delta.set_title("Gimbal δ (deg)")

    ax_theta.grid()
    ax_omega.grid()
    ax_delta.grid()

    # =========================
    # System dashboard (HUD)
    # =========================
    ax_info.clear()
    ax_info.axis("off")

    error = np.degrees(state.setpoint - state.theta)

    ax_info.text(0.05, 0.6, f"Setpoint: {np.degrees(state.setpoint):.2f} deg")
    ax_info.text(0.05, 0.3, f"Error: {error:.2f} deg")

    ax_info.text(0.35, 0.6, f"Wind torque: {env.wind:.2f}")
    ax_info.text(0.35, 0.3, f"Thrust: {dynamics.T:.1f}")

    ax_info.text(0.65, 0.6, f"θ: {np.degrees(state.theta):.2f}")
    ax_info.text(0.65, 0.3, f"ω: {np.degrees(state.omega):.2f}")

    return []


# =========================
# Run animation
# =========================
ani = FuncAnimation(
    fig,
    update,
    interval=20
)

plt.tight_layout()
plt.show()