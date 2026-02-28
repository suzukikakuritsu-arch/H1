# ==========================================================
# TRIPLE-LAYER NODAL BRIDGE
# Coq / Lean / Python Unified Core
# ==========================================================

import numpy as np
import json

# ----------------------------------------------------------
# 1. Load Single Source of Truth
# ----------------------------------------------------------

with open("core_spec.json") as f:
    core = json.load(f)

A = np.array(core["A"])
b_vec = np.array(core["b"])
Hc = core["Hc"]

# ----------------------------------------------------------
# 2. Core Definitions (Must match Coq/Lean)
# ----------------------------------------------------------

def H(x):
    return np.linalg.norm(A @ x - b_vec)**2

def phi(x):
    return x[0] - x[1]

# ----------------------------------------------------------
# 3. Structural Consistency Check
# ----------------------------------------------------------

def verify_structure():
    assert A.shape[0] == A.shape[1], "A must be square"
    assert len(b_vec) == A.shape[0], "b dimension mismatch"
    print("Structure verified.")

# ----------------------------------------------------------
# 4. Stability via Jacobian Eigenvalues
# ----------------------------------------------------------

def jacobian_numeric(x, eps=1e-5):
    n = len(x)
    J = np.zeros((n,n))
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = eps
        J[:,i] = (F(x + dx) - F(x - dx)) / (2*eps)
    return J

# Example dynamic (minimal placeholder)
def F(x):
    return np.array([
        0.5*x[0] - 0.2*x[0]**3,
        -0.3*x[1] + 0.1*x[2],
        -0.2*x[2]
    ])

def stability_check(x):
    J = jacobian_numeric(x)
    eigvals = np.linalg.eigvals(J)
    return eigvals

# ----------------------------------------------------------
# 5. Phase Classification
# ----------------------------------------------------------

def classify(x):
    h = H(x)
    if abs(h - Hc) < 0.01:
        return "CRITICAL"
    elif h > Hc:
        return "UNSTABLE"
    else:
        return "STABLE"

# ----------------------------------------------------------
# 6. Main
# ----------------------------------------------------------

if __name__ == "__main__":
    
    verify_structure()
    
    x_test = np.array([2.0, -1.5, 1.0])
    
    print("H(x):", H(x_test))
    print("phi(x):", phi(x_test))
    print("Phase:", classify(x_test))
    
    eigvals = stability_check(x_test)
    print("Eigenvalues:", eigvals)
