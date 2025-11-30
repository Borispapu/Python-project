import random
import os
from collections import Counter
import tkinter as tk

# ==============================
# Tkinter Dashboard
# ==============================

root = None
money_var = None
last_game_var = None
last_result_var = None

def create_dashboard():
    """Create a simple Tkinter window that shows money, last game, last result."""
    global root, money_var, last_game_var, last_result_var
    root = tk.Tk()
    root.title("Maroon Oasis Dashboard")

    tk.Label(root, text="Maroon Oasis Casino", font=("Arial", 14, "bold")).pack(pady=5)

    money_var = tk.StringVar()
    last_game_var = tk.StringVar()
    last_result_var = tk.StringVar()

    tk.Label(root, textvariable=money_var, font=("Arial", 12)).pack(pady=2)
    tk.Label(root, textvariable=last_game_var, font=("Arial", 11)).pack(pady=2)
    tk.Label(root, textvariable=last_result_var, font=("Arial", 11)).pack(pady=2)

    # Initial values
    money_var.set("Money: $0")
    last_game_var.set("Last game: None")
    last_result_var.set("Last result: -")

def update_dashboard(money, game_name="", result_text=""):
    """Update the Tkinter dashboard labels and keep the window responsive."""
    global root, money_var, last_game_var, last_result_var
    if root is None:
        return
    try:
        if money_var is not None:
            money_var.set("Money: ${}".format(money))  # uses format()
        if last_game_var is not None and game_name:
            last_game_var.set("Last game: {}".format(game_name))
        if last_result_var is not None and result_text:
            last_result_var.set("Last result: {}".format(result_text))
        root.update_idletasks()
        root.update()
    except tk.TclError:
        # Window probably closed by the user; ignore further updates
        pass

# ==============================
# Save / Load Money
# ==============================

def load_money():
    """
    Load player's money from save.txt.
    If the file does not exist or is invalid, start with $100.
    """
    try:
        with open("save.txt", "r") as f:
            money = int(f.read().strip())
    except FileNotFoundError:
        print("(No save file found — starting with $100.)")
        money = 100
    except ValueError:
        print("Save file is corrupted. Resetting balance to $100.")
        money = 100
    except Exception as e:
        print("Unexpected error loading save file:", e)
        money = 100

    # If the loaded amount is 0 or negative, reset to 100
    if money <= 0:
        print("You were broke! Resetting your balance to $100.")
        money = 100
        save_money(money)

    return money

def save_money(money):
    try:
        with open("save.txt", "w") as f:
            f.write(str(money))
    except Exception as e:
        print("Error saving progress:", e)

def clear_save():
    """Delete save file to permanently end the current run."""
    try:
        if os.path.exists("save.txt"):
            os.remove("save.txt")
    except Exception as e:
        print("Error clearing save:", e)

# ==============================
# Tutorials
# ==============================

def blackjack_tutorial():
    print("\n==============================")
    print("  BLACKJACK TUTORIAL ")
    print("==============================")
    print("- Goal: Get as close to 21 as possible without going over.")
    print("- Number cards = their value, face cards = 10, Aces = 1 or 11.")
    print("- You start with 2 cards; so does the dealer.")
    print("- On your turn you can:")
    print("    • Hit: take another card.")
    print("    • Stand: keep your total and end your turn.")
    print("- If your total goes over 21, you bust and lose immediately.")
    print("- After you stand, the dealer draws until they reach at least 17.")
    print("- Closest to 21 without busting wins the round.\n")
    input("Press Enter to begin Blackjack...")

def poker_tutorial():
    print("\n==============================")
    print("  TEXAS HOLD'EM TUTORIAL ")
    print("==============================")
    print("- You and Darren each get 2 hidden 'hole cards'.")
    print("- Five shared 'community cards' come in stages:")
    print("    • Flop: 3 cards")
    print("    • Turn: 1 card")
    print("    • River: 1 card")
    print("- You make the best 5-card hand using any combination of your")
    print("  hole cards + the board.")
    print("- Hand strength (best to worst):")
    print("    Straight Flush > Four of a Kind > Full House > Flush")
    print("    > Straight > Three of a Kind > Two Pair > One Pair > High Card")
    print("- On each street (flop, turn, river) you can:")
    print("    • Call/Check: match the action without raising.")
    print("    • Raise: increase the amount at stake.")
    print("    • Fold: give up the pot immediately.")
    print("- At showdown, the best hand wins the pot.")
    print("- Darren bets based on how strong his hand is, and sometimes bluffs.\n")
    input("Press Enter to sit down with Darren...")

# ==============================
# Blackjack Game
# ==============================

def blackjack(money):
    print("\nWelcome to Blackjack! Your dealer today will be Chris.\n")
    print("You start with $", money)
    update_dashboard(money, "Blackjack", "New Blackjack session")

    # Offer tutorial at the start of Blackjack
    need_tut = input("Need a quick Blackjack tutorial? (y/n): ").lower()
    if need_tut == "y":
        blackjack_tutorial()

    cards = {
        "2": 2, "3": 3, "4": 4, "5": 5,
        "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11
    }
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    def get_total(hand):
        total = 0
        aces = 0
        for rank, _suit in hand:
            total += cards[rank]
            if rank == "Ace":
                aces += 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def show_cards(hand):
        for rank, suit in hand:
            print("-", rank, "of", suit)

    while money > 0:
        print("\nYou have $", money)
        update_dashboard(money, "Blackjack", "Betting a new hand")
        try:
            bet = int(input("How much do you want to bet? "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if bet > money or bet <= 0:
            print("Invalid bet. Try again.")
            continue

        deck = [(rank, suit) for rank in cards.keys() for suit in suits]
        random.shuffle(deck)

        player_cards = [deck.pop(), deck.pop()]
        dealer_cards = [deck.pop(), deck.pop()]

        print("\nYour cards are:")
        show_cards(player_cards)
        print("Dealer shows:", dealer_cards[0][0], "of", dealer_cards[0][1])

        # Player turn
        while True:
            player_total = get_total(player_cards)
            print("Your total is:", player_total)

            if player_total > 21:
                print("You bust! Dealer wins.")
                money -= bet
                update_dashboard(money, "Blackjack", "You busted this hand")
                break

            choice = input("Do you want another card? (y/n): ").lower()
            if choice == "y":
                card = deck.pop()
                player_cards.append(card)
                print("You drew:", card[0], "of", card[1])
            else:
                break

        # Dealer turn and result if player didn't bust
        if get_total(player_cards) <= 21:
            print("\nDealer's turn...")
            print("Dealer's cards:")
            show_cards(dealer_cards)

            while get_total(dealer_cards) < 17:
                card = deck.pop()
                dealer_cards.append(card)
                print("Dealer draws:", card[0], "of", card[1])

            dealer_total = get_total(dealer_cards)
            player_total = get_total(player_cards)
            print("Dealer total is:", dealer_total)

            if dealer_total > 21:
                print("Dealer busts! You win!")
                money += bet
                update_dashboard(money, "Blackjack", "You won this hand")
            elif dealer_total < player_total:
                print("You win!")
                money += bet
                update_dashboard(money, "Blackjack", "You won this hand")
            elif dealer_total > player_total:
                print("Dealer wins!")
                money -= bet
                update_dashboard(money, "Blackjack", "Dealer won this hand")
            else:
                print("It's a tie!")
                update_dashboard(money, "Blackjack", "Push (tie)")

        save_money(money)

        if money <= 0:
            print("\nYou're out of money! Game over.")
            update_dashboard(money, "Blackjack", "You’re out of money")
            break

        again = input("\nPlay Blackjack again? (y/n): ").lower()
        if again != "y":
            print("Leaving the Blackjack table with $", money)
            update_dashboard(money, "Blackjack", "Leaving Blackjack table")
            break

    return money

# ==============================
# Poker Core Functions
# ==============================

def deckOfCards():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    rank_values = {str(n): n for n in range(2, 11)}
    rank_values.update({'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14})
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck, rank_values

def deal_poker_round():
    deck, rank_values = deckOfCards()

    flop = [deck.pop(), deck.pop(), deck.pop()]
    turn_card = deck.pop()
    river_card = deck.pop()

    playerCards = [deck.pop(), deck.pop()]
    sheriffCards = [deck.pop(), deck.pop()]

    combinedPlayer = playerCards + flop + [turn_card, river_card]
    combinedSheriff = sheriffCards + flop + [turn_card, river_card]

    def card_str(card):
        return f"{card[0]} of {card[1]}"

    playerHandStr = f"{card_str(playerCards[0])} and {card_str(playerCards[1])}"
    sheriffHandStr = f"{card_str(sheriffCards[0])} and {card_str(sheriffCards[1])}"
    flopStr = ", ".join(card_str(c) for c in flop)
    turnStr = flopStr + f", {card_str(turn_card)}"
    riverStr = turnStr + f", {card_str(river_card)}"

    return (combinedPlayer, combinedSheriff,
            playerHandStr, sheriffHandStr,
            flopStr, turnStr, riverStr,
            sheriffCards, playerCards, rank_values)

def best_straight_high(values):
    vset = set(values)
    if {14, 2, 3, 4, 5}.issubset(vset):
        best = 5
    else:
        best = None
        for high in range(14, 4, -1):
            if all((high - i) in vset for i in range(5)):
                best = high
                break
    return best

def evaluate_7cards(cards, rank_values):
    values = [rank_values[r] for (r, s) in cards]
    counts = Counter(values)
    unique_vals = sorted(counts.keys(), reverse=True)

    suit_to_vals = {}
    for (r, s) in cards:
        suit_to_vals.setdefault(s, []).append(rank_values[r])

    flush_suit = None
    flush_vals = []
    for suit, vals in suit_to_vals.items():
        if len(vals) >= 5:
            flush_suit = suit
            flush_vals = sorted(vals, reverse=True)
            break

    straight_high = best_straight_high(values)
    straight_flush_high = None
    if flush_suit:
        sf_high = best_straight_high(suit_to_vals[flush_suit])
        if sf_high is not None:
            straight_flush_high = sf_high

    # Category: 0–8
    # 8: Straight flush, 7: quads, 6: full house, 5: flush, 4: straight,
    # 3: trips, 2: two pair, 1: one pair, 0: high card

    if straight_flush_high is not None:
        return (8, [straight_flush_high])

    fours = [v for v, c in counts.items() if c == 4]
    if fours:
        four_val = max(fours)
        kicker = max(v for v in unique_vals if v != four_val)
        return (7, [four_val, kicker])

    trips = sorted([v for v, c in counts.items() if c == 3], reverse=True)
    pairs = sorted([v for v, c in counts.items() if c == 2], reverse=True)
    if trips and (len(trips) >= 2 or pairs):
        if len(trips) >= 2:
            return (6, [trips[0], trips[1]])
        else:
            return (6, [trips[0], pairs[0]])

    if flush_suit:
        top5 = flush_vals[:5]
        return (5, top5)

    if straight_high is not None:
        return (4, [straight_high])

    if trips:
        remaining = [v for v in unique_vals if v not in trips]
        return (3, [trips[0]] + remaining[:2])

    if len(pairs) >= 2:
        top_two = pairs[:2]
        remaining = [v for v in unique_vals if v not in top_two]
        return (2, top_two + remaining[:1])

    if len(pairs) == 1:
        pair_val = pairs[0]
        remaining = [v for v in unique_vals if v != pair_val]
        return (1, [pair_val] + remaining[:3])

    return (0, unique_vals[:5])

def chickenDinner(combinedPlayer, combinedSheriff, rank_values):
    p_rank = evaluate_7cards(combinedPlayer, rank_values)
    s_rank = evaluate_7cards(combinedSheriff, rank_values)
    if p_rank > s_rank:
        return "player", p_rank, s_rank
    elif s_rank > p_rank:
        return "sheriff", p_rank, s_rank
    else:
        return "tie", p_rank, s_rank

def describe_rank(rank_tuple):
    category, _ = rank_tuple
    cat_names = {
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "One Pair",
        0: "High Card"
    }
    return cat_names.get(category, "Unknown")

# ==============================
# Darren's AI (1–9 style strength)
# ==============================

def sheriffDecision(stage, sheriffCards, boardCards, rank_values, playerBet):
    """
    stage: 'flop', 'turn', 'river'
    sheriffCards: Darren's 2 hole cards
    boardCards: community cards visible so far
    playerBet: current pot (amount you stand to win/lose)
    """
    allCards = sheriffCards + boardCards
    sheriffRank = evaluate_7cards(allCards, rank_values)
    category, _ = sheriffRank

    # Convert 0–8 → 1–9 strength
    strength = category + 1

    # Pot size impression
    if playerBet <= 6:
        betLevel = "small"
    elif playerBet <= 15:
        betLevel = "medium"
    else:
        betLevel = "big"

    strong_raise_lines = [
        "I like these odds. Let's kick this up a notch.",
        "You sure you wanna dance with that hand?",
        "That's a pretty pot. I'm fixin' to make it bigger."
    ]
    strong_call_lines = [
        "I'll ride this one out.",
        "I ain't scared of a little pressure.",
        "I'll see what you've got."
    ]
    medium_call_lines = [
        "I'll humor you for now.",
        "Guess I'll stick around.",
        "You ain't scaring me off that easy."
    ]
    medium_fold_lines = [
        "Not worth holstering my badge for this one.",
        "You can have this one, slick.",
        "I know when to holster my chips."
    ]
    weak_fold_lines = [
        "Yeah, that bet smells trouble. I'm out.",
        "I'll live to fight the next hand.",
        "You win this showdown, partner."
    ]
    bluff_call_lines = [
        "I'm calling you on principle alone.",
        "Something smells off, so I'll see it.",
        "I don't buy that story, kid."
    ]

    import random

    # Decision logic: stronger hand → more raising, weaker → more folding
    if strength >= 8:  # monsters
        action = "raise"
        sheriffRaise = 6 if betLevel != "small" else 4
        line = random.choice(strong_raise_lines)

    elif strength >= 6:  # full house / flush / straight
        if betLevel == "big":
            if random.random() < 0.7:
                action = "call"
                sheriffRaise = 0
                line = random.choice(strong_call_lines)
            else:
                action = "raise"
                sheriffRaise = 3
                line = random.choice(strong_raise_lines)
        else:
            action = "raise"
            sheriffRaise = 3
            line = random.choice(strong_raise_lines)

    elif strength >= 4:  # medium strength
        if betLevel == "big":
            if random.random() < 0.5:
                action = "call"
                sheriffRaise = 0
                line = random.choice(medium_call_lines)
            else:
                action = "fold"
                sheriffRaise = 0
                line = random.choice(medium_fold_lines)
        elif betLevel == "medium":
            action = "call"
            sheriffRaise = 0
            line = random.choice(medium_call_lines)
        else:  # small pot
            if random.random() < 0.5:
                action = "raise"
                sheriffRaise = 2
                line = random.choice(strong_raise_lines)
            else:
                action = "call"
                sheriffRaise = 0
                line = random.choice(medium_call_lines)

    elif strength >= 2:  # weakish
        if betLevel == "small":
            if random.random() < 0.5:
                action = "call"
                sheriffRaise = 0
                line = random.choice(bluff_call_lines)
            else:
                action = "fold"
                sheriffRaise = 0
                line = random.choice(weak_fold_lines)
        elif betLevel == "medium":
            if random.random() < 0.3:
                action = "call"
                sheriffRaise = 0
                line = random.choice(medium_call_lines)
            else:
                action = "fold"
                sheriffRaise = 0
                line = random.choice(medium_fold_lines)
        else:
            action = "fold"
            sheriffRaise = 0
            line = random.choice(weak_fold_lines)

    else:  # complete air
        if betLevel == "small":
            if random.random() < 0.3:
                action = "raise"
                sheriffRaise = 2
                line = "Sometimes you gotta win without the cards."
            else:
                action = "fold"
                sheriffRaise = 0
                line = random.choice(weak_fold_lines)
        else:
            action = "fold"
            sheriffRaise = 0
            line = random.choice(weak_fold_lines)

    return action, line, sheriffRaise

# ==============================
# Poker Game Round
# ==============================

def round(money):
    update_dashboard(money, "Poker", "New Poker session")
    firstTime = True
    playAgain = "y"

    while playAgain == "y" and money > 0:
        (combinedPlayer, combinedSheriff,
         playerHand, sheriffHand,
         flop, turn, river,
         sheriffCards, playerCards,
         rank_values) = deal_poker_round()

        winner = "tie"

        if firstTime:
            print("\nYou sit down at the Poker table across from Darren the Sheriff.")
            # Offer tutorial once at the very start of poker session
            need_tut = input("Need a quick Poker tutorial? (y/n): ").lower()
            if need_tut == "y":
                poker_tutorial()
            print("You'll each ante two dollars a round.")
            playAgain = input("Ready to play? (y/n)\nInput: ").lower()
            firstTime = False
        else:
            playAgain = input("Ready for another round? (y/n)\nInput: ").lower()

        if playAgain != "y":
            update_dashboard(money, "Poker", "Leaving Poker table")
            break

        playerBet = 2
        nextRound = True

        # ========== FLOP ==========
        print("\nYour lucky hand:", playerHand)
        print("The flop reveals...", flop)
        update_dashboard(money, "Poker", "Flop dealt")

        while nextRound:
            try:
                roundChoice = int(input("\nFLOP - What would you like to do?\n1. Call/Check\n2. Raise\n3. Fold\nInput: "))
            except ValueError:
                print("Please give a number.")
                continue
            if roundChoice == 1:
                break
            elif roundChoice == 2:
                try:
                    raiseAmount = int(input("Raise by: "))
                    if raiseAmount > 0:
                        playerBet += raiseAmount
                        print(f"You raise. Pot is now ${playerBet}.")
                    else:
                        print("Raise must be positive.")
                        continue
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                break
            elif roundChoice == 3:
                nextRound = False
                winner = "sheriff"
                print("You fold. Darren takes the pot.")
                update_dashboard(money, "Poker", "You folded on the flop")
                break
            else:
                print("Please choose 1, 2, or 3.")

        if nextRound:
            boardCards = combinedSheriff[2:5]
            sheriffAction, sheriffLine, sheriffRaise = sheriffDecision("flop", sheriffCards, boardCards, rank_values, playerBet)
            print(f'\nDarren: "{sheriffLine}"')

            if sheriffAction == "fold":
                winner = "player"
                print("Darren folds. You take the pot.")
                nextRound = False
                update_dashboard(money, "Poker", "Darren folded on the flop")
            elif sheriffAction == "raise":
                playerBet += sheriffRaise
                print(f"Darren raises ${sheriffRaise}. Pot is now ${playerBet}.")
                while True:
                    resp = input("1. Call  2. Fold\nInput: ")
                    if resp == "1":
                        print("You call Darren's raise.")
                        break
                    elif resp == "2":
                        print("You fold to Darren's raise.")
                        winner = "sheriff"
                        nextRound = False
                        update_dashboard(money, "Poker", "You folded to a flop raise")
                        break
                    else:
                        print("Please choose 1 or 2.")

        # ========== TURN ==========
        if nextRound:
            print("\nThe turn reveals...", turn)
            update_dashboard(money, "Poker", "Turn dealt")

            while nextRound:
                try:
                    roundChoice = int(input("\nTURN - What would you like to do?\n1. Call/Check\n2. Raise\n3. Fold\nInput: "))
                except ValueError:
                    print("Please give a number.")
                    continue
                if roundChoice == 1:
                    break
                elif roundChoice == 2:
                    try:
                        raiseAmount = int(input("Raise by: "))
                        if raiseAmount > 0:
                            playerBet += raiseAmount
                            print(f"You raise. Pot is now ${playerBet}.")
                        else:
                            print("Raise must be positive.")
                            continue
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                    break
                elif roundChoice == 3:
                    nextRound = False
                    winner = "sheriff"
                    print("You fold. Darren takes the pot.")
                    update_dashboard(money, "Poker", "You folded on the turn")
                    break
                else:
                    print("Please choose 1, 2, or 3.")

        if nextRound:
            boardCards = combinedSheriff[2:6]
            sheriffAction, sheriffLine, sheriffRaise = sheriffDecision("turn", sheriffCards, boardCards, rank_values, playerBet)
            print(f'\nDarren: "{sheriffLine}"')

            if sheriffAction == "fold":
                winner = "player"
                print("Darren folds. You take the pot.")
                nextRound = False
                update_dashboard(money, "Poker", "Darren folded on the turn")
            elif sheriffAction == "raise":
                playerBet += sheriffRaise
                print(f"Darren raises ${sheriffRaise}. Pot is now ${playerBet}.")
                while True:
                    resp = input("1. Call  2. Fold\nInput: ")
                    if resp == "1":
                        print("You call Darren's raise.")
                        break
                    elif resp == "2":
                        print("You fold to Darren's raise.")
                        winner = "sheriff"
                        nextRound = False
                        update_dashboard(money, "Poker", "You folded to a turn raise")
                        break
                    else:
                        print("Please choose 1 or 2.")

        # ========== RIVER ==========
        if nextRound:
            print("\nThe river reveals...", river)
            update_dashboard(money, "Poker", "River dealt")

            while nextRound:
                try:
                    roundChoice = int(input("\nRIVER - What would you like to do?\n1. Call/Check\n2. Raise\n3. Fold\nInput: "))
                except ValueError:
                    print("Please give a number.")
                    continue
                if roundChoice == 1:
                    break
                elif roundChoice == 2:
                    try:
                        raiseAmount = int(input("Raise by: "))
                        if raiseAmount > 0:
                            playerBet += raiseAmount
                            print(f"You raise. Pot is now ${playerBet}.")
                        else:
                            print("Raise must be positive.")
                            continue
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                    break
                elif roundChoice == 3:
                    nextRound = False
                    winner = "sheriff"
                    print("You fold. Darren takes the pot.")
                    update_dashboard(money, "Poker", "You folded on the river")
                    break
                else:
                    print("Please choose 1, 2, or 3.")

        # ========== SHOWDOWN ==========
        if nextRound:
            winner, playerRank, sheriffRank = chickenDinner(combinedPlayer, combinedSheriff, rank_values)
            print("\nShowdown!")
            print("Your hand:", describe_rank(playerRank))
            print("Darren's hand:", describe_rank(sheriffRank))

        if winner == "sheriff":
            print("Looks like Darren won this round!")
            money -= playerBet
            update_dashboard(money, "Poker", "Darren won the hand")
        elif winner == "player":
            print("You won this round against Darren!")
            money += playerBet
            update_dashboard(money, "Poker", "You won the hand")
        else:
            print("It's a tie! Pot split.")
            update_dashboard(money, "Poker", "Hand ended in a tie")

        print("You now have $", money)
        save_money(money)

        if money <= 0:
            print("You went bust at the poker table!")
            update_dashboard(money, "Poker", "You went bust at Poker")
            break

    save_money(money)
    return money

# ==============================
# Slots Game (3x3 Slot Machine)
# ==============================

class SlotMachine:
    """
    Simple SlotMachine class for a 3x3 slot game.

    - It does NOT touch the global save system directly.
    - It only manages its own balance and one spin at a time.
    - The outer function 'slots(money)' will connect it to your casino.
    """

    def __init__(self, starting_balance, bet_per_spin=10):
        """
        :param starting_balance: money the player brings to the slot machine
        :param bet_per_spin: fixed amount of money used on each spin
        """
        self.balance = starting_balance
        self.bet = bet_per_spin
        # Available symbols for the slot machine
        self.symbols = ['A', 'B', 'C', '7', '$']

    def set_bet(self, new_bet):
        """Change the bet amount if it is a positive value."""
        if new_bet > 0:
            self.bet = new_bet

    def get_bet(self):
        """Return the current bet per spin."""
        return self.bet

    def get_balance(self):
        """Return the current balance inside the slot machine."""
        return self.balance

    def show_balance(self):
        """Print the current slot-machine balance."""
        print(f"\nCurrent balance at the slots: ${self.balance}")

    def get_random_symbol(self):
        """
        Return a random symbol from the list of available symbols.
        We use random.choice(), which picks one element from the list.
        """
        return random.choice(self.symbols)

    def get_payout_for_symbol(self, symbol):
        """
        Return how much money you win if you get 3 of the same symbol in a line.
        The payout is a multiple of the bet.
        """
        if symbol == 'A':
            return self.bet * 2
        elif symbol == 'B':
            return self.bet * 3
        elif symbol == 'C':
            return self.bet * 5
        elif symbol == '7':
            return self.bet * 10
        elif symbol == '$':
            return self.bet * 20
        else:
            return 0

    def play_slots_once(self):
        """
        Perform ONE spin of the slot machine.

        We check:
        - 3 horizontal lines
        - 3 vertical lines
        - 2 diagonal lines

        Each winning line pays separately.
        """
        # 1. Check if there is enough money to spin
        if self.balance < self.bet:
            print("You don't have enough money for another spin.")
            return

        # 2. Subtract the bet from the balance
        self.balance -= self.bet
        print(f"\nYou bet ${self.bet} on this spin.")

        # 3. Create the 3x3 grid for the slot machine (grid[row][col])
        grid = []
        for row in range(3):
            current_row = []
            for col in range(3):
                current_row.append(self.get_random_symbol())
            grid.append(current_row)

        # 4. Print the grid so the player can see the result
        print("---------------------")
        print("     SLOT MACHINE    ")
        print("---------------------")
        for row in range(3):
            # sep example
            print("|", grid[row][0], grid[row][1], grid[row][2], "|", sep=" ")
        print("---------------------")

        # 5. Build ALL possible lines (for clarity)
        #    Each item: (kind, index, [symbols...])
        #    kind: "H", "V", "D1", "D2"
        lines = []

        # Horizontals (3 rows)
        for r in range(3):
            line_symbols = [grid[r][0], grid[r][1], grid[r][2]]
            lines.append(("H", r + 1, line_symbols))

        # Verticals (3 columns)
        for c in range(3):
            line_symbols = [grid[0][c], grid[1][c], grid[2][c]]
            lines.append(("V", c + 1, line_symbols))

        # Diagonal principal (↘)
        lines.append(("D1", None, [grid[0][0], grid[1][1], grid[2][2]]))

        # Diagonal secundaria (↙)
        lines.append(("D2", None, [grid[0][2], grid[1][1], grid[2][0]]))

        total_win = 0
        win_found = False

        # 6. Check each line: 3 of the same symbol
        for kind, idx, symbols in lines:
            # len(set(symbols)) == 1 means all 3 are equal
            if len(set(symbols)) == 1:
                symbol = symbols[0]
                payout = self.get_payout_for_symbol(symbol)
                if payout <= 0:
                    continue

                win_found = True
                total_win += payout

                # Build a description depending on the kind of line
                if kind == "H":
                    desc = f"3 {symbol} in a horizontal line on row {idx}"
                elif kind == "V":
                    desc = f"3 {symbol} in a vertical line on column {idx}"
                elif kind == "D1":
                    desc = f"3 {symbol} on the main diagonal (↘)"
                else:  # "D2"
                    desc = f"3 {symbol} on the secondary diagonal (↙)"

                print(f"You won with {desc}! → You win ${payout}.")

        # 7. Add total win to the balance
        if win_found:
            self.balance += total_win
            print(f"Total win this spin: ${total_win}.")
        else:
            print("No winning lines this time.")

        # 8. Show the new balance
        print(f"Balance after spin: ${self.balance}")

def slots(money):
    """
    Slots game wrapper that plugs into the EXISTING casino structure.

    - Takes the current 'money' from the main menu.
    - Creates a SlotMachine with that money.
    - Lets the player spin until they quit or run out of money.
    - Returns the final balance back to the main menu.
    """
    print("\nWelcome to Slots! The reels are spinning at the Maroon Oasis.\n")
    print(f"You walk up to the slot machines with ${money}.\n")
    update_dashboard(money, "Slots", "Arrived at the slot machines")

    need_tut = input("Need a quick Slots tutorial? (y/n): ").lower()
    if need_tut == "y":
        print("\n==============================")
        print("        SLOTS TUTORIAL        ")
        print("==============================")
        print("- You choose a fixed bet amount per spin.")
        print("- The machine shows a 3x3 grid of symbols.")
        print("- You win with:")
        print("    • 3 in a row HORIZONTAL")
        print("    • 3 in a row VERTICAL")
        print("    • 3 in a row DIAGONAL (cruzado)")
        print("- Different symbols pay different amounts.")
        print("- Multiple lines can win at the same time.\n")
        input("Press Enter to start spinning...")

    # Ask the player for a bet per spin (must be <= money)
    while True:
        try:
            bet_input = int(input(f"\nHow much do you want to bet per spin? (You have ${money}): "))
            if bet_input <= 0:
                print("Bet must be a positive number.")
            elif bet_input > money:
                print("You cannot bet more than you have.")
            else:
                break
        except ValueError:
            print("Please enter a valid whole number.")

    # Create the slot machine with the player's balance
    machine = SlotMachine(starting_balance=money, bet_per_spin=bet_input)

    choice = "y"
    while choice.lower() == "y" and machine.get_balance() > 0:
        machine.show_balance()
        update_dashboard(machine.get_balance(), "Slots", "Spinning the reels")
        machine.play_slots_once()

        if machine.get_balance() <= 0:
            print("\nYou ran out of money at the slot machines!")
            update_dashboard(machine.get_balance(), "Slots", "Out of money at slots")
            break

        choice = input("\nSpin again? (y/n): ")

    final_balance = machine.get_balance()
    print(f"\nYou leave the slot machines with ${final_balance}.")
    save_money(final_balance)
    update_dashboard(final_balance, "Slots", "Left the slot machines")
    return final_balance

# ==============================
# Main Menu
# ==============================

def main():
    print("Welcome to the Maroon Oasis!\n")
    print("You're here to win big and lose nothing!")
    print("Practice gambling in this safe space, and see how much you can make from $100!\n\n")

    # Create the Tkinter dashboard window
    create_dashboard()

    money = load_money()
    update_dashboard(money, "", "Welcome to the casino")
    gameChoice = ""

    while gameChoice not in ("5", "6"):
        if money == 0:
            print("You went bust, try again another day!")
            update_dashboard(money, "", "You went bust overall")
            break

        print("\n==================")
        print(" CASINO MENU ")
        print("==================")
        print("1. Poker: Texas Hold 'em")
        print("2. Blackjack")
        print("3. Slots")
        print("4. Check Account Balance")
        print("5. Save & Quit")
        print("6. End Run (delete save and quit)\n")

        gameChoice = input("\033[1mWhat do you want to play? \033[0m")

        if gameChoice == "1":
            money = round(money)
        elif gameChoice == "2":
            money = blackjack(money)
            save_money(money)
        elif gameChoice == "3":
            money = slots(money)
        elif gameChoice == "4":
            print(f"\nYour current balance is: ${money}")
            update_dashboard(money, "", "Checked account balance")
        elif gameChoice == "5":
            print("\nThank you for playing! You leave with $", money)
            save_money(money)
            print("Your run has been saved. See you next time!")
            update_dashboard(money, "", "Saved & quit")
            break
        elif gameChoice == "6":
            print("\nYou chose to end this run permanently.")
            print("Clearing your save file... Next time you'll start over at $100.")
            clear_save()
            update_dashboard(0, "", "Run ended, save cleared")
            break
        else:
            print("Please choose a valid option (1-6).")

if __name__ == "__main__":
    main()
