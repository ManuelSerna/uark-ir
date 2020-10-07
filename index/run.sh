#*********************************
# Bash script that:
#	1. Automates the creation of a flex scanner
#	2. Tokenizes a collection of numbered HTML documents in a subdirectory
#	3. Reads the temporary collection of tokenized documents to build an inverted file via the multi-way merge algorithm
# 
# How to call:
#   $ ./run.sh <input dir> <output dir> <max>
# Where:
#	<input dir>  the input directory, i.e. where we want to extract the numbered HTML documents
#	<output dir> where the dict, post, and map files will be stored
#	<max> 		 (OPTIONAL) the largest numbered HTML document to tokenize, it is 999 by default
# 
# Required files:
#	token.lex	Lex file that contains tokenization rules
#	hashTable.cpp/.h	Custom hash table class for writing dict and post entries
#	index.cpp	multi-way merge code that uses hash table class
#
# Author: Manuel Serna-Aguilera
#*********************************

#---------------------------------
# 0. Setup
#---------------------------------
# Error check
if [ -z $1 ] || [ -z $2 ]
then
	echo "Error: must specify input and output directories."
	exit 1
fi

in_dir=$1  # first cmd arg is html dir
out_dir=$2 # second cmd arg is output dir

# Make sure output directory exists for 'dict', 'post', and 'map'
dict="dict.txt"
post="post.txt"
map="map.txt"

if [ ! -d "./$out_dir" ]
then
	mkdir $out_dir
	echo "Created directory \"$out_dir\" to store dict, post, and map."
fi



#---------------------------------
# 1. Create scanner using flex
#---------------------------------
echo " Tokenizing..."
flex token.lex
g++ -o token lex.yy.c -lfl



#---------------------------------
# 2. Process numbered html files
#---------------------------------
max=$3 # third cmd arg is num of html docs to process
j=1    # counter for numbered html docs
temp_tokens="temp_tokens" # directory where processed tokens will be kept until they are read by the hash table

# Create temporary directory to store tokenized documents
if [ ! -d "./$temp_tokens" ]
then
	mkdir $temp_tokens
fi

if [ -z "$max" ]
then
	max=999
fi

# Tokenize HTML documents
while [ $j -le $max ]
do
	# Check if file exists
	if [ -e ./$in_dir/$j.html ]
	then
		./token ./$in_dir/$j.html > ./$temp_tokens/$j.txt
	fi

	((j++))
done



#---------------------------------
# 3. Index tokenized documents to build inverted file
#---------------------------------
echo " Indexing..."

temp_index="temp_index" # directory where temp multi-way merge files will be stored
if [ ! -d "./$temp_index" ]
then
	mkdir $temp_index
fi

g++ -std=c++0x index.cpp hashTable.cpp -o index
./index $max $temp_tokens $temp_index $out_dir


#---------------------------------
# N. Clear up memory
#---------------------------------
echo " Cleaning up temp files/directories..."
# Finished, remove any temporary files and directories
rm -r $temp_tokens	# temp storage for tokens
rm -r $temp_index	# temp storage for indexing
rm lex.yy.c			# Lex file that contains DFA
rm token			# lex executable
rm index			# indexing executable



#---------------------------------
echo "Done."

