/*********************************
Format Write to File Demo
Credit: http://www.cplusplus.com/reference/cstdio/fprintf/
*********************************/

#include <stdio.h>

int main()
{
	// File setup
	FILE * file;

	file = fopen("file.txt", "w");// open file to write to
	
	// Several examples
	fprintf(file, "Document %d: %s\n", 1, "some words");
	fprintf(file, "%f is a float\n", 3.14);
	fprintf(file, "input=%d\n\toutput=%d\n\t%c", 1, 2, 'm');

	return 0;
}

