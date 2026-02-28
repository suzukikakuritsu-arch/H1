/-
H1 Economic Phase Transition Core
Lean 4 + mathlib
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.NormedSpace.Basic

open Matrix
open BigOperators

noncomputable section

-- Dimension
def n : ℕ := 3

-- State space R^3
abbrev X := Fin n → ℝ

-- Define matrix A
def A : Matrix (Fin n) (Fin n) ℝ :=
!![ 1.0, -0.5, 0.0;
    0.0,  1.0, -0.3;
    0.2,  0.0,  1.0 ]

-- Define vector b
def b : X := fun _ => 0.0

-- Matrix-vector multiplication
def Ax (x : X) : X :=
fun i => ∑ j, A i j * x j

-- Inconsistency measure
def H (x : X) : ℝ :=
‖(fun i => Ax x i - b i)‖^2

-- Order parameter φ
def phi (x : X) : ℝ :=
x 0 - x 1

-- Critical threshold
def Hc : ℝ := 1.0

------------------------------------------------------------
-- Theorem 1: H(x) ≥ 0
------------------------------------------------------------

theorem H_nonneg (x : X) : 0 ≤ H x := by
  unfold H
  exact sq_nonneg _

------------------------------------------------------------
-- Theorem 2: H(x) = 0 ↔ Ax = b
------------------------------------------------------------

theorem H_zero_iff (x : X) :
  H x = 0 ↔ (fun i => Ax x i - b i) = 0 := by
  unfold H
  constructor
  · intro h
    have h' : ‖(fun i => Ax x i - b i)‖ = 0 := by
      apply norm_eq_zero.mp
      simpa using h
    exact funext (fun i => by
      have := norm_eq_zero.mp h'
      simpa using this)
  · intro h
    simp [H, h]

------------------------------------------------------------
-- Definition: Critical state
------------------------------------------------------------

def Critical (x : X) : Prop :=
H x = Hc

------------------------------------------------------------
-- Structural statement of phase transition
------------------------------------------------------------

def PhaseTransition : Prop :=
∃ x : X, H x = Hc
