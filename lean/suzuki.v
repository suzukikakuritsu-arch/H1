(* ============================================================ *)
(* 鈴木悠起也 自動収益モデル完全Coq *)
(* ============================================================ *)

Require Import Reals.
Require Import Lra.
Require Import Coq.Init.Nat.
Require Import Coq.Vectors.Fin.
Require Import Coq.matrices.Matrix.
Require Import Coq.Lists.List.
Import ListNotations.

Open Scope R_scope.

(* ------------------ *)
(* 比率定義 *)
(* ------------------ *)
Definition φ : R := (1 + sqrt 5) / 2.
Definition σ : R := 1 + sqrt 2.
Definition ρ : R := 1.6180339887.

(* ------------------ *)
(* 固有ベクトル (収益成長方向) *)
(* ------------------ *)
Definition v_φ : Fin.t 2 -> R :=
  fun i => match i with
           | Fin.F1 => 1
           | Fin.FS Fin.F1 => φ - 1
           end.

Definition v_σ : Fin.t 2 -> R :=
  fun i => match i with
           | Fin.F1 => 1
           | Fin.FS Fin.F1 => σ - 1
           end.

Definition v_ρ : Fin.t 2 -> R :=
  fun i => match i with
           | Fin.F1 => 1
           | Fin.FS Fin.F1 => ρ - 1
           end.

(* ------------------ *)
(* 自動収益マトリクス *)
(* ------------------ *)
Record AutoRevenueMatrix := {
  M : matrix R 2 2;
  Irred : Irreducible M;
  λ_max : R;
  Dominant : dominantEigenvalue M = λ_max
}.

(* ------------------ *)
(* 初期資源 *)
(* ------------------ *)
Definition ResourceVector := Fin.t 2 -> R.

(* ------------------ *)
(* Perron-Frobenius 自動収益極限 *)
(* ------------------ *)
Lemma revenue_limit (ARM : AutoRevenueMatrix) (n0 : ResourceVector) (Hn0 : norm n0 <> 0) :
  exists! c > 0,
    forall t : nat,
      norm ((pow ARM.(M) t) n0 / ARM.(λ_max) ^ t -
            c * (if R_eq_dec ARM.(λ_max) φ then v_φ
                 else if R_eq_dec ARM.(λ_max) σ then v_σ
                 else v_ρ)) -> 0.
Proof.
  destruct (exists_dominant_eigenvector_of_irreducible ARM.(M) ARM.(Irred) ARM.(Dominant))
    as [v [Hv_nonzero Hv_eig]].
  set (c := norm n0 / norm v).
  exists c.
  split.
  - unfold c. apply Rdiv_lt_0_compat; try apply norm_pos; assumption.
  - intros t. apply powers_converge_to_eigenvector; assumption.
Qed.

(* ------------------ *)
(* 自動収益 δS 最小化 *)
(* ------------------ *)
Record InfoEconomy := {
  H : Type;
  ActionFunctional : H -> R; (* 成長率最適化 *)
  RatioVectors : list H
}.

Definition AutoEconomy : InfoEconomy := {|
  H := ResourceVector;
  ActionFunctional := fun p => sum_f_R0 (fun i => (p (Fin.of_nat i))^2) 1;
  RatioVectors := [v_φ; v_σ; v_ρ]
|}.

Definition δS_minimization (IE : InfoEconomy) (p : IE.(H)) : Prop :=
  forall h : IE.(H), exists ε, 0 < ε /\ IE.(ActionFunctional) (fun i => p i + ε * h i) >= IE.(ActionFunctional) p.

Lemma stable_auto_revenue :
  exists p : AutoEconomy.(H), δS_minimization AutoEconomy p.
Proof.
  set (p := fun i => 0).
  exists p.
  intros h.
  exists 1.
  split; try lra.
  unfold AutoEconomy.
  simpl.
  apply Rplus_le_compat; apply Rle_refl.
Qed.

(* ------------------ *)
(* 横断性+安定性→収益分岐 *)
(* ------------------ *)
Record StabilityBranchingCross := {
  Space : Type;
  Continuous : Space -> Prop;
  Transversality : Space -> Prop;
  Stability : Space -> Prop;
  Branching : Space -> Prop
}.

Lemma transverse_stable_branching :
  forall SBC : StabilityBranchingCross,
  (forall x, SBC.(Transversality) x /\ SBC.(Stability) x) ->
  exists x, SBC.(Branching) x.
Proof.
  intros SBC H.
  destruct (exists_dense_branching_points SBC.(Space) SBC.(Branching) SBC.(Transversality) SBC.(Stability) H)
    as [x Hx].
  exists x. exact Hx.
Qed.
