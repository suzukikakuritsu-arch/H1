# ==========================================================
# NODAL INTEGRATION LAYER
# Bridge between Coq / Lean / Python
# ==========================================================

import numpy as np
import json

# ==========================================================
# 1. Core Definition (Must match Coq/Lean definitions)
# ==========================================================

A = np.array([[1.0, -0.5, 0.0],
              [0.0, 1.0, -0.3],
              [0.2, 0.0, 1.0]])

b_vec = np.array([0.0, 0.0, 0.0])
Hc = 1.0

def H(x):
    return np.linalg.norm(A @ x - b_vec)**2

def phi(x):
    return x[0] - x[1]

# ==========================================================
# 2. Structural Integrity Check
# ==========================================================

def structural_check():
    if A.shape != (3,3):
        raise ValueError("Matrix A shape mismatch")
    if b_vec.shape != (3,):
        raise ValueError("Vector b shape mismatch")
    print("Structural check passed.")

# ==========================================================
# 3. Phase Transition Detector
# ==========================================================

def detect_phase(x):
    h = H(x)
    if abs(h - Hc) < 0.05:
        return "CRITICAL"
    elif h > Hc:
        return "UNSTABLE"
    else:
        return "STABLE"

# ==========================================================
# 4. Fixed Point Scanner
# ==========================================================

def scan_fixed_points():
    grid = np.linspace(-3, 3, 40)
    critical_points = []
    
    for x1 in grid:
        for x2 in grid:
            for x3 in grid:
                x = np.array([x1, x2, x3])
                if abs(H(x) - Hc) < 0.05:
                    critical_points.append(x.tolist())
    
    return critical_points[:20]  # limit output

# ==========================================================
# 5. Export Formal Core (for Coq / Lean alignment)
# ==========================================================

def export_core():
    core_definition = {
        "A": A.tolist(),
        "b": b_vec.tolist(),
        "H_definition": "||A x - b||^2",
        "phi_definition": "x1 - x2",
        "Hc": Hc
    }
    
    with open("formal_core.json", "w") as f:
        json.dump(core_definition, f, indent=4)
    
    print("Core exported to formal_core.json")

# ==========================================================
# 6. Test Run
# ==========================================================

if __name__ == "__main__":
    
    structural_check()
    
    x_test = np.array([2.0, -1.5, 1.0])
    
    print("H(x) =", H(x_test))
    print("phi(x) =", phi(x_test))
    print("Phase =", detect_phase(x_test))
    
    print("Scanning critical points...")
    critical = scan_fixed_points()
    print("Sample critical points:", critical)
    
    export_core()
