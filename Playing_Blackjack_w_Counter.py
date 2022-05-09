import random
import pandas as pd

running_count = 0
true_count = 0

def check_ace(hand): 
    """
    Checks if there's an ace in the hand in case total went over 21
    """
    if 'A' in hand:
        hand[hand.index('A')] = 'A.'
        return True
    else:
        return False
    

def hand_total(hand): 
    """
    Calculates sum total values from a list of strings using a dictionary
    """
    d_val = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
             '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11, 'A.': 1}
    return sum(d_val[i] for i in hand)


def deal_card(hand, deck, num_of_cards=1): 
    """
    Deals a card, defaulted to one card
    """
    for _ in range(num_of_cards):
        hand.append(deck.pop())
    return hand


def create_deck(num_of_decks=1): 
    """
    Creates a standard playing card deck, defaulted to one deck
    """
    deck = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']*4*num_of_decks
    random.shuffle(deck)
    return deck


def player_print(hand, total): 
    """
    Prints player's current hand and total
    """
    print("\nYour hand: ", hand, "\nYour total: ", total)
    
    
def dealer_print(hand, total): 
    """
    Prints dealer's current hand and total
    """
    print("\nDealer hand: ", hand, "\nDealer total: ", total)
    

def play_again():
    """
    Loops the game
    """
    while True: 
        # Asking the player to play again or not
        ans = input("Play again? \n").lower()
        if ans == 'yes' or ans == 'y':
            print("\n------------ Another Round of Blackjack -------------")
            return True
        elif ans == 'no' or ans == 'n':
            return False
        else:
            print("Yes or no? ")
            continue

def update_count(hand, deck, number=1, print=False):
    global running_count, true_count
    running_count += card_counter(hand[-number:])
    true_count = true_counter(deck, running_count)
    if print:
        print_count(true_count, running_count)
    return running_count, true_count

def bust_check(hand, total):
    if total > 21:
        # Checking for an ace in the player hand
        if check_ace(hand):
            total = hand_total(hand)
            bust_check(hand, total)
        else:
            return True
    else:
        return False

def do_hit(hand, deck, dealer=False):
    deal_card(hand, deck)
    total = hand_total(hand)

    # Counter
    r_count, true_cnt = update_count(hand, deck, print=True)

    # Checking if the player busts
    if bust_check(hand, total):
        if dealer:
            dealer_print(hand, total)
        else:
            player_print(hand, total)
        return True, total
    else:
        if dealer:
            dealer_print(hand, total)
        else:
            player_print(hand, total)
        return False, total

def dealer_turn(your_hand, dealer_hand, total, dtotal, r_count, true_cnt, deck, turn=True): 
    """
    Activates the dealer's turn if player's move was 'stay'
    """
    # Tallying wins, losses, and draws
    wins = 0
    draw = 0
    loss = 0
    
    # Looping through the moves
    while turn:
        total  = hand_total(your_hand)
        if total > 21: 
            
            # Evaluating a player's hand to see if they have an ace
            check_ace(your_hand)
            total = hand_total(your_hand)
            player_print(your_hand, total)
            continue
            
        dtotal = hand_total(dealer_hand)
        dealer_print(dealer_hand, dtotal)

        while dtotal <= 16: 
            
            # Dealing cards to the dealer if they have less than or equal to 16
            bust, dtotal = do_hit(dealer_hand, deck, dealer=True)
            if bust:
                print("Dealer busts! You win!")
                wins += 1
                break

        if dtotal > 21:
            break
                
        # Comparing dealer hand to player hand
        if 17 <= dtotal <= 21:
            if dtotal > total:
                print("Game Over. House wins")
                loss += 1
                break
            elif dtotal < total:
                print("Congratulations! You win!")
                wins += 1
                break
            elif dtotal == total:
                print("Draw. No lost bet.")
                draw += 1
                break
            else:
                print("House busts. You win!")
                wins += 1
                break
    return [wins, loss, draw]


def card_counter(hand, strategy='Hi-Lo'):
    """
    Counting cards based on strategy selected
    Returns sum of the values
    """
    
    df = pd.read_pickle('Card_Counting_Values')

    return sum([df.loc[strategy][i].item() for i in hand])

def true_counter(deck, r_count):
    """
    Calculates and returns the true count rounded down
    """
    try:
        return r_count//(len(deck)//52)
    except:
        
        # Compensating for when there is less than 52 cards or 1 deck left
        return r_count


def print_count(true_cnt, r_count):
    """
    Prints out current counts
    """
    print('\nRunning Count: --->', r_count, '\nTrue Count: ', true_cnt)
    
def blackjack(deck, r_count, true_cnt):
    """
    Playing Blackjack
    """
    your_hand   = deal_card([], deck, 2)
    dealer_hand = deal_card([], deck, 2)

    print("Your hand: ", your_hand)
    print("Dealer hand: ", dealer_hand[:1])
    
    # Tallying wins, losses, and draws
    wins = 0
    draw = 0
    loss = 0
    
    # Card Counting
    update_count(your_hand, deck, number=2, print=True)
    update_count(dealer_hand[:1], deck, print=True)
    
    # Looping through the moves
    while len(deck) > 1:
        print('Remaining cards: ', len(deck), '\n')
        
        # Checking if the player has a natural blackjack
        if hand_total(your_hand) == 21 and len(your_hand) == 2 and hand_total(dealer_hand) < 21:
            dealer_print(dealer_hand, hand_total(dealer_hand))
            
            # Counter
            update_count(your_hand, deck, print=True)
            
            print("Congratulations! Blackjack!")
            wins += 1
            break
        
        # Checking if the player and the dealer tie if they both have natural blackjacks
        elif hand_total(your_hand) == 21 and hand_total(dealer_hand) == 21:
            dealer_print(dealer_hand, hand_total(dealer_hand))
            
            # Counter
            update_count(your_hand, deck, print=True)
            
            print("It's a draw. Bet is returned.")
            draw += 1
            break
            
        # Allowing the player to make a move
        move = input("Hit or stay? ").lower()
        
        if move == "hit" or move == "h":
            bust, total = do_hit(your_hand, deck)
            if bust:
                player_print(your_hand, total)
                print("Dealer wins. You lose.")
                loss += 1
                break
        elif move == "stay" or move == "s":
            total = hand_total(your_hand)
            dtotal = hand_total(dealer_hand)
            
            # Counter
            update_count(dealer_hand, deck, print=True)
            
            # Running the function for the dealer's turn
            result = dealer_turn(your_hand, dealer_hand, total, dtotal, r_count, true_cnt, deck)
            
            # The results of the dealer's turn
            wins += result[0]
            loss += result[1]
            draw += result[2]
            break
                
        else:
            # Continuing the loop if input was different from 'hit' or 'stay'
            print('Please type hit or stay')
            continue
            
    # Returning the results of the game
    global running_count, true_count
    return [wins, loss, draw, running_count, true_count]


def play_blackjack():
    """
    Looping the game until no cards left
    """
    deck = create_deck(6)
    
    play = True
    wins = 0
    rounds_played = 0
    r_count = 0
    true_cnt = 0
    
    while play:
        
        # Running blackjack
        game = blackjack(deck, r_count, true_cnt)
        
        # Recording the results: wins, loss, draw
        wins += game[0]
        rounds_played += sum(game[:3])
        
        r_count = game[3]
        true_cnt = game[4]
        
        print("Wins: ", wins, '/', rounds_played)
        
        # Determining if there are enough cards left
        if len(deck) < 12:
            print("Not enough cards left. Game over.")
            break
        play = play_again()
        
play_blackjack()