"""
app.py

Streamlit UI for the Drug-Likeness Checker.
Lets a user enter a SMILES string (or pick a known drug), view its
2D structure, and see whether it passes Lipinski's Rule of Five
and Veber's Rules.
"""

import streamlit as st
from rdkit.Chem import Draw

from properties import parse_smiles, calculate_properties
from rules import evaluate_lipinski, evaluate_veber, overall_verdict
from sample_molecules import SAMPLE_MOLECULES

st.set_page_config(page_title="Drug-Likeness Checker", page_icon="🧪")
st.title("🧪 Drug-Likeness Checker")
st.caption("Screen a molecule against Lipinski's Rule of Five and Veber's Rules")

# --- Input ---
choice = st.selectbox("Try an example molecule", ["Custom SMILES"] + list(SAMPLE_MOLECULES.keys()))
default_smiles = "" if choice == "Custom SMILES" else SAMPLE_MOLECULES[choice]
smiles = st.text_input("Or enter a SMILES string", value=default_smiles)

if smiles:
    mol = parse_smiles(smiles)

    if mol is None:
        st.error("Couldn't parse that SMILES string. Check the syntax and try again.")
    else:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(Draw.MolToImage(mol, size=(300, 300)), caption=choice if choice != "Custom SMILES" else "Structure")

        with col2:
            props = calculate_properties(mol)
            st.subheader(props["molecular_formula"])
            st.write(f"**Molecular weight:** {props['molecular_weight']} Da")
            st.write(f"**LogP:** {props['logp']}")
            st.write(f"**H-bond donors:** {props['h_bond_donors']}")
            st.write(f"**H-bond acceptors:** {props['h_bond_acceptors']}")
            st.write(f"**Rotatable bonds:** {props['rotatable_bonds']}")
            st.write(f"**TPSA:** {props['tpsa']} Å²")

        st.divider()

        lipinski = evaluate_lipinski(props)
        veber = evaluate_veber(props)

        st.subheader(overall_verdict(lipinski, veber))

        rule_col1, rule_col2 = st.columns(2)

        with rule_col1:
            st.markdown(f"**Lipinski's Rule of Five** ({lipinski['violations']} violation(s))")
            for rule, passed in lipinski["checks"].items():
                st.write(("✅ " if passed else "❌ ") + rule)

        with rule_col2:
            st.markdown(f"**Veber's Rules** ({veber['violations']} violation(s))")
            for rule, passed in veber["checks"].items():
                st.write(("✅ " if passed else "❌ ") + rule)
else:
    st.info("Enter a SMILES string above, or pick an example molecule, to get started.")
