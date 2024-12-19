#!/usr/bin/env python3

"""
This script is for batch conversion of molecular file formats.
For example, from xyz to sdf.
"""

from openbabel import pybel
import pandas as pd

from tqdm import tqdm
from glob import glob
import sys


def process_chunk(file, input_format, output_format):
    outputs = []
    for mol in pybel.readfile(input_format, file):
        out = mol.write(output_format)
        outputs.append(out)
    return outputs

def converter(file_list, input_format, output_format):
    for file in tqdm(file_list):
        out_chunks = process_chunk(file, input_format, output_format)
        out_file_name = file.replace(input_format, output_format)
        with open(out_file_name, 'w') as ofile:
            ofile.writelines(out_chunks)

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 3:
        input_format = args[1].lower()
        output_format = args[2].lower()
        file_list = glob(f"*.{input_format}")
        out_smiles = converter(file_list, input_format, output_format)
    else:
        print(f'usage: {args[0]} input_format output_format')
        print(f'e.g., {args[0]} xyz sdf')
        exit