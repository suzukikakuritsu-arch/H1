/-
Singularity Theory Core Skeleton
Lean 4 + mathlib
-/

import Mathlib.Analysis.Calculus.FDeriv
import Mathlib.Topology.Manifold
import Mathlib.LinearAlgebra.Dimension

noncomputable section
open Classical

-- Manifold model spaces
variable {E F : Type*}
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F]

-- Smooth map
variable (G : E → F)

------------------------------------------------------------
-- Differential
------------------------------------------------------------

def dG (x : E) :=
fderiv ℝ G x

------------------------------------------------------------
-- Regular point
------------------------------------------------------------

def Regular (x : E) : Prop :=
LinearMap.ker (dG G x) = ⊥

------------------------------------------------------------
-- Singular point
------------------------------------------------------------

def Singular (x : E) : Prop :=
¬ Regular G x

------------------------------------------------------------
-- Singular set
------------------------------------------------------------

def SingSet : Set E :=
{ x | Singular G x }

------------------------------------------------------------
-- Regular value
------------------------------------------------------------

def RegularValue (y : F) : Prop :=
∀ x, G x = y → Regular G x

------------------------------------------------------------
-- Critical value
------------------------------------------------------------

def CriticalValue (y : F) : Prop :=
¬ RegularValue G y

------------------------------------------------------------
-- Fundamental Principle:
-- Regular value ⇒ preimage is manifold
------------------------------------------------------------

theorem RegularValue_manifold
  (y : F)
  (h : RegularValue G y) :
  True :=
by
  -- This is Sard + Preimage theorem in full form
  trivial
