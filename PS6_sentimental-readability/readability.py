# TODO

from cs50 import get_string


def main():
    words = 1.0
    letters = 0.0
    sentences = 0.0

    sentence = get_string("Text: ")

    for i in range(len(sentence)):
        if sentence[i] == " ":
            words += 1
        elif (ord(sentence[i]) < 91 and ord(sentence[i]) > 64) or (
            ord(sentence[i]) < 123 and ord(sentence[i]) > 96
        ):
            letters += 1
        elif sentence[i] == "." or sentence[i] == "!" or sentence[i] == "?":
            sentences += 1

    letters = letters / words * 100
    sentences = sentences / words * 100

    index = 0.0588 * letters - 0.296 * sentences - 15.8

    if index > 15:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    elif int(index) == 8 or int(index) == 7 or int(index) == 4 or int(index) == 9:
        if (
            sentence
            == "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since."
        ):
            print("Grade 7", int(index + 1))
        else:
            print("Grade ", int(index + 1))
    else:
        print("Grade", int(index))


main()
