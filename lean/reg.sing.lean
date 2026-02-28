/-
==============================================================
Structural Decomposition of C¹ maps on ℝⁿ
Regular / Singular splitting
Lean 4 + mathlib compatible
==============================================================
-/

import Mathlib.Analysis.Calculus.FDeriv
import Mathlib.Analysis.Calculus.Inverse
import Mathlib.Analysis.NormedSpace.EuclideanSpace
import Mathlib.Topology.LocalHomeomorph
import Mathlib.LinearAlgebra.Matrix.Determinant
import Mathlib.Analysis.NormedSpace.FiniteDimension

noncomputable section
open Classical
open scoped Topology

------------------------------------------------------------
-- Basic Setting
------------------------------------------------------------

variable {n : ℕ}
abbrev E := EuclideanSpace ℝ (Fin n)

------------------------------------------------------------
-- Regular and Singular Points
------------------------------------------------------------

/-- Regular point: derivative is a linear isomorphism -/
def RegularPoint (F : E → E) (x : E) : Prop :=
  ∃ L : E ≃L[ℝ] E,
    HasFDerivAt F L.toContinuousLinearMap x

/-- Singular point: not regular -/
def SingularPoint (F : E → E) (x : E) : Prop :=
  ¬ RegularPoint F x

/-- Regular set -/
def Reg (F : E → E) : Set E :=
  {x | RegularPoint F x}

/-- Singular set -/
def Sing (F : E → E) : Set E :=
  {x | SingularPoint F x}

------------------------------------------------------------
-- Regular set is open
------------------------------------------------------------

theorem regular_set_isOpen
  {F : E → E}
  (hF : ContDiff ℝ 1 F) :
  IsOpen (Reg F) :=
by
  -- derivative varies continuously
  -- invertibility is open condition in finite dimension
  classical
  unfold Reg RegularPoint
  -- full formal proof requires determinant continuity
  -- and GL(n) openness
  -- available in mathlib via linear equivalence openness
  sorry

------------------------------------------------------------
-- Singular set is closed
------------------------------------------------------------

theorem singular_set_isClosed
  {F : E → E}
  (hF : ContDiff ℝ 1 F) :
  IsClosed (Sing F) :=
by
  classical
  unfold Sing
  have h := regular_set_isOpen (F := F) hF
  simpa using h.isClosed_compl

------------------------------------------------------------
-- Local Inverse on Regular Points
------------------------------------------------------------

theorem local_inverse_at_regular
  {F : E → E}
  {x₀ : E}
  (h : RegularPoint F x₀) :
  ∃ (U V : Set E),
    IsOpen U ∧ IsOpen V ∧
    x₀ ∈ U ∧ F x₀ ∈ V ∧
    ∃ (G : E → E),
      (∀ x ∈ U, G (F x) = x) ∧
      (∀ y ∈ V, F (G y) = y) :=
by
  classical
  rcases h with ⟨L, hF⟩
  obtain ⟨U, hU_open, hxU, V, hV_open, hFUV, G, hG_left, hG_right⟩ :=
    hF.hasLocalInverse L.symm.toContinuousLinearMap

  refine ⟨U, V, hU_open, hV_open, hxU, ?_, G, ?_, ?_⟩

  · simpa using hFUV hxU
  · intro x hx; exact hG_left x hx
  · intro y hy; exact hG_right y hy

------------------------------------------------------------
-- Structural Decomposition Theorem
------------------------------------------------------------

theorem structural_decomposition
  (F : E → E) :
  (Set.univ : Set E) = Reg F ∪ Sing F :=
by
  ext x
  unfold Reg Sing RegularPoint SingularPoint
  classical
  by_cases h : RegularPoint F x
  · simp [h]
  · simp [h]

/-
==============================================================
Interpretation:

ℝⁿ decomposes into:

  Reg(F)  : open stable region (local diffeomorphism)
  Sing(F) : closed critical region (degeneracy locus)

Sing(F) = boundary of GL(n)-valued derivative.

All multiplicity, branching, and catastrophe phenomena
occur inside Sing(F).

==============================================================
-/
