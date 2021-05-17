import random

def game():
    wordList = ["leadership","stuff","practical","restless","environment","hero","firefighter","precedent","place","basis"]
    ans = wordList[random.randint(0,9)]
    guess = []
    length = len(ans)

    # initialise guess to '-'
    for i in range(length):
        guess.append("-")

    print("The word you gonna guess is", length, "characters long! ")

    #starting chance
    chance = 10

    #represent unguess character 
    failed = length

    #loop when there are chances left
    while chance > 0:
        # as a flag to determine whether the user has guessed correctly
        found = False
        
        #if no unguess character, user won and break the loop
        if failed == 0:
            print("Congratulation! You won!")
            break
        else:
            #print every character in guess
            for i in guess:
                print(i)

            print("You have",chance,"chances left!")

            #Repeat prompting for char until a character is inputted
            while True:
                c = input("Guess a character:")
                if c.isalpha() and len(c) == 1:
                    break

            for e in range(length):
                if ans[e] == c:
                    guess[e] = c
                    failed -= 1
                    found = True

        if found == False:
            chance -= 1

    if chance == 0:
        print("You lose !")
    print("The word is", ans,"!\n")      

def repeat():
    while True:
        c = input("Would you like to play again?(y/n)")
        c = c.lower()

        if c =='y':
            print()
            game()
        else:
            print("Okay...See you next time")
            break

name = input("Your name:")
print("Hello",name,"\nLet's play Hangman!")
game()
repeat()

