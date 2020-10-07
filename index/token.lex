/********************************/
/* Tokenizer Flex File */
/* Here I defined several tokenization rules in used to process HTNL documents. */
/* Note: Comments in token rules section detail what each rule does. */
/* Author: Manuel Serna-Aguilera */
/********************************/


/* Section of code to be passed directly yo C++ compiler */
%{
#include <iostream>
using namespace std;

char Ch;
%}


/* Specify lex substitution patterns */
UPPERCASE [A-Z]
LOWERCASE [a-z]
DIGITS [0-9]
EXTRACHAR [,:;!?"'`~@#$%&_+\-=\^\*\(\)\{\}\[\]\\\/|\<\>]


/* Specify regular expressions and actions */
%%
[\n\t ]+        		cout << ' ';/* replace all sequences of whitespace with a space */
\<([^\<\>])*\>  		cout << ' ';/* replace ALL HTML tags, even meta data, with single space */
{UPPERCASE}     		{ Ch = yytext[0]-'A'+'a'; cout << Ch; } /* downcase every uppercase letter */
{EXTRACHAR}     		;/* consume extra characters */
{DIGITS}*\.{DIGITS}*    ;/* consume dots, this also consumes floating-point numbers */
\ [,\-]{DIGITS}         cout << yytext[0] << yytext[2];/* consume hyphen or comma in front of a digit preceeded by a space*/
{DIGITS}[,\-]{DIGITS}   cout << yytext[0] << yytext[2];/* consume hyphen or comma in between digits */
{DIGITS}[,\-]\          cout << yytext[0] << yytext[2];/* consume trailing commas or hyphens followed by a space */
{LOWERCASE}[ ,\-]+      cout << yytext[0] << ' ';/* remove comma or hyphen(s) punctuation after a letter, output a single space in its place */
[^a-z0-9 ]				;/* remove anything not lowercase, a number, or space after applying all rules */
.   					cout << yytext;/* do nothing */
%%


/* Section of code to be passed directly to C++ compiler*/
int main(int argc, char **argv)
{
    if((yyin = fopen(argv[1],"r"))==NULL)
    {
        cout << "\n Error opening input file \n";
    }

    yylex();
}

