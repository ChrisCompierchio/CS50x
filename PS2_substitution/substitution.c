#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    //if there are 2 arguments given
    if (argc == 2)
    {
        //check if the user entered a key with 26 characters
        if (strlen(argv[1]) == 26)
        {
            string key = argv[1];

            int count = 0;

            //run through the key to see if any non-letters are included or if there are duplicate letters.
            for (int i = 0; i < strlen(key); i++)
            {
                for (int j = i + 1; j < strlen(key); j++)
                {
                    if (toupper(key[i]) == toupper(key[j]) || toupper(key[j]) < 'A' || toupper(key[j]) > 'Z')
                    {
                        count++;
                        break;
                    }
                }

                if (count > 0)
                {
                    printf("Key must contain 26 distinct, alphabetical characters.\n");
                    return 1;
                    break;
                }
            }

            //if the key has 26 distinct, alphabetical characters
            if (count == 0)
            {
                string plaintext = get_string("plaintext:  ");

                //change the letters to the correct key letter, while maintaining the case
                for (int i = 0; i < strlen(plaintext); i++)
                {
                    for (int j = 65; j < 91; j++)
                    {
                        if (plaintext[i] == j)
                        {
                            plaintext[i] = toupper(key[j - 65]);
                            break;
                        }
                    }

                    for (int k = 97; k < 123; k++)
                    {
                        if (plaintext[i] == k)
                        {
                            plaintext[i] = tolower(key[k - 97]);
                            break;
                        }
                    }
                }

                printf("ciphertext: %s\n", plaintext);
            }
        }
        //print error message if the key is not 26 characters or is blank
        else if (strlen(argv[1]) != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }
    //print error message if the user enters less than or more than 2 arguments
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
}