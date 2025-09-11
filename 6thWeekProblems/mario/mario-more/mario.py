def makePY(Height):
    for i in range(1,user_in+1):
        right = left = "#"*i
        space = " "*(user_in-i)
        print(space +left+" " +right)


while True:
    try:
        user_in = int(input("Height: "))
        if 0 < user_in < 9:
            makePY(user_in)
            break
    except ValueError:
        pass