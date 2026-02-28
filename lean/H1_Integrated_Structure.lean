/-
H1 Integrated Economic Phase Structure
Continuity / Existence / Criticality / Stability
Lean 4 + mathlib
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix
import Mathlib.Analysis.NormedSpace.Basic
import Mathlib.Analysis.Calculus.ContDiff
import Mathlib.Analysis.SpecialFunctions.Pow
import Mathlib.Topology.Algebra.Polynomial

open Matrix
open BigOperators
open Topology

noncomputable section

------------------------------------------------------------
-- 1. Basic Structure
------------------------------------------------------------

def n : ℕ := 3
abbrev X := Fin n → ℝ

def A : Matrix (Fin n) (Fin n) ℝ :=
!![ 1.0, -0.5, 0.0;
    0.0,  1.0, -0.3;
    0.2,  0.0,  1.0 ]

def b : X := fun _ => 0.0

def Ax (x : X) : X :=
fun i => ∑ j, A i j * x j

def H (x : X) : ℝ :=
‖(fun i => Ax x i - b i)‖^2

def phi (x : X) : ℝ :=
x 0 - x 1

def Hc : ℝ := 1.0

------------------------------------------------------------
-- 2. Continuity
------------------------------------------------------------

theorem H_continuous : Continuous H := by
  unfold H Ax
  -- Ax is linear → continuous
  have h1 : Continuous (fun x : X => fun i => Ax x i - b i) := by
    apply Continuous.sub
    · apply Continuous.comp
      · exact continuous_id
      · exact continuous_const
    · exact continuous_const
  -- norm and square preserve continuity
  exact Continuous.pow 2
    (Continuous.norm h1)

------------------------------------------------------------
-- 3. Nonnegativity
------------------------------------------------------------

theorem H_nonneg (x : X) : 0 ≤ H x := by
  unfold H
  exact sq_nonneg _

------------------------------------------------------------
-- 4. Existence of Critical State
------------------------------------------------------------

-- Assume existence of x₁, x₂ such that
-- H x₁ < Hc and H x₂ > Hc

theorem critical_exists
  (x₁ x₂ : X)
  (h₁ : H x₁ < Hc)
  (h₂ : H x₂ > Hc) :
  ∃ x : X, H x = Hc := by

  -- Define line segment γ(t) = (1-t)x₁ + t x₂
  let γ : ℝ → X :=
    fun t i => (1 - t) * x₁ i + t * x₂ i

  have hγ_cont : Continuous (fun t => H (γ t)) :=
    H_continuous.comp
      (by
        apply Continuous.funext
        intro i
        apply Continuous.add
        · apply Continuous.mul
          · exact continuous_const.sub continuous_id
          · exact continuous_const
        · apply Continuous.mul
          · exact continuous_id
          · exact continuous_const)

  -- Intermediate Value Theorem
  have h_low : H (γ 0) = H x₁ := by simp [γ]
  have h_high : H (γ 1) = H x₂ := by simp [γ]

  have : ∃ t ∈ Set.Icc 0 1, H (γ t) = Hc :=
    by
      apply IntermediateValue_Icc
      · exact hγ_cont
      · simp [h_low, h₁]
      · simp [h_high, h₂]

  rcases this with ⟨t, _, ht⟩
  exact ⟨γ t, ht⟩

------------------------------------------------------------
-- 5. Criticality Definition
------------------------------------------------------------

def Critical (x : X) : Prop :=
H x = Hc

------------------------------------------------------------
-- 6. Local Stability (Linearization Level)
------------------------------------------------------------

-- Toy economic dynamic on order parameter
def f (φ : ℝ) : ℝ :=
φ - φ^3

-- Fixed point definition
def FixedPoint (φ : ℝ) : Prop :=
f φ = 0

-- Stability via derivative sign
def Stable (φ : ℝ) : Prop :=
deriv f φ < 0

-- Example: 0 is unstable
theorem zero_unstable : ¬ Stable 0 := by
  unfold Stable f
  simp [deriv_id'', deriv_pow]
  -- derivative at 0 is positive
  norm_num
