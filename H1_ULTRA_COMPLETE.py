"""
H1 ULTRA COMPLETE NUMERICAL RESEARCH SUITE
===========================================

Golden rotation discrepancy full analysis framework.

Features:
- Multi-alpha comparison
- KS discrepancy
- Star discrepancy
- Asymptotic scaling
- Gap distribution (Three-distance verification)
- Continued fraction expansion
- Rational approximation error
- Alpha heatmap exploration
- CSV export
- Plot auto-save
- Auto summary report

Fully executable.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from math import sqrt, log, floor


# ============================================================
# 1. Constants
# ============================================================

def golden_ratio():
    return (1 + sqrt(5)) / 2


# ============================================================
# 2. Rotation Sequence
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
# 4. Gap Structure
# ============================================================

def gap_analysis(seq):
    x = np.sort(seq)
    x = np.concatenate(([0], x, [1]))
    gaps = np.diff(x)
    unique_gaps = np.unique(np.round(gaps, 10))
    return gaps, unique_gaps


# ============================================================
# 5. Continued Fraction Expansion
# ============================================================

def continued_fraction(x, depth=20):
    cf = []
    for _ in range(depth):
        a = floor(x)
        cf.append(a)
        x = x - a
        if abs(x) < 1e-12:
            break
        x = 1 / x
    return cf


# ============================================================
# 6. Rational Approximation Error
# ============================================================

def best_rational_error(alpha, max_q=1000):
    best_error = 1
    best_pair = (0, 1)

    for q in range(1, max_q):
        p = round(alpha * q)
        error = abs(alpha - p/q)
        if error < best_error:
            best_error = error
            best_pair = (p, q)

    return best_pair, best_error


# ============================================================
# 7. Asymptotic Study
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
# 8. Heatmap Exploration
# ============================================================

def heatmap_alpha_scan(N=2000, resolution=200):
    alphas = np.linspace(0.5, 2, resolution)
    values = []

    for a in alphas:
        seq = rotation_sequence(a, N)
        d = ks_discrepancy(seq)
        values.append(d)

    return alphas, values


# ============================================================
# 9. Visualization
# ============================================================

def save_plot(x, y, title, filename, output_dir, logx=False):
    plt.figure()
    plt.plot(x, y)
    if logx:
        plt.xscale("log")
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


def save_hist(data, title, filename, output_dir):
    plt.figure()
    plt.hist(data, bins=50)
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()


# ============================================================
# 10. CSV Export
# ============================================================

def export_csv(data, headers, filename, output_dir):
    with open(os.path.join(output_dir, filename), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)


# ============================================================
# 11. Full Pipeline
# ============================================================

def run():

    output_dir = "H1_ULTRA_RESULTS"
    os.makedirs(output_dir, exist_ok=True)

    phi = golden_ratio()
    alphas = {
        "phi": phi,
        "sqrt2": sqrt(2),
        "pi": np.pi,
        "e": np.e,
        "random": np.random.rand()
    }

    summary = []

    print("=== Multi-Alpha Comparison ===")

    for name, alpha in alphas.items():
        seq = rotation_sequence(alpha, 5000)
        ks = ks_discrepancy(seq)
        star = star_discrepancy(seq)
        gaps, unique_gaps = gap_analysis(seq)

        print(f"{name}: KS={ks:.6f}, Star={star:.6f}, gap_types={len(unique_gaps)}")

        summary.append((name, ks, star, len(unique_gaps)))

        save_hist(gaps, f"{name} Gap Distribution", f"{name}_gaps.png", output_dir)

        cf = continued_fraction(alpha, 20)
        with open(os.path.join(output_dir, f"{name}_cf.txt"), "w") as f:
            f.write(str(cf))

        pair, err = best_rational_error(alpha)
        with open(os.path.join(output_dir, f"{name}_rational.txt"), "w") as f:
            f.write(f"Best approx: {pair}, error={err}")

    export_csv(summary, ["alpha", "KS", "Star", "gap_types"], "summary.csv", output_dir)

    print("\n=== Asymptotic Study (phi) ===")
    N_values = [100, 300, 1000, 3000, 10000, 30000]
    asymp = asymptotic_study(phi, N_values)

    for row in asymp:
        print(row)

    export_csv(asymp, ["N", "KS", "Scaled"], "asymptotic.csv", output_dir)

    save_plot(
        [r[0] for r in asymp],
        [r[2] for r in asymp],
        "Scaled KS (phi)",
        "asymptotic_phi.png",
        output_dir,
        logx=True
    )

    print("\n=== Alpha Heatmap Scan ===")
    alphas_scan, values_scan = heatmap_alpha_scan()
    save_plot(
        alphas_scan,
        values_scan,
        "KS vs Alpha",
        "alpha_scan.png",
        output_dir
    )

    print("\nAll results saved in:", output_dir)


# ============================================================
# 12. Main
# ============================================================

if __name__ == "__main__":
    run()
