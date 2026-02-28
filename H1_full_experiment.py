"""
H1 FULL NUMERICAL EXPERIMENT SUITE
===================================

Golden rotation discrepancy research framework
- KS discrepancy
- Star discrepancy
- Gap distribution (Three-distance observation)
- Asymptotic scaling
- Automatic plot saving
- CSV result export

Fully executable.
No proofs included.
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from math import sqrt, log


# ============================================================
# 1. Constants
# ============================================================

def golden_ratio():
    return (1 + sqrt(5)) / 2


# ============================================================
# 2. Core Rotation Logic
# ============================================================

def rotation_sequence(alpha, N):
    n = np.arange(1, N + 1)
    return (n * alpha) % 1


# ============================================================
# 3. Discrepancy Measures
# ============================================================

def ks_discrepancy(seq):
    N = len(seq)
    x = np.sort(seq)
    empirical = np.arange(1, N + 1) / N

    d_plus = np.max(empirical - x)
    d_minus = np.max(x - (np.arange(0, N) / N))

    return max(d_plus, d_minus)


def star_discrepancy(seq):
    N = len(seq)
    x = np.sort(seq)
    empirical = np.arange(1, N + 1) / N
    return np.max(np.abs(empirical - x))


# ============================================================
# 4. Gap Analysis (Three-distance observation)
# ============================================================

def gap_distribution(seq):
    x = np.sort(seq)
    x = np.concatenate(([0], x, [1]))
    gaps = np.diff(x)
    unique_gaps = np.unique(np.round(gaps, 10))
    return gaps, unique_gaps


# ============================================================
# 5. Asymptotic Scaling Study
# ============================================================

def asymptotic_study(alpha, N_values):
    results = []

    for N in N_values:
        seq = rotation_sequence(alpha, N)
        d = ks_discrepancy(seq)
        scaled = d * N / log(N)
        results.append((N, d, scaled))

    return results


# ============================================================
# 6. Visualization Utilities
# ============================================================

def plot_cdf(alpha, N, output_dir):
    seq = rotation_sequence(alpha, N)
    x = np.sort(seq)
    empirical = np.arange(1, N + 1) / N

    plt.figure()
    plt.plot(x, empirical)
    plt.plot([0,1], [0,1])
    plt.title(f"CDF Comparison (alpha={alpha:.6f}, N={N})")
    plt.xlabel("x")
    plt.ylabel("F_N(x)")
    plt.savefig(os.path.join(output_dir, f"cdf_N{N}.png"))
    plt.close()


def plot_asymptotic(results, output_dir):
    N = [r[0] for r in results]
    scaled = [r[2] for r in results]

    plt.figure()
    plt.plot(N, scaled)
    plt.xscale("log")
    plt.title("Scaled KS Discrepancy: D_N * N / log(N)")
    plt.xlabel("N (log scale)")
    plt.ylabel("Scaled value")
    plt.savefig(os.path.join(output_dir, "asymptotic_scaling.png"))
    plt.close()


def plot_gap_histogram(gaps, output_dir):
    plt.figure()
    plt.hist(gaps, bins=50)
    plt.title("Gap Distribution")
    plt.xlabel("Gap size")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(output_dir, "gap_distribution.png"))
    plt.close()


# ============================================================
# 7. CSV Export
# ============================================================

def export_csv(results, output_dir):
    with open(os.path.join(output_dir, "asymptotic_results.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "KS_discrepancy", "Scaled_DN"])
        for row in results:
            writer.writerow(row)


# ============================================================
# 8. Full Pipeline
# ============================================================

def run_full_experiment():

    output_dir = "H1_results"
    os.makedirs(output_dir, exist_ok=True)

    phi = golden_ratio()

    print("Running H1 Full Experiment")
    print("===========================")

    # --- Basic test ---
    N_test = 5000
    seq = rotation_sequence(phi, N_test)

    ks = ks_discrepancy(seq)
    star = star_discrepancy(seq)

    print(f"KS discrepancy (N={N_test}):", ks)
    print(f"Star discrepancy (N={N_test}):", star)

    # --- Gap structure ---
    gaps, unique_gaps = gap_distribution(seq)
    print("Number of unique gap sizes:", len(unique_gaps))

    # --- Save plots ---
    plot_cdf(phi, N_test, output_dir)
    plot_gap_histogram(gaps, output_dir)

    # --- Asymptotic study ---
    N_values = [100, 300, 1000, 3000, 10000, 30000]
    results = asymptotic_study(phi, N_values)

    for r in results:
        print(f"N={r[0]}, D_N={r[1]:.6f}, scaled={r[2]:.6f}")

    plot_asymptotic(results, output_dir)
    export_csv(results, output_dir)

    print("\nAll results saved to:", output_dir)


# ============================================================
# 9. Main
# ============================================================

if __name__ == "__main__":
    run_full_experiment()
