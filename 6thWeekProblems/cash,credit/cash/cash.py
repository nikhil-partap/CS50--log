def greed (Amount):
    # print(change)
    quater_change = (cents//25)
    dime_left = cents%25
    # print(quater_change)

    # no_of_dime = change -quater_change
    dime_change = (dime_left//10)
    nickel_left = dime_left%10
    # print(dime_change)
    # print(nickel_left)


    # no_of_nickel= no_of_dime - dime_change
    nickel_change = (nickel_left//5)
    pennie_left = nickel_left%5
    # print(nickel_change)


    # no_of_pennie = no_of_nickel- nickel_change
    pennie_change = int(pennie_left)
    # print(pennie_change)

    total_coins = quater_change+dime_change+nickel_change+pennie_left

    print(total_coins)

while True:
    try:
        change = float(input("Change: "))
        cents = int(change*100)

        
        if cents >= 0:
            greed(cents)
            break
        

    except ValueError :
        pass
