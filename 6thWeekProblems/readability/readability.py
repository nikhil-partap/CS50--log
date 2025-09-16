# 0.0588 * L - 0.296 * S - 15.8

user_input = input("Enter your para : ")
def isBlank(s):
    return not (s and s.strip())

L = 0;
S = 0;
W = 0;


for char in user_input:
    if char.isalpha:
        L += 1
    elif isBlank(char):
        W += 1
    elif char == "." or "?" or "!" :    #  . ? !
        S += 1

    
    
    # // printf("letter = %i \nword = %i \nsen = %i", letter, word, sen);
    # if (index < 1.5)
    # {
    #     printf("Before Grade 1\n");
    # }
    # else if (index < 16 && index > 1.5)
    # {
    #     printf("Grade %0.0f\n", round(index));
    # }
    # else
    # {
    #     printf("Grade 16+\n");
    # }


