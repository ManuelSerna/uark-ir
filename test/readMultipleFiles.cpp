// Use file pointers to keep reading file lines

#include <fstream>
#include <iostream>
#include <string>

using namespace std;

int main()
{
	// Open one file
	/*
	ifstream inFile;
	inFile.open("2.txt");
	
	string line;
	getline(inFile, line);
	cout << line << endl;
	
	inFile.close();// */


	// Maintain multiple ifstream objects
	const int SIZE = 4;
	ifstream files[SIZE];// array of file ptrs
	string buffer[SIZE];// array of lines from files
	
	// I. Load first lines of each file (if they exist) into buffer
	for (int i=1; i<=SIZE; i++)
	{
		// Init offset index for arrays (i is for file names only)
		int j = i-1;

		// open files
		string fileName = to_string(i) + ".txt";// shift by one index to use first element
		files[j].open(fileName);

		// load first line into buffer
		if (!files[j].fail())
		{
			string line = "";
			getline(files[j], line);
			buffer[j] = line;
			cout << "reading file" << i << endl;
		}
		else
		{
			cout << "could NOT read file " << i << endl;
		}
	}
	cout << "reading from buffer\n";

	// II. Display read lines
	for (int i=1; i<=SIZE; i++)
	{
		int j = i-1;// offset index for arrays
		
		// read files
		//string fileName = to_string(i) + ".txt";
		if (!files[j].fail())
		{
			cout << "file " << i << ":" << buffer[j] << endl;
		}
		else
		{
			cout << "file " << i << " reached eof\n";
		}
	}

	// read the next line from file 2
	string line = "";
	int fnum = 3;
	getline(files[fnum], line);
	buffer[fnum] = line;
	
	// only getline if eof not found
	if (buffer[fnum].size() == 0)
		cout << "NOTHING TO READ\n";	
	cout << "\nnext from 4.txt: " << buffer[fnum] << endl;

	// Close all files
	for (int j=0; j<SIZE; j++)
	{
		files[j].close();
	}
	
	cout << "done\n";
	return 0;
}
