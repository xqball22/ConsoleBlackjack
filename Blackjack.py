import array as arr
import pdb
import random

class Card:
    suits = ("Spades"
             "Hearts"
             "Diamonds"
             "Clubs")

    values = (2, 3, 4, 5, 6, 7,
              8, 9, 10, 11, 12, 13, 14)      

    def __init__ (self, value, suit):
        self.value = value
        self.suit = suit

    def getSuit(self):
        if self.suit == 0:
            return "Spades"
        elif self.suit == 1:
            return "Hearts"
        elif self.suit == 2:
            return "Diamonds"
        else:
            return "Clubs"

    def getValue(self): 
        if self.value == 11:
            return "Jack"
        elif self.value == 12:
            return "Queen"
        elif self.value == 13:
            return "King"
        elif self.value == 14:
            return "Ace"
        else:
            return str(self.value)

class Deck:
    def __init__ (self):
        self.cards = []

    def removeCard(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()

    def shuffle(self):
        self.cards.clear()

        for x in range (2,15):
            for y in range(4):
                self.cards.append(Card(x, y))

        random.shuffle(self.cards)

class Player:
    def __init__ (self, chips):
        self.chips = chips
        self.cards = []
        self.score = 0
        self.bustedScore = 0
        self.aceCount = 0 
        self.pocketPair = False 
        self.splitCards = []
        self.splitScore= 0
        self.splitBustedScore = 0
        self.splitAceCount = 0
        self.handOneHasBusted = False
        self.handTwoHasBusted = False
        self.blackjack1 = False
        self.blackjack2 = False
        
    def checkPocketPair(self):
        if self.cards[0].value == self.cards[1].value:
            self.pocketPair = True

    def updateScore(self):
        points = 0

        for x in range(len(self.cards)):
            if self.cards[x].value == 11 or self.cards[x].value == 12 or self.cards[x].value == 13:
                points += 10
            elif self.cards[x].value == 14:
                points += 11
                self.aceCount += 1
            else:
                points += self.cards[x].value

        self.score = points
        self.bustedScore = self.score

        if self.score == 21 and len(self.cards) == 2:
            self.blackjack1 = True
    
    def hasBusted(self):
        aceIndex = []

        if self.score > 21:
            self.bustedScore = self.score

            for x in range(self.aceCount):
                for y in range(len(self.cards)):
                    if self.cards[y].value == 14:
                        if aceIndex.count(y) == 0:
                            self.bustedScore -= 10
                            aceIndex.append(y) 
                            break
                if self.bustedScore <= 21:
                    return False

            if self.bustedScore > 21:
                return True
            else:
                return False
        else:
            self.bustedScore == self.score
            return False

    def splitScoreUpdate(self):
        points = 0

        for x in range(len(self.splitCards)):
            if self.splitCards[x].value == 11 or self.splitCards[x].value == 12 or self.splitCards[x].value == 13:
                points += 10
            elif self.splitCards[x].value == 14:
                points += 11
                self.splitAceCount += 1
            else:
                points += self.splitCards[x].value

        self.splitScore = points
        self.splitBustedScore = points

        if self.splitScore == 21 and len(self.splitCards) == 2:
            self.blackjack2 == True

    def splitHasBusted(self):
        aceIndex = [] 

        if self.splitScore > 21:
            self.splitBustedScore = self.splitScore

            for x in range(self.splitAceCount):
                for y in range(len(self.splitCards)):
                    if self.splitCards[y].value == 14:
                        if aceIndex.count(y) == 0:
                               self.splitBustedScore -= 10
                               aceIndex.append(y)
                               break

                        if self.splitBustedScore <= 21:
                               return False
            if self.splitBustedScore > 21: 
                return True
            else:
                return False
        else:
            self.splitBustedScore = self.splitScore
            return False

class Dealer:
    def __init__ (self):
        self.cards = []
        self.score = 0
        self.bustedScore = 0
        self.aceCount = 0
        self.blackjack = False
    
    def updateScore(self):
        points = 0

        for x in range(len(self.cards)):
            if self.cards[x].value == 11 or self.cards[x].value == 12 or self.cards[x].value == 13:
                points += 10
            elif self.cards[x].value == 14:
                points += 11
                self.aceCount += 1
            else:
                points += self.cards[x].value

        self.score = points
        self.bustedScore = self.score

        if self.score == 21 and len(self.cards) == 2:
            self.blackjack = True

    def hasBusted(self):
        aceIndex = []

        if self.score > 21:
            self.bustedScore = self.score

            for x in range(self.aceCount):
                for y in range(len(self.cards)):
                    if self.cards[y].value == 14:
                        if aceIndex.count(y) == 0:
                            self.bustedScore -= 10
                            aceIndex.append(y) 
                            break 

                if self.bustedScore <= 21:
                    break
                    return False

            if self.bustedScore > 21: 
                return True
            else:
                return False
            
        else:
            self.bustedScore = self.score
            return False
    
class Game:
    def __init__ (self):
        self.deck = Deck()
        self.player = Player(5000)
        self.dealer = Dealer()
        self.pot = 0
        self.bet = 0
        self.splitBet = 0
        self.splitPot = 0
        self.insuranceBet = 0
        self.insurancePot = 0
        
    def placeBet(self):
        while self.bet <= 0 or self.bet > self.player.chips:
            print("\n> You have $" + str(self.player.chips) + ". Place a bet:")
            self.bet = float(input())

            if self.bet <= 0 or self.bet > self.player.chips:
                print("\n> Error! Invalid bet!")

            self.bet = self.betErrorTrap(self.bet)
        
        self.pot = 2 * self.bet
        self.player.chips -= self.bet

        print("\n> You have placed a bet of $" + str(self.bet) + ".")

    def betErrorTrap(self, bet):
        round(bet, 0)
        bet = int(bet)
        return bet

    def shuffleDeck(self):
        print("\n> Shuffling...") 
        self.deck.shuffle()

    def dealIn(self):
        print("\n> Dealing...")
        self.player.cards.append(self.deck.removeCard())
        self.dealer.cards.append(self.deck.removeCard())
        self.player.cards.append(self.deck.removeCard())
        self.dealer.cards.append(self.deck.removeCard())

        self.player.updateScore()
        self.dealer.updateScore()

        self.player.hasBusted()
        self.player.hasBusted()

        self.player.checkPocketPair()

    def dealInPrompt(self):
        print("\t> " + self.player.cards[0].getValue() + " of " + self.player.cards[0].getSuit() + "\n\t> " + self.player.cards[1].getValue() + " of " + self.player.cards[1].getSuit())
        print("\t> Your score: " + str(self.player.score))
        print("\n> Dealer's face-up card:\n\t\t\t\t> " + self.dealer.cards[1].getValue() + " of " + self.dealer.cards[1].getSuit())

    def insuranceBetPossible(self):
        if self.dealer.cards[1].value == 14 and self.player.chips - self.bet / 2 > 0:
            return True
        else:
            return False

    def placeInsuranceBet(self):
        string = str

        print("\n> The dealer's face-up card is an ace. Would you like to make an inusurance bet of $" + str(int(self.bet / 2)) + " that the dealer has a blacjack (y/n)?")
        string = input()

        string = self.errorTrap("y", "y", "n", "n", string)

        if string == "y":
            self.player.chips -= int(self.bet / 2)
            self.insuranceBet = int(self.bet / 2)
            self.insurancePot = self.bet

            if self.dealer.score == 21:
                print("\n> The dealer shows a blackjack!\n\t\t\t\t> " + self.dealer.cards[0].getValue() + " of " + self.dealer.cards[0].getSuit() + "\n\t\t\t\t> " + self.dealer.cards[1].getValue() + " of " + self.dealer.cards[1].getSuit())
                print("\n> You win $" + str(self.insurancePot) + " from your $" + str(self.insuranceBet) + " insurance bet!")

                self.player.chips += self.insurancePot
                
            else:
                print("\n> The dealer does not have a blackjack. You lost your $" + str(self.insuranceBet) + " insurance bet. Proceed:") 
        else:
            print("\n> Proceed:")

    def postDeal(self):
        if self.insuranceBetPossible() == True:
            self.placeInsuranceBet()

        if self.player.blackjack1 == True and self.dealer.blackjack == True:
            print("\n> Dealer shows:\n\t\t\t\t> " + self.dealer.cards[0].getValue() + " of " + self.dealer.cards[0].getSuit() + "\n\t\t\t\t> " + self.dealer.cards[1].getValue() + " of " + self.dealer.cards[1].getSuit())
            self.showdown()
        elif self.player.blackjack1 == True and self.dealer.blackjack == False:
            self.dealerProcess()
        else:
            if self.player.pocketPair == True:
                self.splitPlayerProcess()
            else:
                self.playerProcess()

    def playerProcess(self):
        string = str
        
        while self.player.hasBusted() == False:
            if len(self.player.cards) == 2 and self.canDoubleDown() == True:
                print("\n> Type 'h' to hit, 's' to stand, 'd' to double down:")
                string = input()
                string = self.errorTrap("h", "s", "d", "d", string)

                if string == "h":
                    self.playerHit()
                elif string == "s":
                    print("\n> You stand on " + str(self.player.bustedScore) + ".") 
                    break
                else:
                    self.playerDoubleDown()
                    break
            else:
                print("\n> Type 'h' to hit, 's' to stand:")
                string = input()
                string = self.errorTrap("h", "s", "h", "s", string)

                if string == "h":
                    self.playerHit()
                else:
                    print("\n> You stand on " + str(self.player.bustedScore) + ".")
                    break

        if self.player.hasBusted() == True:
            self.playerBust()
        else:
            self.dealerProcess()           

    def playerHit(self):
        self.player.cards.append(self.deck.removeCard())
        self.player.updateScore()
        self.player.hasBusted()

        print("\n> You have drawn the:\n\t> " + self.player.cards[len(self.player.cards) - 1].getValue() + " of " + self.player.cards[len(self.player.cards) - 1].getSuit())
        print("\t> Your score: " + str(self.player.bustedScore))

    def playerDoubleDown(self):
        print("\n> You have chosen to double your $" + str(self.bet) + " wager for the exchange of one last card...")

        self.player.chips -= self.bet
        self.bet *= 2
        self.pot *= 2

        self.playerHit()

    def playerBust(self):
        print("\n> You bust with a score of " + str(self.player.bustedScore) + "! You lose your $" + str(self.bet) + " wager!")
        self.wash()

    def splitPlayerProcess(self):
        string = str

        while self.player.hasBusted() == False:
            if len(self.player.cards) == 2 and self.canDoubleDown() == True:
                print("\n> Type 'h' to hit, 's' to stand, 'd' to double down, 'sp' to split:")
                string = input()
                string = self.errorTrap("h", "s", "d", "sp", string)

                if string == "h":
                    self.playerHit()
                elif string == "s":
                    print("\n> You stand on " + str(self.player.bustedScore) + ".")
                    break
                elif string == "d":
                    self.playerDoubleDown()
                    break
                else:
                    self.playerSplits()
                    break

                if self.player.hasBusted() == True:
                    self.playerBust()
            else:
                print("\n> Type 'h' to hit, 's' to stand:")
                string = input()
                string = self.errorTrap("h", "s", "d", "sp", string)

                if string == "h":
                    self.playerHit()
                else:
                    print("\n> You stand on " + str(self.player.bustedScore) + ".")
                    break
                


            if self.player.hasBusted() == True:
                self.playerBust()
            elif len(self.cards.splitCards) == 0:
                self.dealerProcess()
            
                    
    def playerSplits(self): 
        string = str
        tempCard = self.player.cards[0]

        print("\n> You double your $" + str(self.bet) + " wager to play two hands...")
        
        self.player.splitCards.append(self.player.cards[1])
        self.player.cards.clear()
        self.player.cards.append(tempCard)
        self.player.cards.append(self.deck.removeCard())
        self.player.splitCards.append(self.deck.removeCard())

        self.player.updateScore()
        self.player.hasBusted()
        self.player.splitScoreUpdate()
        self.player.splitHasBusted()

        self.player.chips -= self.bet
        self.splitBet = self.bet
        self.splitPot = self.bet * 2

        print("\n> You now hold the:\n\t> " + self.player.cards[0].getValue() + " of " + self.player.cards[0].getSuit() + "\n\t> " + self.player.cards[1].getValue() + " of " + self.player.cards[1].getSuit())
        print("\n\t> " + self.player.splitCards[0].getValue() + " of " + self.player.splitCards[0].getSuit() + "\n\t> " + self.player.splitCards[1].getValue() + " of " + self.player.splitCards[1].getSuit())

        print("\n> For your first hand:\n\t> " + self.player.cards[0].getValue() + " of " + self.player.cards[0].getSuit() + "\n\t> " + self.player.cards[1].getValue() + " of " + self.player.cards[1].getSuit())
        print("\n> Your score: " + str(self.player.score))

        while self.player.hasBusted() == False:
            if len(self.player.cards) == 2 and self.canDoubleDown() == True:
                print("\n> Type 'h' to hit, 's' to stand, 'd' to double down:")
                string = input()
                string = self.errorTrap("h", "s", "d", "d", string)

                if string == "h":
                    self.playerHit()
                elif string == "s":
                    print("\n> You stand on " + str(self.player.bustedScore) + ".")
                    break
                else:
                    self.playerDoubleDown()
                    break
            else:
                print("\n> Type 'h' to hit, 's' to stand:")
                string = input()
                string = self.errorTrap("h", "s", "h", "s", string)

                if string == "h":
                    self.playerHit()
                else:
                    print("\n> You stand on " + str(self.player.bustedScore) + ".")
                    break 

        if self.player.hasBusted() == True:
            self.splitPlayerBust(0)

        print("\n> For your second hand:\n\t> " + self.player.splitCards[0].getValue() + " of " + self.player.splitCards[0].getSuit() + "\n\t> " + self.player.splitCards[1].getValue() + " of " + self.player.splitCards[1].getSuit())
        print("\n> Your score: " + str(self.player.splitScore))

        while self.player.splitHasBusted() == False:
            if len(self.player.splitCards) == 2 and self.canDoubleDown() == True:
                print("\n> Type 'h' to hit, 's' to stand, 'd' to double down:")
                string = input()
                string = self.errorTrap("h", "s", "d", "d", string)

                if string == "h":
                      self.splitPlayerHit()
                elif string == "s":
                    print("\n> You stand on " + str(self.player.splitBustedScore) + ".")
                    break
                else:
                    self.splitDoubleDown()
                    break
            else:
                print("\n> Type 'h' to hit, 's' to stand:")
                string = input()
                string = self.errorTrap("h", "s", "h", "s", string)

                if string == "h":
                    self.splitPlayerHit()
                else:
                    print("\n> You stand on " + str(self.player.splitBustedScore) + ".")
                    break

        if self.player.splitHasBusted() == True:
            self.splitPlayerBust(1)

        if self.player.hasBusted() and self.player.splitHasBusted():
            self.splitShowdown()
        else: 
            self.dealerProcess()

    def splitPlayerHit(self):
        self.player.splitCards.append(self.deck.removeCard())
        self.player.splitScoreUpdate()
        self.player.splitHasBusted()

        print("\n> You have drawn the:\n\t> " + self.player.splitCards[len(self.player.splitCards) - 1].getValue() + " of " + self.player.splitCards[len(self.player.splitCards) - 1].getSuit())
        print("\t> Your score: " + str(self.player.splitBustedScore))

    def splitDoubleDown(self):
        print("\n> You have chosen to double your $" + str(self.splitBet) + " wager for the exchange of one last card...")

        self.player.chips -= self.splitBet
        self.splitBet *= 2
        self.splitPot *= 2

        self.splitPlayerHit()

    def splitPlayerBust(self, x):
        if x == 0:
            self.player.handOneHasBusted = True
        else:
            self.player.handTwoHasBusted = True

    def dealerProcess(self):
        print("\n> Dealer shows the:\n\t\t\t\t> " + self.dealer.cards[0].getValue() + " of " + self.dealer.cards[0].getSuit() + "\n\t\t\t\t> " + self.dealer.cards[1].getValue() + " of " + self.dealer.cards[1].getSuit())
        print("\t\t\t\t> Dealer score: " + str(self.dealer.bustedScore))
        
        while self.dealer.hasBusted() == False:
            if self.dealer.bustedScore < 17:
                self.dealerHit()
            else:
                print("\n> Dealer stands on " + str(self.dealer.bustedScore) + ".")
                break

        if self.dealer.hasBusted() == True:
            self.dealerBust()
        else:
            if len(self.player.splitCards) > 0:
                self.splitShowdown()
            else:
                self.showdown()
            
    def dealerHit(self):
        self.dealer.cards.append(self.deck.removeCard())
        self.dealer.updateScore()
        self.dealer.hasBusted()

        print("\n> Dealer has drawn the:\n\t\t\t\t> " + self.dealer.cards[len(self.dealer.cards) - 1].getValue() + " of " + self.dealer.cards[len(self.dealer.cards) - 1].getSuit())
        print("\t\t\t\t> Dealer score: " + str(self.dealer.bustedScore))

    def dealerBust(self):
        if len(self.player.splitCards) > 0:
            if self.player.handOneHasBusted == True and self.player.handTwoHasBusted == False:
                print("\n> Dealer busts with a score of " + str(self.dealer.bustedScore) + "! You win your $" + str(self.bet) + " wager and lose your split $" + str(self.splitBet) + " wager!")
                self.player.chips += self.pot
            elif self.player.handOneHasBusted == False and self.player.handTwoHasBusted == True:
                print("\n> Dealer busts with a score of " + str(self.dealer.bustedScore) + "! You lose your $" + str(self.bet) + " wager and win your split $" + str(self.splitBet) + " wager!")
                self.player.chips += self.splitPot
            else:
                print("\n> Dealer busts with a score of " + str(self.dealer.bustedScore) + "! You win your $" + str(self.bet) + " wager and win your split $" + str(self.splitBet) + " wager!")
                self.player.chips += self.pot
                self.player.chips += self.splitPot              

        else:
            print("\n> Dealer busts with a score of " + str(self.dealer.bustedScore) + "! You win your $" + str(self.bet) + " wager!")
            self.player.chips += self.pot

        self.wash()

    def showdown(self): 
        if self.player.bustedScore > self.dealer.bustedScore:
            if self.player.blackjack1 == True:
                print("\n> Your blackjack beats the dealer's " + str(self.dealer.bustedScore) + "! You win your $" + str(self.bet) + " wager at a rate of 3:2 - so you win $" + str(self.pot * 1.5) + "!")
                self.player.chips += self.bet * 1.5
            else:
                print("\n> Your " + str(self.player.bustedScore) + " beats the dealer's " + str(self.dealer.bustedScore) + "! You win your $" + str(self.bet) + " wager!")   
                self.player.chips += self.pot           
    
        elif self.player.bustedScore < self.dealer.bustedScore:
            if self.dealer.blackjack == True:
                print("\n> Your " + str(self.player.bustedScore) + " is beaten by the dealer's blackjack! You lose your $" + str(self.bet) + " wager!")
            else:
                print("\n> Your " + str(self.player.bustedScore) + " is beaten by the dealer's " + str(self.dealer.bustedScore) + "! You lose your $" + str(self.bet) + " wager!")
        else:
            if self.player.blackjack1 == True and self.dealer.blackjack == True: 
                print("\n> Your blackjack matches the dealer's blackjack! Your $" + str(self.bet) + " wager is pushed!")
                self.player.chips += self.bet
            else:
                print("\n> Your " + str(self.player.bustedScore) + " matches the dealer's " + str(self.dealer.bustedScore) + "! Your $" + str(self.bet) + " wager is pushed!")
                self.player.chips += self.bet

        self.wash()

    def splitShowdown(self):
        print("\n> For your first hand:")

        if self.player.handOneHasBusted == False:
            if self.player.bustedScore > self.dealer.bustedScore:
                print("\n> Your " + str(self.player.bustedScore) + " beats the dealer's " + str(self.dealer.bustedScore) + "! You win your $" + str(self.bet) + " wager!")
                self.player.chips += self.pot
            elif self.player.bustedScore < self.dealer.bustedScore:
                print("\n> Your " + str(self.player.bustedScore) + " is beaten by the dealer's " + str(self.dealer.bustedScore) + "! You lose your $" + str(self.bet) + " wager!")
            else:
                print("\n> Your " + str(self.player.bustedScore) + " matches the dealer's " + str(self.dealer.bustedScore) + "! Your $" + str(self.bet) + " wager is pushed!")
        else:
            print("\n You bust with a score of " + str(self.player.bustedScore) + "! You lose your $" + str(self.bet) + " wager!") 

        print("\n> For your second hand:") 

        if self.player.handTwoHasBusted == False:
            if self.player.splitBustedScore > self.dealer.bustedScore:
                print("\n> Your " + str(self.player.splitBustedScore) + " beats the dealer's " + str(self.dealer.bustedScore) + "! You win your $" + str(self.splitBet) + " wager!")
                self.player.chips += self.splitPot
            elif self.player.splitBustedScore < self.dealer.bustedScore:
                print("\n> Your " + str(self.player.splitBustedScore) + " is beaten by the dealer's " + str(self.dealer.bustedScore) + "! You lose your $" + str(self.splitBet) + " wager!")
            else:
                print("\n> Your " + str(self.player.splitBustedScore) + " matches the dealer's " + str(self.dealer.bustedScore) + "! Your $" + str(self.splitBet) + " wager is pushed!")
        else:
            print("\n> You bust with a score of " + str(self.player.splitBustedScore) + "! You lose your $" + str(self.splitBet) + " wager!")

        self.wash()
            
    def wash(self):
        self.player.cards.clear()
        self.player.score = 0 
        self.player.bustedScore = 0
        self.player.aceCount = 0
        self.player.pocketPair = False
        self.player.splitCards.clear()
        self.player.splitScore = 0
        self.player.splitBustScore = 0
        self.player.splitAceCount = 0
        self.handOneHasBusted = False
        self.handTwoHasBusted = False
        self.player.blackjack1 = False
        self.player.blackjack2 = False

        self.dealer.cards.clear()
        self.dealer.score = 0
        self.dealer.bustedScore = 0
        self.dealer.aceCount = 0
        self.dealer.blackjack = False

        self.pot = 0
        self.bet = 0
        self.splitBet = 0
        self.splitPot = 0
        self.insuranceBet = 0
        self.insurancePot = 0

    def errorTrap(self, a, b, c, d, string):
        if string != a and string != b and string != c and string != d:
            print("\n> Error! Invalid Input!:")
            string = input()
            return self.errorTrap(a, b, c, d, string)
        else:
            return string

    def canDoubleDown(self):
        if self.player.chips - self.bet >= 0:
            return True
        else:
            return False
                                    
def main():
    string = "y"

    while string == "y":
        game = Game()

        print("\n> Good luck!") 
        
        while game.player.chips > 0:  
            game.placeBet()
            game.shuffleDeck()
            game.dealIn()
            game.dealInPrompt()
            game.postDeal()
            game.wash()

        print("\n> You have busted all your chips! Do you want to play again? Type 'y' to play again or 'n' to leave:")
        string = input()
        game.errorTrap("y", "y", "n", "n", string)

        if string == "n":
            print("\n> Nice playing with you!") 
        
if __name__ == "__main__":
    main()
