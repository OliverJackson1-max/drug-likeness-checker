"""
rules.py

Evaluates calculated molecular properties against medicinal chemistry
screening rules: Lipinski's Rule of Five and Veber's Rules.
"""


def evaluate_lipinski(props: dict) -> dict:
    """
    Lipinski's Rule of Five. A molecule is considered likely to be
    orally bioavailable if it violates no more than one rule.
    """
    checks = {
        "Molecular weight <= 500 Da": props["molecular_weight"] <= 500,
        "LogP <= 5": props["logp"] <= 5,
        "H-bond donors <= 5": props["h_bond_donors"] <= 5,
        "H-bond acceptors <= 10": props["h_bond_acceptors"] <= 10,
    }
    violations = sum(not passed for passed in checks.values())
    return {
        "checks": checks,
        "violations": violations,
        "passes": violations <= 1,
    }


def evaluate_veber(props: dict) -> dict:
    """
    Veber's Rules. Predicts good oral bioavailability based on
    molecular flexibility and polar surface area — catches some
    cases Lipinski misses.
    """
    checks = {
        "Rotatable bonds <= 10": props["rotatable_bonds"] <= 10,
        "TPSA <= 140 Å²": props["tpsa"] <= 140,
    }
    violations = sum(not passed for passed in checks.values())
    return {
        "checks": checks,
        "violations": violations,
        "passes": violations == 0,
    }


def overall_verdict(lipinski: dict, veber: dict) -> str:
    """Combine both rule sets into a single plain-English verdict."""
    if lipinski["passes"] and veber["passes"]:
        return "Drug-like — passes Lipinski and Veber filters"
    elif lipinski["passes"]:
        return "Borderline — passes Lipinski but fails Veber's flexibility/polarity rules"
    else:
        return "Unlikely to be orally bioavailable — fails Lipinski's Rule of Five"
