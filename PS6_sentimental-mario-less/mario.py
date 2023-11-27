# TODO
def main():
    # get height
    while True:
        height = input("Height: ")

        if len(height) == 1:
            if int(height) < 9 and int(height) > 0:
                height = int(height)
                break

    spaces = height - 1

    # print hashes
    for i in range(height):
        for i in range(spaces, 0, -1):
            print(" ", end="")
        for j in range(height - spaces):
            print("#", end="")
        print("")
        spaces -= 1


# call main
main()
