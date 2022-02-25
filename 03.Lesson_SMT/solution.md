## Solving Puzzle
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(push)
(assert (= (+ x x) 10))
(assert (= (+ y (* x y)) 12))
(assert (= (- (* x y) (* z x)) x))
(check-sat)
(get-model)

Result :
sat
(
  (define-fun z () Real
    1.0)
  (define-fun y () Real
    2.0)
  (define-fun x () Real
    5.0)
)

## Equivalence Check
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
(define-fun conjecture () Bool
    (= (= (and p q) p) (=> p q)))
(assert (not conjecture))
(check-sat)

Result : unsat. Hence formulas are equivalent 


