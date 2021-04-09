# Automated Bisulfite Analysis

## Overview
A simple automated bisulfite analysis Python script to determine the methylation status of CpG sites (Predicted by MethPrimer) given sequences of control samples (.fasta files) and sequences of perturbed samples (also .fasta files). Read below for very brief background information, usage instructions and an example output.

In brief, it allows the automated analysis of the extent of methylation of cells after being exposed to a perturbation (e.g. cigarette smoke).

Can be run from terminal in Mac OS.

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
Treatment of DNA with bisulfite converts cytosine residues to uracil but leaves methylated cytosines unaffected. After direct sequencing, unmethylated cytosines are displayed in the sense strand as thymine residues. These are called CpG islands. This script compares the original sequence found in MethPrimer with control sequences and perturbed sequences. 

In my experiment, RNA was extracted from control and perturbed samples, converted into cDNA, treated with bisulfite and then ligated into a TOPO vector (ThermoFisher) and subsequently E. Coli. These were grown on an agar plate containing X-gal and successfully transformed bacterial colonies were observed as white colonies instead of blue colonies. These successfully transformed bacterial colonies were picked by a pipette and sequenced.

https://en.wikipedia.org/wiki/Bisulfite_sequencing

### MethPrimer
MethPrimer is a program for designing bisulfite-conversion-based Methylation PCR Primers. Currently, it can design primers for two types of bisulfite PCR: 1) Methylation-Specific PCR (MSP) and 2) Bisulfite-Sequencing PCR (BSP) or Bisulfite-Restriction PCR. MethPrimer can also predict CpG islands in DNA sequences.

https://www.urogene.org/methprimer/

Relevant functionalities of MethPrimer are designing primers for bisulfite-sequencing PCR and prediction of CpG islands.


## Quick Start
### Dependencies
Ensure you have the following libraries installed:
`pip install biopython`<br/>
https://biopython.org/wiki/Download<br/>
`pip install pandas`<br/>
https://pypi.org/project/pandas/<br/>
`pip install plotly-express`<br/>
https://pypi.org/project/plotly-express/<br/>


### Preparing the files and understanding your data
Assuming you've already conducted bisulfite PCR and have the sequences of your control and perturbation samples perform the following steps:
1. Identify the sequence you're analysing with MethPrimer and index (0 indexed) all the CpG islands between your forward and reverse primers (Indicated by GC in the original stand on top)
2. Identify false CpG sites (GC sequences that MethPrimer does not recognise as a CpG site, predicted CpG sites are indicated by a "++" between the top and bottom strand) and note their index.
3. MethyPrimer displays 2 strands (the strand on top is the original sequence and the strand at the bottom is the bisulfite treated sequence). Visually identify a sequence that is unaffected by bisulfite sequencing after your forward primer and just before the first CpG island. Find another short sequence after your last CpG island and before your reverse primer. Enter these in the .py file as the variables "before_first_cpg" and "after_last_cpg" respectively. This allows the program to zoom in on the area of DNA with CpG sites.
5. Place all your .fasta files of your control sequences into the `control_samples` folder
6. Place all your .fasta files of your perturbed sequences into the `perturbed_samples` folder

### Running the program from terminal
1. Prepare your sequences and modify variables in the `bisulfite_analysis.py` file as shown above
2. Navigate to the the folder you placed `bisulfite_analysis.py`, `control_samples` and `perturbed_samples` with<br/>
`cd path/to/folder`
3. Run the program with<br/>
`python bisulfite_analysis.py`
4. For a graph of the statistics, uncomment the last block of code in the `PRINT_OUTPUT()` function in the `bisulfite_analysis.py` file

## Example Output
Control Group Methylation:<br/>
A07 :  __________O ;  1<br/>
A08 :  __________O ;  1<br/>
B07 :  _________OO ;  2<br/>
C07 :  __________O ;  1<br/>
D07 :  O_________O ;  2<br/>
E07 :  __________O ;  1<br/>
F07 :  ___O______O ;  2<br/>
G07 :  __________O ;  1<br/>
H07 :  _O________O ;  2<br/>

Perturbed Group Methylation:<br/>
A12 :  ______OO__O ;  3<br/>
B12 :  ______OOO_O ;  4<br/>
C12 :  ______O_O_O ;  3<br/>
D12 :  ______OO__O ;  3<br/>
E12 :  _______OO_O ;  3<br/>

Statistics:<br/>
Control Methylation Percentage:  13.131313131313133 %<br/>
Perturbed Methylation Percentage:  29.09090909090909 %<br/>

Optional bar graph of statistics can be produced by uncommenting the relevant code in the .py file.
