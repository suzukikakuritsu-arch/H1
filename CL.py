# ==========================================================
# ECONOMIC PHASE TRANSITION SIMULATOR
# Bridge layer for future Coq / Lean formalization
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. Parameters
# ------------------------------

a = 1.0
b = 1.0
gamma = 0.8
Hc = 1.0

dt = 0.01
T = 50
steps = int(T / dt)

# ------------------------------
# 2. Structural matrices (Core definition)
# ------------------------------

A = np.array([[1.0, -0.5, 0.0],
              [0.0, 1.0, -0.3],
              [0.2, 0.0, 1.0]])

b_vec = np.array([0.0, 0.0, 0.0])

# ------------------------------
# 3. Inconsistency Measure H(x)
# ------------------------------

def H(x):
    return np.linalg.norm(A @ x - b_vec)**2

# ------------------------------
# 4. Order parameter φ
# ------------------------------

def phi(x):
    return x[0] - x[1]  # concentration - liquidity

# ------------------------------
# 5. Civilization OS control
# ------------------------------

def control_input(x):
    h = H(x)
    if h > Hc:
        # redistribute & inject liquidity
        return np.array([-0.5, 0.5, 0.3])
    else:
        return np.array([0.1, 0.1, 0.0])

# ------------------------------
# 6. State evolution
# ------------------------------

def F(x):
    return np.array([
        0.5 * x[0] - 0.2 * x[0]**3,
        -0.3 * x[1] + 0.1 * x[2],
        -0.2 * x[2]
    ])

# ------------------------------
# 7. Simulation
# ------------------------------

x = np.array([2.0, -1.5, 1.0])  # initial unstable state

history_phi = []
history_H = []
history_time = []

for i in range(steps):
    t = i * dt
    
    u = control_input(x)
    dx = F(x) + u
    x = x + dx * dt
    
    history_phi.append(phi(x))
    history_H.append(H(x))
    history_time.append(t)

# ------------------------------
# 8. Visualization
# ------------------------------

plt.figure()
plt.plot(history_time, history_phi)
plt.title("Order Parameter φ(t)")
plt.xlabel("Time")
plt.ylabel("φ")
plt.show()

plt.figure()
plt.plot(history_time, history_H)
plt.axhline(Hc)
plt.title("Inconsistency Measure H(t)")
plt.xlabel("Time")
plt.ylabel("H")
plt.show()
