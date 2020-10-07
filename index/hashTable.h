//================================
// Hash Table Header File
// Manuel Serna-Aguilera
//================================
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
using namespace std;

const int NONE = -1;
const string EMPTY = "-1";
const string DELETED = "-2";

class HashTable
{
public:
    explicit HashTable(unsigned long size);// constructor takes in size of hash table
    ~HashTable();

	unsigned long getHTSize();// return size of hash table    
    unsigned long getCorpusSize();// return number of unique terms--corpus size of ht
    unsigned long getTotalInserts();// return total insertions
    unsigned long getCollisions();// return total collisions
	
	void updateNumDocs(const string key);
	void setStart(const string key, const long start);

	void   insertTerm(const string key);// insert term into hash table and update data
	bool   searchTerm(const string key);// check if a term is in the hash table
    string searchTerm(const int index);// return term given index
    int    searchNumDocs(const string key);// return # docs containing term
	long   searchStart(const string key);// return start field for a term
    int    searchTermFreq(const string key);// return term frequency/count
    void   deleteTerm(const string key);// delete term from hash table
	
    void printDict();// print dict content
	void writeDict(const string filePath);// print ALL records of hash table to a lexicon file
	void reset();// reset all contents of hash table

private:
    unsigned long Size;// size of hash table
    unsigned long corpusSize;// number of unique terms in hash table
    unsigned long totalInserts;// total times values have been inserted into hash table
    unsigned long collisions;// keeps track of collisions
    
    string *Term;// terms/tokens (for global AND local ht)
    int    *NumDocs;// number of documents that contain term i (for global ht)
	long   *Start;// store start position for term in post (for global ht)
    int    *TermFreq;// term frequency for term i in some document (for local ht)
    
	unsigned long find(const string key);// search for index of term	
    unsigned long hash(string key);// hash procedure to return index in Key and Count
    unsigned long linearProbe(unsigned long index);// linear probe
    unsigned long secondaryHash(unsigned long index);// secondary hash
};

