# Drug-Likeness Checker

live demo: https://drug-likeness-checker-py.streamlit.app/

A tool that screens small molecules for oral drug-likeness using
**Lipinski's Rule of Five** and **Veber's Rules** — early-stage
filters commonly used in pharmaceutical R&D to flag promising drug
candidates before committing to expensive wet-lab testing.

## What it does

Enter a molecule as a SMILES string (or pick a known drug from the
dropdown) and the app will:

- Render its 2D structure
- Calculate molecular weight, LogP, H-bond donors/acceptors,
  rotatable bonds, and topological polar surface area (TPSA)
- Check the molecule against Lipinski's Rule of Five
- Check the molecule against Veber's Rules
- Give an overall plain-English drug-likeness verdict

## Why these rules

Lipinski's Rule of Five (1997) predicts oral bioavailability from
four simple properties — molecules that are too large, too greasy
(lipophilic), or have too many hydrogen bond donors/acceptors tend
to absorb poorly in the gut. Veber's Rules (2002) add two more
checks — molecular flexibility and polar surface area — that catch
some drug-like failures Lipinski's rules miss.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repo structure

- `app.py` — Streamlit UI
- `properties.py` — SMILES parsing + property calculation (RDKit)
- `rules.py` — Lipinski/Veber rule evaluation logic
- `sample_molecules.py` — preloaded example drugs

## Built with

Python, RDKit, Streamlit
