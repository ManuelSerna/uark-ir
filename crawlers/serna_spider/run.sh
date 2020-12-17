#*********************************
# Execute crawler program
# Call:
#   $ ./run.sh <max_pgs>
#
# where
#   <max_pgs> is the max number of pages to crawl
#*********************************

# TODO: eventually i want to feed the program the name of an input doc which
#  contains the starting urls (each in their own line)

if [ -z $1 ]
then
    echo "ERROR: Need to specify number of pages to crawl!"
    exit
fi

echo "Executing SernaSpider."
echo 

python3 SernaSpider.py $1

echo ""
echo "Done."

