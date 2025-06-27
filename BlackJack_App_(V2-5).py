#Black Jack app
import random
import time
import copy
import colorama
from colorama import Fore, Back, Style

################################################################  
# THIS BOX CONTAINS PROGRAM TOOLS, NOT ANYTHING FOR THE GAME ITSELF
################################################################
#This clears the screen quickly
def clearScreen():
    for i in range(20):
        print("\n\n\n")
    
#This creates a repeating ♥♦♠♣ line
def fancyLine(cards2):
    tempLine = ''
    for i in range(15):
        for j in range(4):
            tempLine += (cards2[j])
    return tempLine

##############################################################

#This compiles the cards (so i dont need to manually write all the cards)
def cardCompiler(cards1, cards2):
    new_list = []
    for i in range(len(cards2)):
        for j in range(len(cards1)):
            new_list.append(cards1[j] + cards2[i])
    return new_list

cards1 = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'J', 'K']
cards2 = ['♥', '♦', '♠', '♣']
allCards = []
#These are the default cards, compiled in order
allCards = cardCompiler(cards1, cards2)
#Here is all the cards deep copied
gameCards = copy.deepcopy(allCards)
#Then shuffeled properly, just a cool "random" feature
#The randomizer also gets a random seed in order for it to be truly random
random.seed()
random.shuffle(gameCards)


#Display for the screen, probably one of the most important methods
def showCards(urCards, DlrCards):
    clearScreen()
    print("\t\tDealer cards: \n")
    print("\t\t   ", end = '')
    tempDlrCards = copy.deepcopy(DlrCards)
    if len(tempDlrCards) == 2:
        tempDlrCards[1] = "🂠"
    if len(tempDlrCards) == 3 and "XX" in tempDlrCards:
        tempDlrCards.remove("XX")
    for i in range(len(tempDlrCards)):
        print(tempDlrCards[i], end = ' ')
    

    if tempDlrCards[1] != "🂠":
        print("\n\n\t\tDealer = " + str(cardScore(DlrCards)))
    else:
        print("\n\n\t\tDealer = ?")
    
    print("\n\n\n")
    print("\t\tYour Cards: \n")
    print("\t\t   ", end = '')
    for i in range(len(urCards)):
        print(urCards[i], end = ' ')
    print("\n\n\t\tYour score = " + str(cardScore(urCards)))


#This sequence hits the card for you
def hittingYou(urCards, DlrCards):
    choice = input("\n\t\tHit? (y/n)\n\n\t\t     ")
    if (choice == 'Y' or choice == 'y') and cardScore(urCards) < 21:
        while cardScore(urCards) < 21 and (choice == 'Y' or choice == 'y'):
            clearScreen()
            print("\n\t   You chose to hit on a " + str(cardScore(urCards)) + "\n")
            dealUrCards(urCards)
            time.sleep(1)
            showCards(urCards, DlrCards)
            if cardScore(urCards) < 21:
                choice = input("\n\n\t\tHit? (y/n)\n\t\t\t")
            elif cardScore(urCards) > 21:
                time.sleep(2)
                bust_lose()
            elif cardScore(urCards) == 21:
                time.sleep(2)
                instaWin()
            else:
                continue
    elif choice == 'N' or choice == 'n':
        clearScreen()
        print("\n\t   You chose to stand on a " + str(cardScore(urCards)) + "\n")
        time.sleep(1)
        showCards(urCards, DlrCards)
        time.sleep(2)
        hittingDlr(DlrCards)
    else:
        clearScreen()
        print("\n\t  Please enter a valid response...\n")
        time.sleep(1)
        showCards(urCards, DlrCards)
        hittingYou(urCards, DlrCards)


#This sequence hits the card for the dealer
def hittingDlr(DlrCards):
    #This code "XX" is specifically made for the...
    #...showCards method to show the dealer's 2nd card first
    if len(DlrCards) == 2:
        DlrCards.append("XX")
    showCards(urCards, DlrCards)
    if len(DlrCards) > 2:
        DlrCards.remove("XX")
    time.sleep(1)
    while cardScore(DlrCards) < 17:
        dealDlrCards(DlrCards)
        showCards(urCards, DlrCards)
        time.sleep(2)


#These two methods deal one card each time they are called
def dealUrCards(urCards):
    randomElement = random.choice(gameCards)
    urCards.append(randomElement)
    gameCards.remove(randomElement)
    return urCards

def dealDlrCards(DlrCards):
    randomElement = random.choice(gameCards)
    DlrCards.append(randomElement)
    gameCards.remove(randomElement)
    return DlrCards


#This method literally just sorts the hand from lowest to highest score
def handSorter(cards):
    i = 0
    j = 0
    while i < len(cards) and j != len(cards):
        cardScore = cards[i][:len(cards[i])-1]
        if (i+1) < len(cards):
            cardScoreAbove = cards[i+1][:-1]
        if cardScore.isdigit() and i > 0 and (cardScoreAbove.isdigit() and int(cardScore) < int(cardScoreAbove)):
            x = cards[i]
            cards.remove(x)
            cards.insert(i+1, x)
            i -= 1
        elif (cardScore == "J" or cardScore == 'Q' or cardScore == 'K') and cardScoreAbove != "A":
            x = cards[i]
            cards.remove(x)
            cards.insert(len(cards), x)
            i -= 1
        elif cardScore == "A":
            x = cards[i]
            cards.remove(x)
            cards.insert(len(cards), x)
            i -= 1
        i += 1
        j += 1
    
def AddRemoveXX(DlrCards):
    if "XX" in DlrCards and len(DlrCards) == 3:
        DlrCards.remove("XX")
    elif "XX" not in DlrCards and len(DlrCards) == 2:
        DlrCards.append("XX")


#This method returns the int score from the given cards
#Additional edits were made for the Ace cars ability to be 1 and 11
def cardScore(cards):
    handSorter(cards)
    tempList = copy.deepcopy(cards)
    score = 0
    for i in range(len(tempList)):
        cardScore = tempList[i][:len(tempList[i])-1]
        if cardScore.isdigit():
            score += int(cardScore)
        elif cardScore == 'K' or cardScore == 'Q' or cardScore == 'J':
            score += 10
        elif score < 11 and cardScore == 'A':
            score += 11
        elif cardScore == "X":
            score += 0
        else:
            score += 1
    return score



#Instant win message
def instaWin():
    clearScreen()
    print(fancyLine(cards2))
    print("\n\t\tYOU INSTANTLY WIN WITH BLACKJACK!!\n")
    time.sleep(2)
    print("\t\tHere were the cards...")
    time.sleep(2)
    showCards(urCards, DlrCards)
    print("\n" + fancyLine(cards2))
    quit()

#Bust message
def bust_lose():
    clearScreen()
    print(fancyLine(cards2))
    print("\n\t\tBUST! You lost buddy...\n")
    time.sleep(2)
    print("\t\tHere were the cards...")
    time.sleep(2)
    showCards(urCards, DlrCards)
    print("\n" + fancyLine(cards2))
    quit()

#Game Tied Message
def tieGame():
    clearScreen()
    print(fancyLine(cards2))
    print("\n\t\tTIED?!? Holy Moly...\n")
    time.sleep(2)
    print("\t\tHere were the cards...")
    time.sleep(2)
    showCards(urCards, DlrCards)
    print("\n" + fancyLine(cards2))
    quit()

#Game Lost by score Message
def loseGame():
    clearScreen()
    print(fancyLine(cards2))
    print("\n\t\tYou Lose by Score :((\n")
    time.sleep(2)
    print("\t\tHere were the cards...")
    time.sleep(2)
    showCards(urCards, DlrCards)
    print("\n" + fancyLine(cards2))
    quit()

#Game Won by score message
def winGame():
    clearScreen()
    print(fancyLine(cards2))
    print("\n\t\tYou Win by Score :D\n")
    time.sleep(2)
    print("\t\tHere were the cards...")
    time.sleep(2)
    showCards(urCards, DlrCards)
    print("\n" + fancyLine(cards2))
    quit()

#Game Won because Dealer Struck out
def winGame2():
    clearScreen()
    print(fancyLine(cards2))
    print("\n\t\tYou Win, Dealer Bust :D\n")
    time.sleep(2)
    print("\t\tHere were the cards...")
    time.sleep(2)
    showCards(urCards, DlrCards)
    print("\n" + fancyLine(cards2))
    quit()



#The main method that starts the game, and shows the flow
def Start(reply):
    print("\n\n\t   Welcome to BlackJack! ᵇʸ ˢᵉˡᵐᵃⁿ")
    time.sleep(2)
    print("\n\t   I am 6.5 hours into making this...")
    time.sleep(0.5)
    
    #Burn one card like in the game
    gameCards.pop()
    
    #Deal one of your cards
    dealUrCards(urCards)
    #Deal one of the dealer cards
    dealDlrCards(DlrCards)
    #Deal your second card
    dealUrCards(urCards)
    #Deal dealer's second cards
    dealDlrCards(DlrCards)
    #Show cards
    showCards(urCards, DlrCards)
    
    #If you instantly get 21, the game stops asking for input and says you won.
    if cardScore(urCards) == 21:
        time.sleep(1)
        instaWin()
    #If you got less than 21, the game asks if you would like to hit or stand.
    elif cardScore(urCards) < 21:
        hittingYou(urCards, DlrCards)
    #If you got more than 21, the game stops asking for input and says you lost.
    elif cardScore(urCards) > 21:
        time.sleep(1)
        bust_lose()
    
    #BlackJack win, Tie, Lose by Points, and Win by Points
    #This is after the initial cards are given and you've hit
    if cardScore(urCards) == 21:
        time.sleep(1)
        instaWin()
    elif cardScore(DlrCards) == cardScore(urCards):
        time.sleep(1)
        AddRemoveXX(DlrCards)
        tieGame()
    elif cardScore(DlrCards) > cardScore(urCards) and cardScore(DlrCards) <= 21:
        time.sleep(1)
        AddRemoveXX(DlrCards)
        loseGame()
    elif cardScore(urCards) > cardScore(DlrCards)  and cardScore(urCards) <= 21:
        time.sleep(1)
        AddRemoveXX(DlrCards)
        winGame()
    elif cardScore(DlrCards) > 21:
        time.sleep(1)
        AddRemoveXX(DlrCards)
        winGame2()

    
    

urCards = []
DlrCards = []

print(fancyLine(cards2))
Start(input("\n\t\t Are you ready to play??\n\n\t\t   (Enter any key)\n\t\t\t  "))