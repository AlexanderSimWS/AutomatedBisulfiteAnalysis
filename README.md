# Automated Bisulfite Analysis

## Overview
A simple automated bisulfite analysis Python script to determine the methylation status of CpG sites (Predicted by MethPrimer) given sequences of control samples (.fasta files) and sequences of perturbed samples (also .fasta files).

Can be run from terminal in Mac OS

## Background
### Epigenetics
Epigenetics is the reversible modification of DNA to change the amount of transcription and, hence, translation of various proteins in organisms.
Gene expression in the transcription stage can be modified in the following ways:
1. DNA Methylation
3. Histone Modification
4. Non-coding DNA

This script focuses on the analysis of the extent of DNA methylation in promoter sequences. Methylation of the promoter sequence inhibits transcription factors from binding to the DNA and represses transcriptional activity

https://www.cdc.gov/genomics/disease/epigenetics.htm

### Bisulfite Sequencing
One way to 

### MethPrimer



## How to Use


## Output
Control Group Methylation:
A07 :  __________O ;  1
A08 :  __________O ;  1
B07 :  _________OO ;  2
C07 :  __________O ;  1
D07 :  O_________O ;  2
E07 :  __________O ;  1
F07 :  ___O______O ;  2
G07 :  __________O ;  1
H07 :  _O________O ;  2

Perturbed Group Methylation:
A12 :  ______OO__O ;  3
B12 :  ______OOO_O ;  4
C12 :  ______O_O_O ;  3
D12 :  ______OO__O ;  3
E12 :  _______OO_O ;  3

Statistics:
Control Methylation Percentage:  13.131313131313133 %
Perturbed Methylation Percentage:  29.09090909090909 %

Optional bar graph of statistics can be produced by uncommenting the relevant code in the .py file.
