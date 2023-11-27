#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double average = (image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0;

            image[i][j].rgbtBlue = round(average);
            image[i][j].rgbtGreen = round(average);
            image[i][j].rgbtRed = round(average);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            if (round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue > 255))
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            }
            if (round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue > 255))
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            }
            if (round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue > 255))
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < round(width / 2); j++)
        {
            int distance = width - 1 - j;

            RGBTRIPLE hold = image[i][distance];

            image[i][distance] = image[i][j];
            image[i][j] = hold;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copyImage[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copyImage[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double avRed = 0;
            double avGreen = 0;
            double avBlue = 0;

            double count = 0.0;

            for (int k = i - 1; k < i + 2; k++)
            {
                for (int l = j - 1; l < j + 2; l++)
                {
                    if (k > -1 && l < width && l > -1 && k < height)
                    {
                        avRed += image[k][l].rgbtRed;
                        avGreen += image[k][l].rgbtGreen;
                        avBlue += image[k][l].rgbtBlue;

                        count++;
                    }
                }
            }

            copyImage[i][j].rgbtRed = round(avRed / count);
            copyImage[i][j].rgbtGreen = round(avGreen / count);
            copyImage[i][j].rgbtBlue = round(avBlue / count);

            if (copyImage[i][j].rgbtRed > 255)
            {
                copyImage[i][j].rgbtRed = 255;
            }
            else if (copyImage[i][j].rgbtGreen > 255)
            {
                copyImage[i][j].rgbtGreen = 255;
            }
            else if (copyImage[i][j].rgbtBlue > 255)
            {
                copyImage[i][j].rgbtBlue = 255;
            }
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copyImage[i][j];
        }
    }

    return;
}
