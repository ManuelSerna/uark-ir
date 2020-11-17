/*********************************
Format Write to File Demo
Credit: http://www.cplusplus.com/reference/cstdio/fprintf/
*********************************/

#include <fstream>
#include <iostream>
#include <stdio.h>
#include <string>

using namespace std;

int main()
{
	// Write to file
	/*
	FILE * file;

	file = fopen("file.txt", "w");// open file to write to
	
	// Several examples
	fprintf(file, "Document %d: %s\n", 1, "some words");
	fprintf(file, "%f is a float\n", 3.14);
	fprintf(file, "input=%d\n\toutput=%d\n\t%c", 1, 2, 'm');
	*/

	// Read from file
	FILE * inFile;
	
	inFile = fopen("1.txt", "r");
	string line;
	
	if (inFile == NULL)// check if file exists
	{
		cout << "1.txt does not exist!\n";
		fclose(inFile);
	}
	else
	{
		while(!feof(inFile))
		{
			// reminder: fgets retrieves a string until a newline \n is found
			//  OR end of file is reached
			//fgets(line, 100, inFile);
		}
		fclose(inFile);
	}

	// array of FILE objects

	cout << "done\n";
	return 0;
}

