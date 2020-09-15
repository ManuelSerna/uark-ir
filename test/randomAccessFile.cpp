/******************************//*
Random Access File Demo
Credit: https://www.learncpp.com/cpp-tutorial/187-random-file-io/

Instead of sequentially accessing a file, access specific 'parts' of a file with seekg() and seekp(). This allows us to manipulate the file pointer (instead of it being set to the beginning or end of a file).
 - seekg() is used for file input (get)
 - seekp() is used for file output (put)

The two functions take in two parameters:
 - Offset for determining how many bytes
 - ios flag that specifies what the offset parameter should be offset from

There are also ios seek flags to know about:
 beg	offset relative to beginning of file (default)
 cur	offset relative to current location of file pointer
 end	offset relative to end of file

Reminder: to output contents of a file (including newlines and spaces), type command
	$ od -a textfile

to output characters in ascii. 
*********************************/
#include <iostream>
#include <fstream>
using namespace std;

int main()
{
	// Read file
	ifstream inputFile("./sample.in");

	if (!inputFile)
	{
		cout << "Error, could not read file\n";
		return 1;
	}
	
	// Read and output file contents but at certain points
	string line;
	
	//inputFile.seekg(7);// move to 7th character in the first line
	inputFile.seekg(7);

	// Print remaining characters in read line
	getline(inputFile, line);
	cout << line << endl;

	// Note: it seems the file pointer is at the beginning of the next line
	
	inputFile.seekg(11, ios::cur);// move 11 bytes
	getline(inputFile, line);
	cout << line << endl;

	// Move file pointer 12 bytes before end of file; print line
	// Account for file ending in newlines and such
	inputFile.seekg(-12, ios::end);
	getline(inputFile, line);
	cout << line << endl;
	
	// Close input file
	inputFile.close();

	return 0;
}

