#*********************************
# Bash script to automate creation of scanner using flex and tokenize numbered html docs
# 
# How to call:
#   $ ./process_html.sh <input dir> <output dir> <max>
# Where:
#	<input dir>  the input directory, i.e. where we want to extract the numbered HTML documents
#	<output dir> where the processed/tokenized HTML documents will be stored
#	<max> 		 (OPTIONAL) the largest numbered HTML document to tokenize, it is 999 by default
# 
# Author: Manuel Serna-Aguilera
#*********************************

# Error check
if [ -z $1 ] || [ -z $2 ]
then
	echo "Error: must specify input and output directories."
	exit 9999
fi

in_dir=$1
out_dir=$2

# Make sure output directory exists for processed docs
if [ ! -d "./$out_dir" ]
then
	mkdir $out_dir
	echo "Created directory \"$out_dir\" to store processed docs."
fi


# Create scanner using flex
flex token.lex
g++ -o token lex.yy.c -lfl


# Process numbered html files
j=1
max=$3

if [ -z "$max" ]
then
	max=999
fi

while [ $j -le $max ]
do
	# Check if file exists
	if [ -e ./$in_dir/$j.html ]
	then
		./token ./$in_dir/$j.html > ./$out_dir/$j.out
	fi

	((j++))
done

