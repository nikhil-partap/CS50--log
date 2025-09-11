def makePY(Height):
    for i in range(1, Height+1):
        for j in range(Height - i):
            print(" ", end="")
        for k in range(i):
            print("#", end="")
        print()


while True:
    try:
        user_in = int(input("Height: "))
        if 0 < user_in < 9:
            makePY(user_in)
            break
    except ValueError:
        pass



# user_input = int(input("Height: "))
# for  i  in range(user_input):
#     for l in range(user_input -i):
#         print("#", end="")
#     print()



# def makePY(Height):
#     for i in range(1,Height+1):
#         for j in range(Height -i ):
#             print(" ", end="")
#         for k in range(i):
#             print("#", end="")
#         print()



# while True :
#     try:
#         user_in = int(input("Height: "))
#         if 0<user_in<9:
#             makePY(user_in)
#             break
#     except ValueError:
#         pass
    


# user_in=int(input("Height: "))

# for i in range(1,user_in+1):
#     print(" "*(user_in-i)+"#"*i+" "+"#"*i+" "*(user_in-i-1), end="")
#     print()





    
        
            

        
 

