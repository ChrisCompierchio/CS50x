import csv
import sys
import cs50


def main():
    # TODO: Check for command-line usage

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py, data.csv, sequence.txt")

    # TODO: Read database file into a variable

    dbase = open(sys.argv[1], "r")

    # TODO: Read DNA sequence file into a variable

    seq = []
    for row in csv.reader(open(sys.argv[2], "r")):
        seq.append(row)

    # TODO: Find longest match of each STR in DNA sequence
    data = []
    cols = 0
    rows = 0
    count = 0

    for row in csv.reader(dbase, delimiter=","):
        data.append(row)
        rows += 1

    for col in data[0]:
        cols += 1

    for i in range(1, rows):
        count = 0
        for j in range(1, cols):
            if int(data[i][j]) == longest_match(seq[0][0], data[0][j]):
                count += 1
                if count == cols - 1:
                    print(data[i][0])
                    sys.exit()
    print("No match")

    # TODO: Check database for matching profiles

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
