'''
 File: Blackjack.py
 Description: This program simulates a game of blackjack and
 demonstrates the concept of inheritance.
 Student: Thomas Welborn
 Date Created: 10/02/18
'''

import random

class Card (object):
  RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

  SUITS = ('C', 'D', 'H', 'S')

  # constructor
  def __init__ (self, rank = 12, suit = 'S'):
    if (rank in Card.RANKS):
      self.rank = rank
    else:
      self.rank = 12

    if (suit in Card.SUITS):
      self.suit = suit
    else:
      self.suit = 'S'

  # string representation of a Card object
  def __str__ (self):
    if (self.rank == 1):
      rank = 'A'
    elif (self.rank == 13):
      rank = 'K'
    elif (self.rank == 12):
      rank = 'Q'
    elif (self.rank == 11):
      rank = 'J'
    else:
      rank = str(self.rank)

    return rank + self.suit

  # equality tests
  def __eq__ (self, other):
    return self.rank == other.rank

  def __ne__ (self, other):
    return (self.rank != other.rank)

  def __lt__ (self, other):
    return (self.rank < other.rank)

  def __le__ (self, other):
    return (self.rank <= other.rank)

  def __gt__ (self, other):
    return (self.rank > other.rank)

  def __ge__ (self, other):
    return (self.rank >= other.rank)



class Deck (object):
  # constructor
  def __init__ (self, n = 1):
    self.deck = []
    for i in range (n):
      for suit in Card.SUITS:
        for rank in Card.RANKS:
          card = Card (rank, suit)
          self.deck.append (card)

  # shuffle the deck
  def shuffle (self):
    random.shuffle (self.deck)

  def deal (self):
    if (len(self.deck) == 0):
      return None
    else:
      return (self.deck.pop(0))



class Player (object):
  # cards is a list of Card objects
  def __init__ (self, cards):
    self.cards = cards

  # when a player hits append a card
  def hit (self, card):
    self.cards.append (card)

  # count the points in the Players's hand
  def get_points (self):
    count = 0
    for card in self.cards:
      if (card.rank > 9):
        count += 10
      elif (card.rank == 1):
        count += 11
      else:
        count += card.rank

    # deduct 10 if Ace is there and needed as 1
    for card in self.cards:
      if (count <= 21):
        break
      elif (card.rank == 1):
        count = count - 10

    return count

  # does the player have blackjack
  def has_blackjack (self):
    return (len(self.cards) == 2) and (self.get_points() == 21)

  # complete the code that prints the cards and the points
  def __str__ (self):
    out_string = ''
    for i in range (len(self.cards)):
      out_string += str(self.cards[i]) + ' '
    return out_string



class Dealer (Player):
  def __init__ (self, cards):
    Player.__init__ (self, cards)
    self.show_one_card = True

  # override the hit() function in the parent class
  def hit (self, deck):
    self.show_one_card = False
    while (self.get_points() < 17):
      self.cards.append (deck.deal())

  # return a string showing just one card if not hit yet
  def __str__ (self):
    if (self.show_one_card):
      return str(self.cards[0])
    else:
      return Player.__str__ (self)



class Blackjack (object):
  def __init__ (self, num_players = 1):
    self.deck = Deck()
    self.deck.shuffle()

    # create the number of Player objects
    self.num_players = num_players
    self.player_list = []

    for i in range (self.num_players):
      player = Player([self.deck.deal(), self.deck.deal()])
      self.player_list.append(player)

    # create the Dealer object
    # dealer also gets two cards
    self.dealer = Dealer ([self.deck.deal(), self.deck.deal()])

  def play (self):
    # print the cards that each player has
    for i in range (self.num_players):
      print ('Player ' + str(i + 1) + ' : ' + str(self.player_list[i]) + '- ' + str((self.player_list[i]).get_points()) + ' points')

    # print the cards that the dealer has
    print ('Dealer : ' + str(self.dealer))
    print (' ')

    # each player hits until he says no
    player_points = []
    for i in range (self.num_players):
      while True:
        choice = input ('Player ' + str(i+1) + ', do you want to hit? [y / n]: ')
        if choice in ('y', 'Y'):
          self.player_list[i].hit(self.deck.deal())
          points = (self.player_list[i]).get_points()
          print ('Player ' + str(i + 1) + ' : ' + str(self.player_list[i]) + '- ' + str(points) + ' points')
          if (points >= 21):
            print(' ')
            break
        else:
          print(' ')
          break
      player_points.append((self.player_list[i]).get_points())

    # dealer's turn to hit
    self.dealer.hit(self.deck)
    dealer_points = self.dealer.get_points()
    print ('Dealer : ' + str(self.dealer) + '- ' + str(dealer_points) + ' points')

    # determine the outcome; this code is written for one player
    # extend it for all players
    # create a list of 0's to store wins, loses, and ties for each player
    player_outcomes = []
    for i in range (0, self.num_players):
      player_outcomes.append(0)

    for i in range (0, self.num_players):
      if (player_points[i] > 21):
        player_outcomes[i] = 'loses'
      elif (dealer_points > 21):
        player_outcomes[i] = 'wins'
      elif (dealer_points > player_points[i]) and (dealer_points < 22):
        player_outcomes[i] = 'loses'
      elif (dealer_points < 22) and (player_points[i] < 22) and (dealer_points == player_points[i]):
        if self.player_list[i].has_blackjack() and not self.dealer.has_blackjack():
          player_outcomes[i] = 'wins'
        elif not self.player_list[i].has_blackjack() and self.dealer.has_blackjack():
          player_outcomes[i] = 'loses'
        else:
          player_outcomes[i] = 'ties'
      elif player_points[i] > dealer_points:
        player_outcomes[i] = 'wins'
      else:
        # can add more elif statements later if more outcomes are thought of
        player_outcomes[i] = 'wins'
    
    print(' ')
    for i in range (0, self.num_players):
      print('Player ' + str(i+1) + ' ' + str(player_outcomes[i]))



def main():
  num_players = int (input ('Enter number of players: '))
  while (num_players < 1 or num_players > 6):
    num_players = int (input ('Enter number of players: '))
  print(' ')

  # create the Blckjack object
  game = Blackjack (num_players)

  # start the game
  game.play()

if __name__ == '__main__':
  main()
