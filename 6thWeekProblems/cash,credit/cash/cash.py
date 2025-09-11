change = float(input("Change: "))

# then check the input accross 1 5 10 25

quater_change = (change//0.25)
print(quater_change)

no_of_dime = change -quater_change
dime_change = ((no_of_dime)//0.10)
print(dime_change)


no_of_nickel= no_of_dime - dime_change
nickel_change = ((no_of_nickel)//0.05)
print(nickel_change)


no_of_pennie = no_of_nickel- nickel_change
pennie_change = int(no_of_pennie/0.01)
print(no_of_pennie)


print(quater_change+dime_change+nickel_change+no_of_pennie)
