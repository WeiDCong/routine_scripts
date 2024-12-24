#!/usr/bin/env python3
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Scaffolds import MurckoScaffold

smi_file = "example.csv"
smi_data = pd.read_csv(smi_file)
smi_list = np.array(smi_data[['smiles']]).flatten()

mol_list = np.array([Chem.MolFromSmiles(smi) for smi in smi_list])
scaffold_smi = np.array([MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=True) for mol in mol_list])
uniq_scaffolds = np.unique(scaffold_smi)

cluster_name = [f"scaffold_cluster_{n}" for n in range(len(uniq_scaffolds))]
for cluster, name in zip(uniq_scaffolds, cluster_name):
    print(cluster)
    idx = np.where(np.array(scaffold_smi) == cluster)
    smi_list = np.array([smi_list[i] for i in idx]).reshape(-1,1)

    smi_df = pd.DataFrame(smi_list)
    smi_df.to_csv(f"{name}.csv", index=False, columns=[f"scaffold: {cluster}"])