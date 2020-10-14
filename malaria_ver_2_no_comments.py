#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: malaria_ver_2.py
Date: 2020-10-09
Author: Arthur Boffelli Castro

Description:
    This program will output a fasta file with the an additional informormation
        about the protein related to the sequence, obtained through a
        BlastX-run.
    The user will specify the organism file in fasta format, the blast file
        tab delimited, and the name of the output file.

List of functions:
    No user defined functions are used in this program.

List of "non standard" modules:
    No "non standard" are used in this program.

Procedure:
    1. Create a dictionary with the blast file, key = queryName and
        value = hitDescription.
    2. Compare the queryName from the fasta file with the keys in the
        dictionary to retrieve the right value. The sequences with no hits in
        Blast (null) will not be included in the output file.
    3. Write the fasta information and add the hitDescription in the end of the
        line.

Usage:
    ./running_exercise_1.py input_fasta.fna input_blast.tab output.fna

"""

################################################################
import sys

organism_file = sys.argv[1]
blast_file = sys.argv[2]
result_file = sys.argv[3]

blast_dict = {}

with open(organism_file, 'r') as organism, open (blast_file,
'r') as blast, open (result_file, 'w') as result:
   
    header = blast.readline()

    for blast_line in blast:
        read_line = blast_line.split('\t')
        blast_dict[read_line[0]] = read_line[9]

    for line in organism:
        if line.startswith('>'):
            code_num = line.split('\t')[0].strip('>')
            
            if code_num in blast_dict:
                if blast_dict[code_num] != 'null':
                    result.write('{}\t{}'.format(line.strip('\n'),
                                 blast_dict[code_num]) + '\n')

                else:    # value == null
                    next(organism)  # read sequence line too.
        else:   # sequence line
            result.write(line)
            
