//********************************
/*
 Objective: Use the multi-way merge algorithm to store terms/tokens from an input subdirectory and store the documents' and term information in a lexicon file (dict.txt), postings file (post.txt), and mapping file (docs.txt).
 NOTE: input documents are assumed to be numbered txt files (e.g. 7.txt) that contain processed tokens (called terms in this stage).

 Compile:
	$ g++ -std=c++0x index.cpp hashTable.cpp -o index

 How to call:
	$ ./index <max> <read_dir> <pass1_dir> <index_dir>

  where:
	<max> 		is the last numbered file in the collection of processed documents
	<read_dir>	is where we will read the collection of processed documents (terms/tokens) from
	<pass1_dir> is the directory that will contain the temporary files after multi-way merge's first phase
	<index_dir> is the directory where the final dict.txt, post.txt, and map.txt files will reside
 
 Author: Manuel Serna-Aguilera
 6 Oct, 2020
*/
//*******************************

#include "hashTable.h"
#include <cstdlib>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
using namespace std;

// NOTE: to test on smaller docs in merge_test directories, use 30 as global ht size and 15 for local ht size

const unsigned long GLOBAL_SIZE = 90000;// size of global hash table
const unsigned long LOCAL_SIZE = 27000;// size of local hash tables


//================================
// Quicksort for string arrays
//================================
int partition(string A[], int low, int high)
{
    string x = A[high];
    int i = low-1;
    
    for (int j=low; j<high; j++)
    {
        if (A[j] <= x)
        {
            i++;
            string temp = A[i];
            A[i] = A[j];
            A[j] = temp;
        }
    }
    
    string temp = A[i+1];
    A[i+1] = A[high];
    A[high] = temp;
    
    return i+1;
}

void quicksort(string A[], int low, int high)
{
    if (low < high)
    {
        int q = partition(A, low, high);// assign partition element to index q
        quicksort(A, low, q-1);
        quicksort(A, q+1, high);
    }
}


//================================
// Multi-Way Merge Algorithm: build lexicon (dict.txt), postings (post.txt), and mapping file (docs.txt)
/*
 Input:
	maxDoc: name of (numerically) last document in collection
	inputDir: where to read (tokenized) input documents from
	pass1Dir: temp directory to store local post files from phase 1
	finalDir: directory name where inverted file files will be written to
 Return: NA
*/
//================================
void multiWayMerge(int maxDoc, const string inputDir, const string pass1Dir, const string finalDir)
{
	// Setup: directory info
	string dir = "./" + inputDir +"/";// where to read files for pass 1
	string outDir1 = "./" + pass1Dir + "/";// where to store temp files after pass 1
	string indexDir = "./" + finalDir + "/";// where to store final inverted file files
	
	string fileExtension = ".txt";// types of files were are looking for
	string filePath = "";// store full path to file here; we will try to open/write this file later

	string dict = "dict.txt";
	string post = "post.txt";
	string map = "map.txt";

	// Initialize hash tables
	HashTable globalHT(GLOBAL_SIZE);
	HashTable localHT(LOCAL_SIZE);
	
	//-------------------------------
	// Phase 1: iterate through each input file and create temporary local postings files
	//-------------------------------
	for (int i = 1; i <= maxDoc; i++)
	{
		int j = i-1;// use i for file names, but j for internal operations

		// Open file i
		filePath = dir + to_string(i) + fileExtension;
		ifstream inFile;
		inFile.open(filePath.c_str());

		// Check if file i exists
		if (!inFile)
		{
			inFile.close();
			continue;// go to next numbered document
		}

		// 1. Insert terms into local hash table
		string term;
		while (inFile >> term)
		{
			localHT.insertTerm(term);// NOTE: this also updates NumDocs accordingly
		}

		// 2. Insert terms from local ht to global ht (if not present already), and update NumDocs for term
		for (unsigned long k = 0; k < localHT.getHTSize(); k++)
		{
			// Make sure to consider non-empty entries
			string localTerm = localHT.searchTerm(k);// search local term only once
			if (localTerm != EMPTY)
			{
				// Check if term in local ht is NOT in global ht
				if (!globalHT.searchTerm(localTerm))
				{
					globalHT.insertTerm(localTerm);// insert new term (and init NumDocs to 1)
				}
				else
				{
					globalHT.updateNumDocs(localTerm);// add 1 to numdocs of term
				}
			}
		}

		// 3. Sort terms of local hash table before writing to temp file i
		unsigned long totFreq = localHT.getCorpusSize();
		string localTerms[totFreq];// insert terms one at a time here

		int sortIndex = 0;
		for (unsigned long k = 0; k < localHT.getHTSize(); k++)
		{
			string localTerm = localHT.searchTerm(k);// get current term in local ht

			if (localTerm != EMPTY)
			{
				localTerms[sortIndex] = localTerm;
				sortIndex++;// move on to next spot in sort array
			}
		}

		quicksort(localTerms, 0, totFreq-1);

		inFile.close();// close input file

		// 4. Write sorted array to file i.txt
		filePath = outDir1 + to_string(i) + fileExtension;// specify full output file name and path
		ofstream outFile;
		outFile.open(filePath);

		// Write: term, term frequency
		// NOTE: I did not store doc IDs since they are implied with the index of the loop/file name
		for (int k=0; k<totFreq; k++)
		{
			string term = localTerms[k];
			//outFile << term << " " << i << " "  << localHT.searchTermFreq(term) << endl;
			outFile << term << " " << localHT.searchTermFreq(term) << endl;
		}

		outFile.close();// close output file
		localHT.reset();// reset local hash table
	}

	//-------------------------------
	// Phase 2: write to sorted postings file
	//-------------------------------
	//globalHT.printDict();// so far, global ht contains correct values
	
	ifstream files[maxDoc];// array of ifstream objects to keep track of file contents
	string buffer[maxDoc];// buffer array to hold file records

	// Load first line for all documents into buffer array
	// NOTE: index i is for file names, index j is for arrays
	for (int i=1; i<=maxDoc; i++)
	{
		int j = i-1;
		
		filePath = outDir1 + to_string(i) + fileExtension;
		files[j].open(filePath);

		// Load first lines of each file into buffer, also account for non-existent files
		if (!files[j].fail())
		{
			getline(files[j], buffer[j]);
		}
	}

	// Loop over buffer until all elements are empty, i.e. ""
	bool done = false;// "done inserting from buffer?"
	long start = 0;// keep track of start for each term in dict
	ofstream postFile;
	postFile.open(indexDir+post);

	while (!done)
	{
		// Assign 'first'
		string first = "zzzzzzzz";// to be alphabetically first term in current buffer
		for (int j=0; j<maxDoc; j++)
		{
			// Check if term from buffer is valid (not empty str)
			string termJ = buffer[j].substr(0, buffer[j].find(' '));
			if (termJ.size() <= 0)
			{
				continue;
			}
			
			// Keep getting the alphabetically least word (starting from many z's)
			if (first.compare(termJ) > 0)
			{
				first = termJ;
			}
			
		}
		
		globalHT.setStart(first, start);// set start for current 'first' term

		// Insert all instances of term 'first' to postings
		for (int j=0; j<maxDoc; j++)
		{
			if (first == buffer[j].substr(0, buffer[j].find(' ')))
			{
				int i = j+1;
				postFile << i << " " << buffer[j].substr(first.size()+1) << endl;
				//postFile << first << " " << i << " " << buffer[j].substr(first.size()+1) << endl;// DEBUG print token to confirm position in post and dict
				getline(files[j], buffer[j]);// reload buffer
				start++;// update start for next term
			}
		}

		// Check if all buffers are empty
		for (int j=0; j<maxDoc; j++)
		{
			if (!files[j].fail())
			{
				break;// if we can still open files, continue reading from buffer
			}
			else if ((files[j].fail()) && (j == maxDoc-1))
			{
				done = true;// done when at last index and file open fils
			}
		}
	}
	postFile.close();// close completed post file

	// Close all files in buffer
	for (int j=0; j<maxDoc; j++)
	{
		files[j].close();
	}

	// Write global hash table to file as the completed dict file
	globalHT.writeDict(indexDir+dict);

	// Write docs file (NOTE: original docs were HTML docs)
	ofstream mapFile;
	mapFile.open(indexDir+map);
	for (int j=1; j<=maxDoc; j++)
	{
		mapFile << j << " " << j << ".html" << endl;
	}
}


//================================
// Main
//================================
int main(int argc, char** argv)
{
	// Setup: cmd parameters
	int maxDoc = atoi(argv[1]);// declare up to what file id we are considering
	string inputDir = argv[2];// name of subdirectory where we will read input files from
	string pass1Dir = argv[3];// pass 1 temp post files, 1 per input file from inputDir
	string indexDir = argv[4];// subdirectory where inverted file txt files will be written to
	
	// Call multi-way merge function
	multiWayMerge(maxDoc, inputDir, pass1Dir, indexDir);

	return 0;
}

