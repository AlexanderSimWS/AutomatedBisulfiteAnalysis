import os
from Bio.Seq import Seq
import pandas as pd
import plotly.express as px

#****************************************READ ME***********************************
# This program helps you analyse bisulfite methylation in a given PCR product (between your primers)
# Inputs: Control samples (.fasta files) in a single folder, Perturbed samples (.fasta files) in another folder
# Outputs: Methylation positions and mean % methylation

# You have to use MethPrimer to find CpG islands of interest first
#**********************************************************************************


#****************************************User Config***********************************
# 1. Change these manually based on what you see in MethPrimer
before_first_cpg = 'TAGTATAAAAGGGG'
after_last_cpg = 'TAATTTTTT'
total_no_of_cpg = 11
no_of_control_samples = 9
no_of_perturbed_samples = 5

# 2. Change the name of your output based on the naming format of your input files in READ_ALL_FILES() (Indicated by "-----> Change me!")
# 3. Remove false CpG sites (sites that are 'CG' but are not predicted by MethPrimer) by changing the "seq[0:8] + seq[9] + seq[11:13]" indexes in FIND_METHYL() (Indicated by "-----> Change me!")

# Hope this helps someone
#**************************************************************************************

control_list = []
control_index = []
control_trunc_list = []
perturbed_list = []
perturbed_index = []
perturbed_trunc_list = []
control_methylation = []
perturbed_methylation = []
control_methyl_dict = {}
perturbed_methyl_dict = {}

# Read all .fasta files in specified folder
def READ_ALL_FILES(folder_name, list_to_append, index_list):
	# Get path to folder as string
	directory = os.fsencode(folder_name)
	
	# Read all .fasta files in folder
	for file in os.listdir(directory):
		line_count = 0
		file_name = os.fsdecode(file)
		file_path = os.getcwd() + '/' + folder_name + '/' + file_name
		
		contents = ''
		if file_name.endswith('.fasta'):
			temp_file = open(file_path, 'r')
			# Get augmented file names (specific to my inputs)
			aug_file_name = (file_name.split('.', 3)[0]).split('_')[4] # -----> Change me!
			index_list.append(aug_file_name)
			# Read .fasta file except first line
			while True:
				line = temp_file.readline()
				line_count += 1
				if line_count > 1:
					line = line.strip()
					contents = contents + line
				if not line:
					break
			temp_file.close()
			list_to_append.append(contents)
			continue
		else:
			continue

def FIND_METHYL(selected_list, selected_methyl_list):
	# Check if sequence is actually reverse compliment
	for seq in selected_list:
		if ((before_first_cpg in seq) == True): # Normal order
			print('seq ' + str(selected_list.index(seq)) + ' is normal')
		elif ((str(Seq(before_first_cpg).reverse_complement()) in seq) == True): # Get reverse complement
			print('Getting reverse complement of seq ' + str(selected_list.index(seq)))
			selected_list[selected_list.index(seq)] = str(Seq(seq).reverse_complement())
		else:
			print('Segment not found!')

	# Truncate sequence to region with CpG islands
	for seq in selected_list:
		temp_methylation_string = ''
		reading_window = []
		
		# Remove region right before first CpG island
		split_seq = seq.split(before_first_cpg, 1)[1]
		
		# Take incomplete conversion into account
		unconverted_segment_before_reverse_primer = after_last_cpg
		for char in unconverted_segment_before_reverse_primer:
			if char == 'T':
				char = 'C'

		# Remove region right after last CpG island
		if ((after_last_cpg in seq) == True):
			trunc_seq = split_seq.split(after_last_cpg, 1)[0]
		elif ((unconverted_segment_before_reverse_primer in seq) == True):
			trunc_seq = split_seq.split(unconverted_segment_before_reverse_primer, 1)[0]

		# Search for CpG islands
		for char in trunc_seq:
			if len(reading_window) < 2:
				reading_window.append(char)
			else:
				reading_window.pop(0)
				reading_window.append(char)

			if reading_window == ['C', 'G']:
				temp_methylation_string += 'O'
			if reading_window == ['T', 'G']:
				temp_methylation_string += '_'

		selected_methyl_list.append(temp_methylation_string)

	for seq in selected_methyl_list:
		selected_methyl_list[selected_methyl_list.index(seq)] = seq[0:8] + seq[9] + seq[11:13] # -----> Change me!

def MAKE_DICT():
	control_count = 0
	perturbed_count = 0

	for element in control_methylation:
		control_methyl_dict[control_index[control_count]] = element
		control_count += 1
	
	for element in perturbed_methylation:
		perturbed_methyl_dict[perturbed_index[perturbed_count]] = element
		perturbed_count += 1

def PRINT_OUTPUT():
	total_control_methyl = 0
	total_perturbed_methyl = 0
	control_methyl_percentage = 0
	perturbed_methyl_percentage = 0

	print('Control Group Methylation:')
	for key in sorted(control_methyl_dict.keys()):
		print(key, ': ', control_methyl_dict[key], '; ', control_methyl_dict[key].count('O'))
		total_control_methyl += control_methyl_dict[key].count('O')

	print('\nPerturbed Group Methylation:')
	for key in sorted(perturbed_methyl_dict.keys()):
		print(key, ': ', perturbed_methyl_dict[key], '; ', perturbed_methyl_dict[key].count('O'))
		total_perturbed_methyl += perturbed_methyl_dict[key].count('O')

	control_methyl_percentage = (total_control_methyl/(no_of_control_samples*total_no_of_cpg))*100
	perturbed_methyl_percentage = (total_perturbed_methyl/(no_of_perturbed_samples*total_no_of_cpg))*100

	print('\nStatistics:')
	print('Control Methylation Percentage: ', control_methyl_percentage, '%')
	print('Perturbed Methylation Percentage: ', perturbed_methyl_percentage, '%')

	# #*******************Uncomment for a bar chart of the methylation percentage for control and perturbed groups*******************

	# fig_data = [['Control Group', control_methyl_percentage], ['Perturbed Group', perturbed_methyl_percentage]]
	# df = pd.DataFrame(fig_data, columns = ['Group', 'Percentage Methylation (%)'])
	# # print(df.to_string())
	# fig = px.bar(df, y='Percentage Methylation (%)', x='Group', color='Group')
	# fig.update_layout(
	# 	font = dict(
	# 		family = 'Arial',
	# 		size = 24
	# 		),
	# 	width = 500,
	# 	showlegend = False
	# )
	# fig.show()
	
	# #*****************************************************************************************************************************

def MAIN():
	READ_ALL_FILES('control_samples', control_list, control_index)
	READ_ALL_FILES('perturbed_samples', perturbed_list, perturbed_index)
	FIND_METHYL(control_list, control_methylation)
	FIND_METHYL(perturbed_list, perturbed_methylation)
	MAKE_DICT()
	print('\nInputs have been processed!\n')
	PRINT_OUTPUT()


MAIN()