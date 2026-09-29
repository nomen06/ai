VARS = ["A", "B", "C"]
NEIGHBORS = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}

domains = {
    "A": [(1, 1), (2, 1)],
    "B": [(2, 1), (2, 2), (3, 2), (4, 2)],
    "C": [(1, 2), (3, 2), (4, 2)],
}
assignment = {}


def ok(x, p, y, q):
    if {x, y} in ({"A", "B"}, {"B", "C"}) and p[0] == q[0]:
        return False
    if p == q:
        return False
    if {x, y} == {"A", "C"} and abs(p[0] - q[0]) == 1:
        return False
    return True


def show(doms):
    for v in VARS:
        if v in assignment:
            print(f"  {v}: assigned {assignment[v]}")
        else:
            print(f"  {v}: {doms[v] if doms[v] else '{} <-- EMPTY'}")


def degree(v):
    return sum(1 for n in NEIGHBORS[v] if n not in assignment)


def select_variable(doms):
    unassigned = [v for v in VARS if v not in assignment]
    x = min(unassigned, key=lambda v: (len(doms[v]), -degree(v)))
    print("MRV sizes:", {v: len(doms[v]) for v in unassigned},
          "| degrees:", {v: degree(v) for v in unassigned})
    print(f"Selected {x} (domain size {len(doms[x])}, degree {degree(x)})")
    return x


def backtrack(doms, sequence):
    if len(assignment) == len(VARS):
        return True

    x = select_variable(doms)

    for p in list(doms[x]):
        if not all(ok(x, p, y, q) for y, q in assignment.items()):
            print(f"Violation: {x} = {p}")
            continue

        assignment[x] = p
        sequence.append(f"{x} = {p}")
        print(f"\nAssign {x} -> {p}")

        new = {v: list(d) for v, d in doms.items()}
        for y in VARS:
            if y in assignment:
                continue
            new[y] = [q for q in doms[y]
                      if all(ok(y, q, w, r) for w, r in assignment.items())]
            removed = [q for q in doms[y] if q not in new[y]]
            print(f"  FC {y}: {doms[y]} -> {new[y]}"
                  + (f"   removed {removed}" if removed else "   (no change)"))
        show(new)

        if any(y not in assignment and not new[y] for y in VARS):
            print("Empty domain -> Backtracking")
        elif backtrack(new, sequence):
            return True

        del assignment[x]
        sequence.append(f"BACKTRACK {x} = {p}")
        print(f"Backtrack from {x} = {p}")

    return False


if __name__ == "__main__":
    print("Initial domains (after unary constraints):")
    show(domains)
    print()

    seq = []
    found = backtrack(domains, seq)

    print("\nSearch sequence:")
    for i, s in enumerate(seq, 1):
        print(f"{i}. {s}")

    print("\nFinal Schedule" if found else "\nNo valid schedule")
    if found:
        print("Section  Time  Lab")
        for v in VARS:
            t, lab = assignment[v]
            print(f"{v:<8} {t:<5} L{lab}").
