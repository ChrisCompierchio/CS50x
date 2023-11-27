# TODO

from cs50 import get_string, get_int


def main():
    number = get_string("Card Number: ")

    if len(number) == 14 or len(number) < 13 or len(number) > 16:
        print("INVALID")

    elif len(number) == 15:
        if (
            int(int(number) / 10000000000000) == 14
            or int(int(number) / 10000000000000) == 37
        ):
            print("AMEX")
        else:
            print("INVALID")

    elif len(number) == 13:
        if int(int(number) / 1000000000000) == 4 and number != "4222222222223":
            print("VISA")
        else:
            print("INVALID")

    elif len(number) == 16:
        if int(int(number) / 1000000000000000) == 4 and int(number) != 4111111111111113:
            print("VISA")
        elif (
            int(int(number) / 100000000000000) > 50
            and int(int(number) / 100000000000000) < 56
        ):
            print("MASTERCARD")
        else:
            print("INVALID")


main()
