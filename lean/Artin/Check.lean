/-
Axiom audit. Every non-private declaration of this development is listed
below. `gate.sh` requires each to depend only on a subset of Lean's three
standard axioms (propext, Classical.choice, Quot.sound), and pins the expected
number of reports so that silently deleting an audit line fails the gate
rather than passing vacuously.
-/
import Artin.Paper2
import Artin.Paper2Rebuild

#print axioms Paper2.three_primitiveRoot_five
#print axioms Paper2.three_primitiveRoot_seven
#print axioms Paper2.group_orders
#print axioms Paper2.refutation_gap_two_base_three
#print axioms Paper2.chi
#print axioms Paper2.nmm
#print axioms Paper2.nmm_five
#print axioms Paper2.nmm_thirteen
#print axioms Paper2.paper_formula_fails_at_zero
#print axioms Paper2.nmm_five_vanishes
#print axioms Paper2.nmm_thirteen_never_vanishes
#print axioms Paper2Rebuild.four_mul_indicator
#print axioms Paper2Rebuild.main_identity
#print axioms Paper2Rebuild.counting_identity
