#include <cs50.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

typedef struct
{
    BYTE byte[512];
} data;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: recover infile\n");
        return 1;
    }

    data buffer;

    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    char name[8];

    int BLOCK_SIZE = 512;

    int number = 0;

    FILE *output = NULL;

    while (fread(&buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer.byte[0] == 0xff && buffer.byte[1] == 0xd8 && buffer.byte[2] == 0xff && buffer.byte[3] >= 0xe0 &&
            buffer.byte[3] <= 0xef)
        {
            if (number == 0)
            {
                if (number / 10.0 < 1.0)
                {
                    sprintf(name, "00%i.jpg", number);
                }
                else if (number / 10.0 >= 1.0 && number / 10.0 < 10.0)
                {
                    sprintf(name, "0%i.jpg", number);
                }
                else
                {
                    sprintf(name, "%i.jpg", number);
                }

                output = fopen(name, "w");
                number++;
            }
            else
            {
                fclose(output);

                if (number / 10.0 < 1.0)
                {
                    sprintf(name, "00%i.jpg", number);
                }
                else if (number / 10.0 >= 1.0 && number / 10.0 < 10.0)
                {
                    sprintf(name, "0%i.jpg", number);
                }
                else
                {
                    sprintf(name, "%i.jpg", number);
                }

                output = fopen(name, "w");
                number++;
            }
            fwrite(&buffer, 512, 1, output);
        }
        else
        {
            if (output != NULL)
            {
                fwrite(&buffer, 512, 1, output);
            }
        }
    }
    fclose(file);
    fclose(output);
    return 0;
}