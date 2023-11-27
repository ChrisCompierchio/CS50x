#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card_number;
    int counter = 1;
    double d;

    do
    {
        card_number = get_long("Number: ");
        d = card_number;

        do
        {
            if (d / 10 < 1)
            {
                break;
            }

            d = d / 10;
            counter++;
        }
        while (d > 1);

        if (counter < 13 || counter > 16 || counter == 14)
        {
            printf("INVALID\n");
            break;
        }
    }
    while (counter < 13 || counter > 16 || counter == 14);

    if (counter == 15)
    {
        if ((int) (card_number / 10000000000000) == 34 || (int) (card_number / 10000000000000) == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (counter == 13)
    {
        if ((int) (card_number / 1000000000000) == 4 && card_number != 4222222222223)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (counter == 16)
    {
        if ((int) (card_number / 1000000000000000) == 4 && card_number != 4111111111111113)
        {
            printf("VISA\n");
        }
        else if ((int) (card_number / 100000000000000) > 50 && (int) (card_number / 100000000000000) < 56)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
}
