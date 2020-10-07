//********************************
// Hash Table Class for storing string keys and counts for corresponding key
// Author: Manuel Serna-Aguilera
//********************************
#include "hashTable.h"
using namespace std;

//================================
// Constructor
//  Input: size of hash table (NOTE: should be a large prime number).
//================================
HashTable::HashTable(unsigned long size)
{
    // Set up: attributes
    Size = size;
	corpusSize = 0;
	totalInserts = 0;
    collisions = 0;

	// Set up: arrays
	Term = new string[Size];
	NumDocs = new int[Size];
	Start = new long[Size];
	TermFreq = new int[Size];

    // Initialize contents
    for(unsigned long i = 0; i < Size; i++)
    {
		Term[i] = EMPTY;
		NumDocs[i] = NONE;
		Start[i] = NONE;
		TermFreq[i] = NONE;
    }
}

//================================
// Destructor: de-allocate memory
//================================
HashTable::~HashTable()
{
	delete []Term;
	delete []NumDocs;
	delete []Start;
	delete []TermFreq;
	
	Term = NULL;
	NumDocs = NULL;
	Start = NULL;
	TermFreq = NULL;
    Size = 0;
}


//================================
// Getters
//  Access: public
//================================
unsigned long HashTable::getHTSize()
{
	return Size;
}

unsigned long HashTable::getCorpusSize()
{
    return corpusSize;
}

unsigned long HashTable::getTotalInserts()
{
    return totalInserts;
}

unsigned long HashTable::getCollisions()
{
    return collisions;
}

//================================
// Increment NumDocs[index] for term in hash table
/*
	NOTE: If inserting a new term, NumDocs is automatically initialized to 1
	Access: public
	Input:  
		key: term to update NumDocs for
	Return: NA
*/
//================================
void HashTable::updateNumDocs(const string key)
{
	unsigned long index = hash(key);
	if (Term[index] == key)
	{
		NumDocs[index]++;
	}
}

//================================
// Set start field for a term
/*
	Access: public
	Input:
		key: term
		start: start position of term in postings
	Return: NA
*/
//================================
void HashTable::setStart(const string key, const long start)
{
	unsigned long index = find(key);
	if (Term[index] == key)
	{
		Start[index] = start;
	}
}

//================================
/*
   Insert term into hash table and update:
	- corpus size (if inserting new term)
	- NumDocs[i] (if inserting new term)
	- TermFreq[i] (if inserting new term, init to 1, otherwise, increment by 1)

	Access: public
	Input:
		key: term
	Return: NA
*/
//================================
void HashTable::insertTerm(const string key)
{
    if (corpusSize >= Size)
    {
        cout << "Hash table full!" << endl;
        return;
    }
    else
    {
		unsigned long index = find(key);

        // Update hash table
        if (Term[index] == EMPTY)
        {
			corpusSize++;// added new term to vocab
			NumDocs[index] = 1;// init number of docs term appears in
			TermFreq[index] = 1;// init count for new term
        }
		else
		{
			// NOTE: increment NumDocs[index] in method updateNumDocs
			TermFreq[index]++;
		}

        totalInserts++;
		Term[index] = key;
    }
}

//================================
// Check if term is in a hash table
/*
	Input:
		key: term to search the existence of
	Return: true of false: answer to "is term in hash table?"
*/
//================================
bool HashTable::searchTerm(const string key)
{
	unsigned long index = find(key);
	if (Term[index] != key)
	{
		return false;// key was not in hash table
	}
	else
	{
		return true;
	}
}

//================================
// Search for term based on index
/*
	Input: index for some (possibly non-EMPTY term)
	Return: contents of Term[index]
*/
//================================
string HashTable::searchTerm(const int index)
{
	return Term[index];
}

//================================
// Search for number of documents a term appears in
/*
	Access: public
	Input: 
		key: term
	Return:
		NumDocs for term (if term and given key match)
*/
//================================
int HashTable::searchNumDocs(const string key)
{
	unsigned long index = find(key);

	if (Term[index] == key)
	{
		return NumDocs[index];
	}
	else
	{
		return -1;
	}
}

//================================
// Search for starting location of term in postings
/*
	Access: public
	Input:
		key: term
	Return:
		starting location of given key in postings (if term matches key)
*/
//================================
long HashTable::searchStart(const string key)
{
	unsigned long index = find(key);
	
	if (Term[index] == key)
	{
		return Start[index];
	}
	else
	{
		return -1;
	}
}

// TODO: implement searchTermFreq
//================================
// Search for frequency of term
/*
	Access: public
	Input:
		key: term
	Return: frequency of key (if term matches given key)
*/
//================================
int HashTable::searchTermFreq(const string key)
{
	unsigned long index = find(key);
	if (Term[index] == key)
	{
		return TermFreq[index];
	}
	else
	{
		return -1;
	}
}

//================================
// Delete value
//  Access: public
//  Input:  key as a string
//	Return: NA
//================================
void HashTable::deleteTerm(const string key)
{
	unsigned long index = find(key);

	if (Term[index] == key)
	{
		// Key match
		corpusSize--;
		Term[index] = DELETED;
		NumDocs[index] = NONE;
		Start[index] = NONE;
		TermFreq[index] = NONE;
	}
	else
	{
		return;// key not found (not matching record or empty/deleted
	}
}


//================================
// Print contents of hash table that would appear in lexicon (dict) file
//  Access: public
//  Input:  NA
//  Return: NA
//================================
void HashTable::printDict()
{	
	cout << "term\tNumDocs[term]\tstart\n";
	for (unsigned long i = 0; i < Size; i++)
	{
		cout << Term[i] << " " << NumDocs[i] << " " << Start[i] << endl;
		//cout << Term[i] << " " << NumDocs[i] << " " << Start[i] << " freq=" << TermFreq[i] << endl;
	}
}


//================================
// Write dict contents of hash table to file of given name
//  Access: public
//  Input: complete file name in path
//  Return: NA
//================================
void HashTable::writeDict(const string filePath)
{
	ofstream file;
	file.open(filePath);

	for (unsigned long i=0; i < Size; i++)
	{
		file << Term[i] << " " << NumDocs[i] << " " << Start[i] << endl;
	}

	file.close();
}


//================================
// Reset all contents of hash table
//  Access: public
//  Input:  NA
//  Return: NA
//================================
void HashTable::reset()
{
	corpusSize = 0;
	totalInserts = 0;
	collisions = 0;

	for(unsigned long i = 0; i < Size; i++)
	{
	    Term[i] = EMPTY;
    	NumDocs[i] = NONE;
	    Start[i] = NONE;
    	TermFreq[i] = NONE;
	}
}



//================================
// Find index of given key
/*
NOTE: I don't anticipate this hash table filling up past capacity, so error checking is just infinitely looping (since we only exit the while loop when we find an empty spot). This can turn into a problem, however.

	Access: private
	Input: key: term
	Return: index for next available spot for term (key)
*/
//================================
unsigned long HashTable::find(const string key)
{
	unsigned long index = hash(key);

    // If keys do not match, perform linear probing
    while ((Term[index] != key) && (Term[index] != EMPTY))
    {
        index = linearProbe(index);
		//index = secondaryHash(index);
    }
	
	return index;
}

//================================
// Primary hash insert
//  Access: private
//  Input:  key as a string
//  Return: index computed for key (as unsigned long due to length of hash table)
//================================
unsigned long HashTable::hash(const string key)
{
    /*
    // Simple method collisions: ~111,000
    for (unsigned long i = 0; i < key.length(); i++)
    {
        index = (16 * index) + key[i];
    }
    */

    // To get index, perform arithmetic on char values depending on length
	// collisions: 22,000
    unsigned long dest = 0;// destination index
    int keyLength = key.length();

    switch(keyLength)
    {
        // One-letter word
        case 1:
            dest += ((key[0] * 2) + dest) % Size;
            break;
        // Two-letter word
        case 2:
            for(int i = 0; i < keyLength; i++)
            {
                switch(i)
                {
                    case 0: dest += ((dest + 1) * key[1]) % Size;
                        break;
                    case 1: dest += (((key[0] * key[1] * dest) + (key[1] + key[0])) * key[1]) % Size;
                        break;
                    default: dest += ((key[0] * 2) + dest) % Size;
                        break;
                }
            }
            break;
        // Three-letter words
        case 3:
            for(int i = 0; i < keyLength; i++)
            {
                switch(i)
                {
                    case 0: dest += (dest + (key[2] % Size) * ((key[0]/2) % Size)) % Size;// B
                        break;
                    case 1: dest += ((key[0] + dest + key[2]) + (key[0] % 3)) % Size;// A
                        break;
                    case 2: dest += (((key[1] * key[0]) + (key[2] + dest)) * key[1]) % Size;// D
                        break;
                    default: dest += ((key[1] * 2) + dest) % Size;
                        break;
                }
            }
            break;
        // Four-letter word
        case 4:
            for(int i = 0; i < keyLength; i++)
            {
                switch(i)
                {
                    case 0: dest += (((key[0] * key[3] * dest) + (key[1] + key[0])) * key[2]) % Size;// F
                        break;
                    case 1: dest += (dest + key[0] + ((key[3] * key[1]))) % Size;// E
                        break;
                    case 2: dest += (dest + key[0] + ((key[1] * key[2]))) % Size;// E
                        break;
                    case 3: dest += ((dest + 1) * key[2]) % Size;// C
                        break;
                    default: dest += ((dest + 2) * key[2]) % Size;// C
                        break;
                }
            }
            break;
        // Five-letter word
        case 5:
            for(int i = 0; i < keyLength; i++)
            {
                switch(i)
                {
                    case 0: dest += ((key[0] + dest + key[3]) + (key[0] % 3)) % Size;// A
                        break;
                    case 1: dest += (dest + (key[3] % Size) * ((key[0]/2) % Size)) % Size;// B
                        break;
                    case 2: dest += ((dest + 1) * key[2]) % Size;// C
                        break;
                    case 3: dest += (((key[1] * key[3]) + (key[2] + dest)) * key[4]) % Size;// D
                        break;
                    case 4: dest += (dest + key[4] + ((key[3] * key[4]))) % Size;// E
                        break;
                    default: dest += (((key[4] * key[4] * dest) + (key[1] + key[0])) * key[2]) % Size;// F
                        break;
                }
            }
            break;
        // Larger words
        default:
            for(int i = 0; i < keyLength; i++)
            {
                switch(i)
                {
                    case 0: dest += (dest + (key[3] % Size) * ((key[0]/2) % Size)) % Size;// B
                        break;
                    case 1: dest += ((key[0] + dest + key[3]) + (key[0] % 3)) % Size;// A
                        break;
                    case 2: dest += (dest + key[4] + ((key[3] * key[2]))) % Size;// E
                        break;
                    case 3: dest += (((key[1] * key[3]) + (key[2] + dest)) * key[4]) % Size;// D
                        break;
                    case 4: dest += ((dest + 1) * key[2]) % Size;// C
                        break;
                    default: dest += (((key[0] * key[i] * dest) + (key[1] + key[i])) * key[2]) % Size;// F
                        break;
                }
            }
            break;
    }

    if (dest < 0)
    {
        dest *= -1;
    }

    dest %= Size;

    return dest;
}

//================================
// Linear Probing insert
//  Access: private
//  Input:  index that caused collision
//	Return: index value incremented by one
//================================
unsigned long HashTable::linearProbe(unsigned long index)
{
	return (index+1) % Size;
}

//================================
// Secondary hash insert
//  Access: private
//  Input:  index that caused collision
//	Return: new index incremented by some step
//================================
unsigned long HashTable::secondaryHash(unsigned long index)
{
    return (index + 7) % Size;
}

