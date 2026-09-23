"""
properties.py

Handles SMILES parsing and molecular property calculation using RDKit.
"""

from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski


def parse_smiles(smiles: str):
    """
    Parse a SMILES string into an RDKit Mol object.
    Returns None if the SMILES is invalid.
    """
    if not smiles or not smiles.strip():
        return None
    mol = Chem.MolFromSmiles(smiles.strip())
    return mol


def calculate_properties(mol) -> dict:
    """
    Calculate the core physicochemical properties used in
    Lipinski's Rule of Five and Veber's Rules.

    Returns a dict of property name -> value.
    """
    return {
        "molecular_weight": round(Descriptors.MolWt(mol), 2),
        "logp": round(Crippen.MolLogP(mol), 2),
        "h_bond_donors": Lipinski.NumHDonors(mol),
        "h_bond_acceptors": Lipinski.NumHAcceptors(mol),
        "rotatable_bonds": Descriptors.NumRotatableBonds(mol),
        "tpsa": round(Descriptors.TPSA(mol), 2),  # topological polar surface area
        "molecular_formula": Chem.rdMolDescriptors.CalcMolFormula(mol),
    }
