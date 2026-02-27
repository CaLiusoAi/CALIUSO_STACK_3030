---- MODULE LAYER1_CATHEDRAL ----
EXTENDS Naturals, Reals, Sequences

VARIABLES phase, ledger

Phases == {"initialized", "active", "sealed"}

Init ==
    /\ phase = "initialized"
    /\ ledger = << >>

CanAdvance(p) ==
    p \in Phases

Next ==
    /\ phase' \in Phases
    /\ CanAdvance(phase')
    /\ ledger' = Append(ledger, <<phase, phase'>>)

Invariant ==
    /\ phase \in Phases
    /\ Len(ledger) >= 0

Spec == Init /\ [][Next]_<<phase, ledger>>

====
