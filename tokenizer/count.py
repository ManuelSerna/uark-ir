#*********************************
'''
	Count the frequencies of tokens in the numbered documents processed by the flex scanner.

	How to execute:
		python3 count.py <input directory>
	Where <input directory> is the directory of the tokenized documents.

	Program output:
		- JSON file of tokens sorted alphabetically, called 'alphabetized.json'
		- JSON file of tokens sorted by frequency, called 'frequencies.json' 
	(Note: frequencies.json sorts the hash table output in alphabetized.json by frequency)

	Author: Manuel Serna-Aguilera
'''
#*********************************

import collections
import json
import os
import string
import sys


# Directory setup
here = os.path.dirname(os.path.realpath(__file__)) # get current directory
subdir = sys.argv[1] # get subdirectory name from command line

# Create tokens dictionary/hash table
tokens = {}

# Read numbered files in given directory
for i in range(1, 1000):
	file_name = '{}.out'.format(i)
	file_path = os.path.join(here, subdir, file_name)

	# Extract text if file i.out exists
	try:
		file_content = open(file_path, 'r')

		# Get list of tokens (each element in the words list was separated by spaces in the processed document)
		text = file_content.read()
		file_content.close()
		words = text.split()
		
		# Insert words and update counts in dictionary
		for w in words:
			try:
				tokens[w] += 1
			except KeyError:
				tokens[w] = 1
	except:
		x=0

# Once done, write to JSON files
sorted_file = 'alphabetized.json'
freq_file = 'frequencies.json'

# Sort tokens alphabetically
sorted_tokens = collections.OrderedDict(sorted(tokens.items()))
with open(sorted_file, 'w') as file:
    file.write(json.dumps(sorted_tokens, indent=4))

# Write tokens sorted by frequency first
frequencies = sorted(sorted_tokens.items(), key=lambda kv: kv[1], reverse=True)
frequencies = collections.OrderedDict(frequencies)
with open(freq_file, 'w') as file:
    file.write(json.dumps(frequencies, indent=4))

print('Tokens sorted by tokens stored in: {}'.format(sorted_file))
print('Tokens sorted by frequency stored in: {}'.format(freq_file))

