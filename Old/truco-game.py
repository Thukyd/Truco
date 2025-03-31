import random
import os
import time
import sys

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value  # Truco specific value (for ranking)
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def get_display(self):
        """Returns a display-friendly representation of the card with Spanish deck symbols"""
        suit_symbols = {
            'Espadas': '🗡️', # Sword for Espadas
            'Bastos': '🏑',  # Hockey stick for Bastos (club/baton)
            'Oros': '🪙',    # Gold coin for Oros
            'Copas': '🏆'    # Trophy/cup for Copas
        }
        
        # Handle numeric and face cards
        if self.rank in ['Sota', 'Caballo', 'Rey']:
            rank_display = {'Sota': 'J', 'Caballo': 'C', 'Rey': 'R'}[self.rank]
        else:
            rank_display = self.rank
            
        return f"{rank_display}{suit_symbols[self.suit]}"

class Deck:
    def __init__(self):
        self.cards = []
        self.create_truco_deck()
        
    def create_truco_deck(self):
        """Creates a Spanish deck (40 cards) with Truco-specific values"""
        suits = ['Espadas', 'Bastos', 'Oros', 'Copas']
        
        # Truco uses a special ranking of cards
        # The ranking from highest to lowest is:
        # 1 of Espadas, 1 of Bastos, 7 of Espadas, 7 of Oros
        # 3s, 2s, 1s (except the 1 of Espadas and 1 of Bastos), 
        # Rey (King), Caballo (Knight), Sota (Jack), 7s (except 7 of Espadas and 7 of Oros),
        # 6s, 5s, 4s
        
        # We'll assign a value to each card for easy comparison
        special_cards = {
            ('Espadas', '1'): 14,  # Highest card
            ('Bastos', '1'): 13,
            ('Espadas', '7'): 12,
            ('Oros', '7'): 11
        }
        
        # Add all cards with their Truco values
        for suit in suits:
            # Add numbered cards 1-7
            for rank in range(1, 8):
                rank_str = str(rank)
                
                # Check if it's a special card
                if (suit, rank_str) in special_cards:
                    value = special_cards[(suit, rank_str)]
                elif rank == 3:
                    value = 10  # All 3s
                elif rank == 2:
                    value = 9   # All 2s
                elif rank == 1:  # Regular 1s (not Espadas or Bastos)
                    value = 8
                elif rank == 7:  # Regular 7s (not Espadas or Oros)
                    value = 4
                elif rank == 6:
                    value = 3
                elif rank == 5:
                    value = 2
                elif rank == 4:
                    value = 1
                else:
                    value = 0
                
                self.cards.append(Card(suit, rank_str, value))
            
            # Add face cards (Sota, Caballo, Rey)
            for rank, value in [('Sota', 5), ('Caballo', 6), ('Rey', 7)]:
                self.cards.append(Card(suit, rank, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self, num_cards):
        """Deal a specific number of cards from the deck"""
        if len(self.cards) < num_cards:
            return []
        
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.team = None
        
    def add_cards(self, cards):
        self.hand.extend(cards)
        
    def play_card(self, card_index):
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None
    
    def get_hand_display(self):
        """Returns a formatted display of cards in hand with indices"""
        display = []
        for i, card in enumerate(self.hand):
            display.append(f"{i+1}: {card.get_display()} ({self.get_card_strength_description(card)})")
        return display
    
    def get_card_strength_description(self, card):
        """Returns a description of the card's strength in Truco with emojis"""
        # Top 4 cards
        if card.suit == 'Espadas' and card.rank == '1':
            return "⭐⭐⭐ Strongest card"
        elif card.suit == 'Bastos' and card.rank == '1':
            return "⭐⭐ 2nd strongest"
        elif card.suit == 'Espadas' and card.rank == '7':
            return "⭐ 3rd strongest"
        elif card.suit == 'Oros' and card.rank == '7':
            return "✨ 4th strongest"
        # Card types
        elif card.rank == '3':
            return "💪 Very strong"
        elif card.rank == '2':
            return "👍 Strong"
        elif card.rank == '1':
            return "👌 Good"
        elif card.rank in ['Rey', 'Caballo', 'Sota']:
            return "➖ Medium"
        elif card.rank == '7':
            return "🔽 Weak-Medium"
        else:
            return "👎 Weak"

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.score = 0
        
        # Assign this team to all players
        for player in players:
            player.team = self

    def add_score(self, points):
        self.score += points
        
    def has_won_game(self):
        return self.score >= 15  # First team to 15 or more points wins

class TrucoGame:
    def __init__(self, num_players=2):
        self.num_players = num_players
        if num_players not in [2, 4, 6]:
            raise ValueError("Truco must be played with 2, 4, or 6 players")
            
        self.players = []
        self.teams = []
        self.deck = None
        self.current_player_index = 0
        self.current_round = 0
        self.hand_number = 0
        self.envido_phase = True
        self.current_bet = "No bet"
        self.bet_value = 1
        self.round_cards = []
        self.round_winners = []
        self.tutorial_mode = True
        
    def get_card_strength_description(self, card):
        """Returns a description of the card's strength in Truco with emojis"""
        # Top 4 cards
        if card.suit == 'Espadas' and card.rank == '1':
            return "⭐⭐⭐ Strongest card"
        elif card.suit == 'Bastos' and card.rank == '1':
            return "⭐⭐ 2nd strongest"
        elif card.suit == 'Espadas' and card.rank == '7':
            return "⭐ 3rd strongest"
        elif card.suit == 'Oros' and card.rank == '7':
            return "✨ 4th strongest"
        # Card types
        elif card.rank == '3':
            return "💪 Very strong"
        elif card.rank == '2':
            return "👍 Strong"
        elif card.rank == '1':
            return "👌 Good"
        elif card.rank in ['Rey', 'Caballo', 'Sota']:
            return "➖ Medium"
        elif card.rank == '7':
            return "🔽 Weak-Medium"
        else:
            return "👎 Weak"
        
    def setup_game(self, player_name="Player"):
        """Initialize the game with players and teams"""
        # Create players
        team_size = self.num_players // 2  # Either 1, 2, or 3 players per team
        
        # Create human player
        human_player = Player(player_name, is_human=True)
        self.players.append(human_player)
        
        # Create AI players
        for i in range(1, self.num_players):
            ai_player = Player(f"AI Player {i}")
            self.players.append(ai_player)
        
        # Create teams
        team1_players = [self.players[i] for i in range(0, self.num_players, 2)]
        team2_players = [self.players[i] for i in range(1, self.num_players, 2)]
        
        self.teams = [
            Team("Your Team 🙂", team1_players),
            Team("Opponent Team 🤖", team2_players)
        ]
        
        print(f"\n{'='*60}")
        print(f"{'🎮 WELCOME TO ARGENTINIAN TRUCO 🎮':^60}")
        print(f"{'='*60}")
        print(f"\n👥 Team setup:")
        print(f"- {self.teams[0].name}: {', '.join(p.name for p in self.teams[0].players)}")
        print(f"- {self.teams[1].name}: {', '.join(p.name for p in self.teams[1].players)}")
        
        # Show tutorial information
        self.show_card_ranking_tutorial()
        
    def show_card_ranking_tutorial(self):
        """Display the card ranking in Truco to help the player learn"""
        print("\n" + "="*60)
        print(f"{'🃏 CARD RANKING IN ARGENTINIAN TRUCO 🃏':^60}")
        print("="*60)
        print("\nCards in Truco have a special ranking that's different from other card games.")
        print("Here's the ranking from strongest to weakest:")
        print("\n1. 1 of Espadas (🗡️) - ⭐⭐⭐ The highest card")
        print("2. 1 of Bastos (🏑) - ⭐⭐ Second highest")
        print("3. 7 of Espadas (🗡️) - ⭐ Third highest")
        print("4. 7 of Oros (🪙) - ✨ Fourth highest")
        print("5. All 3s - 💪 Very strong")
        print("6. All 2s - 👍 Strong")
        print("7. All other 1s (Oros and Copas) - 👌 Good")
        print("8. Kings (Rey) - ➖ Medium")
        print("9. Knights (Caballo) - ➖ Medium")
        print("10. Jacks (Sota) - ➖ Medium")
        print("11. All other 7s (Bastos and Copas) - 🔽 Weak-Medium")
        print("12. All 6s - 👎 Weak")
        print("13. All 5s - 👎 Weak")
        print("14. All 4s - 👎 Weak")
        print("\n🔑 Remember: This ranking is unique to Truco and mastering it is key to success!")
        print("\n💡 During the game, we'll show each card's relative strength to help you learn.")
        print("="*60)
        input("\nPress Enter to continue...")
        
    def show_betting_tutorial(self):
        """Display information about betting in Truco"""
        print("\n" + "="*60)
        print(f"{'💰 BETTING IN ARGENTINIAN TRUCO 💰':^60}")
        print("="*60)
        print("\nTruco has a unique betting system:")
        print("\n1. 🎲 Truco - Worth 2 points")
        print("   - Can be raised to Retruco")
        print("\n2. 🎯 Retruco - Worth 3 points")
        print("   - Can be raised to Vale Cuatro")
        print("\n3. 🔥 Vale Cuatro - Worth 4 points")
        print("   - The highest possible bet")
        print("\nWhen a bet is made, you can:")
        print("✅ Accept: Play for the current bet value")
        print("⬆️ Raise: Increase to the next level")
        print("❌ Decline: Give up the hand and opponent gets the current points at stake")
        print("\n🃏 Betting adds strategy and bluffing to the game!")
        print("="*60)
        input("\nPress Enter to continue...")
    
    def deal_cards(self):
        """Deal cards to all players for a new hand"""
        self.deck = Deck()
        self.deck.shuffle()
        
        # Each player gets 3 cards
        for player in self.players:
            player.hand = []
            cards = self.deck.deal(3)
            player.add_cards(cards)
        
        self.hand_number += 1
        self.current_round = 0
        self.envido_phase = True
        self.current_bet = "No bet"
        self.bet_value = 1
        self.round_cards = []
        self.round_winners = []
        
        # Determine who plays first (rotates each hand)
        self.current_player_index = (self.hand_number - 1) % self.num_players
        
        print(f"\n{'='*60}")
        print(f"{'🎮 NEW HAND 🎮':^60}")
        print(f"{'='*60}")
        print(f"\n🎲 Hand #{self.hand_number}")
        print(f"📊 Current Score: {self.teams[0].name} {self.teams[0].score} - {self.teams[1].score} {self.teams[1].name}")
        print(f"\n👉 {self.players[self.current_player_index].name} plays first this hand.")
        
        # Always display the human player's hand at the start of a new hand
        human_player = next((p for p in self.players if p.is_human), None)
        if human_player:
            print("\n🃏 Your Hand:")
            for i, card_display in enumerate(human_player.get_hand_display()):
                print(card_display)
        
    def play_game(self):
        """Main game loop"""
        self.setup_game()
        self.show_betting_tutorial()
        
        while not any(team.has_won_game() for team in self.teams):
            self.deal_cards()
            self.play_hand()
            
            # Check if any team has won
            if any(team.has_won_game() for team in self.teams):
                # Find the winning team
                winning_team = next(team for team in self.teams if team.has_won_game())
                print(f"\n{'='*60}")
                print(f"{'GAME OVER':^60}")
                print(f"{'='*60}")
                print(f"\n{winning_team.name} wins the game with {winning_team.score} points!")
                print(f"\nFinal Score: {self.teams[0].name} {self.teams[0].score} - {self.teams[1].score} {self.teams[1].name}")
                break
                
            input("\nPress Enter to continue to the next hand...")
            
    def play_hand(self):
        """Play a complete hand (3 rounds)"""
        # Main hand loop
        while len(self.round_winners) < 2 and self.current_round < 3:
            self.current_round += 1
            print(f"\n{'='*60}")
            print(f"{'🎯 ROUND ' + str(self.current_round) + ' 🎯':^60}")
            print(f"{'='*60}")
            
            # Always display human player's hand at the beginning of each round
            human_player = next((p for p in self.players if p.is_human), None)
            if human_player:
                print("\n🃏 Your Current Hand:")
                for i, card_display in enumerate(human_player.get_hand_display()):
                    print(card_display)
            
            self.round_cards = []
            
            # Each player plays one card
            for _ in range(self.num_players):
                current_player = self.players[self.current_player_index]
                
                if current_player.is_human:
                    self.human_turn()
                else:
                    self.ai_turn()
                
                # Move to next player
                self.current_player_index = (self.current_player_index + 1) % self.num_players
            
            # Determine round winner
            self.determine_round_winner()
            
            # If we have a clear winner of the hand (team won 2 rounds), end the hand
            if len(self.round_winners) >= 2:
                # Count how many times each team won
                team_wins = {team: 0 for team in self.teams}
                
                for winner in self.round_winners:
                    for team in self.teams:
                        if winner in team.players:
                            team_wins[team] += 1
                
                # Team with most wins gets the points
                winning_team = max(team_wins.items(), key=lambda x: x[1])[0]
                winning_team.add_score(self.bet_value)
                
                print(f"\n🏆 {winning_team.name} wins the hand and gets {self.bet_value} point(s)!")
                break
            
            # If we have a tie (or 1-1-1 situation), play another round
            if len(self.round_winners) == 0 and self.current_round == 3:
                print("\n🔄 The hand is tied! No points awarded.")
                break
        
    def human_turn(self):
        """Handle a human player's turn"""
        player = self.players[self.current_player_index]
        
        # First check for betting options
        if self.current_bet == "No bet" and len(player.hand) > 0:
            self.handle_betting(player)
        
        print(f"\n👤 {player.name}'s turn:")
        print(f"💰 Current bet: {self.current_bet} ({self.bet_value} points)")
        
        if self.round_cards:
            print("\n🎮 Cards played this round:")
            for i, (p, card) in enumerate(self.round_cards):
                print(f"{p.name}: {card.get_display()}")
        
        print("\n🃏 Your hand:")
        for i, card_display in enumerate(player.get_hand_display()):
            print(card_display)
        
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input("\n🤔 Which card do you want to play? (Enter the number): "))
                if 1 <= choice <= len(player.hand):
                    card = player.play_card(choice - 1)
                    self.round_cards.append((player, card))
                    print(f"\n🎯 You played: {card.get_display()}")
                    valid_choice = True
                else:
                    print("❌ Invalid card number. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def ai_turn(self):
        """Handle an AI player's turn"""
        player = self.players[self.current_player_index]
        
        # Simple AI strategy
        # If it's the betting phase, sometimes make a bet
        if self.current_bet == "No bet" and random.random() < 0.3:
            self.handle_ai_betting(player)
        
        # Choose a card (simple strategy)
        if not player.hand:
            return  # No cards to play
            
        # Determine if AI should play a strong or weak card
        if len(self.round_cards) == 0:
            # AI plays first in the round, choose randomly
            card_index = random.randint(0, len(player.hand) - 1)
        else:
            # Check the highest card played so far
            highest_card = max((card for _, card in self.round_cards), key=lambda x: x.value)
            
            # Find cards that can beat the highest card
            better_cards = [i for i, card in enumerate(player.hand) if card.value > highest_card.value]
            
            if better_cards and random.random() < 0.7:  # 70% chance to play a winning card if available
                card_index = random.choice(better_cards)
            else:
                # Play the weakest card
                card_index = min(range(len(player.hand)), key=lambda i: player.hand[i].value)
        
        card = player.play_card(card_index)
        self.round_cards.append((player, card))
        
        print(f"\n{player.name} plays: {card}")
        time.sleep(1)  # Pause for effect
    
    def handle_betting(self, player):
        """Handle betting options for human player"""
        print("\n💰 Betting options:")
        print("1. ➡️ Continue without betting")
        
        # Determine available bets based on current bet
        if self.current_bet == "No bet":
            print("2. 🎲 Truco (2 points)")
            bet_options = ["Continue", "Truco"]
        elif self.current_bet == "Truco":
            print("2. 🎯 Retruco (3 points)")
            bet_options = ["Continue", "Retruco"]
        elif self.current_bet == "Retruco":
            print("2. 🔥 Vale Cuatro (4 points)")
            bet_options = ["Continue", "Vale Cuatro"]
        else:
            # No more raising possible
            bet_options = ["Continue"]
            
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input("\nDo you want to bet? Enter your choice: "))
                if choice == 1:
                    # Continue without betting
                    print("Continuing without betting.")
                    valid_choice = True
                elif choice == 2 and len(bet_options) > 1:
                    # Make a bet
                    new_bet = bet_options[1]
                    print(f"\nYou called {new_bet}!")
                    
                    # AI response to the bet
                    ai_response = self.ai_respond_to_bet(new_bet)
                    
                    if ai_response == "accept":
                        print("Opponent accepts your bet!")
                        self.current_bet = new_bet
                        if new_bet == "Truco":
                            self.bet_value = 2
                        elif new_bet == "Retruco":
                            self.bet_value = 3
                        elif new_bet == "Vale Cuatro":
                            self.bet_value = 4
                    elif ai_response == "raise":
                        if new_bet == "Truco":
                            print("Opponent raises to Retruco!")
                            # Ask player to accept, raise to Vale Cuatro, or fold
                            self.handle_player_bet_response("Retruco")
                        elif new_bet == "Retruco":
                            print("Opponent raises to Vale Cuatro!")
                            # Ask player to accept or fold
                            self.handle_player_bet_response("Vale Cuatro")
                    elif ai_response == "decline":
                        print("Opponent declines your bet! You win this hand.")
                        self.teams[0].add_score(1 if self.current_bet == "No bet" else self.bet_value)
                        return
                    
                    valid_choice = True
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def handle_ai_betting(self, player):
        """Handle AI betting decisions"""
        # Simple AI betting strategy based on hand strength
        hand_strength = sum(card.value for card in player.hand)
        
        # Based on hand strength, decide whether to bet
        if hand_strength > 25 or random.random() < 0.2:  # Sometimes bluff
            if self.current_bet == "No bet":
                new_bet = "Truco"
                print(f"\n{player.name} calls Truco!")
                
                # Ask human to respond
                self.handle_player_bet_response("Truco")
            elif self.current_bet == "Truco" and (hand_strength > 30 or random.random() < 0.15):
                new_bet = "Retruco"
                print(f"\n{player.name} calls Retruco!")
                
                # Ask human to respond
                self.handle_player_bet_response("Retruco")
            elif self.current_bet == "Retruco" and (hand_strength > 35 or random.random() < 0.1):
                new_bet = "Vale Cuatro"
                print(f"\n{player.name} calls Vale Cuatro!")
                
                # Ask human to respond
                self.handle_player_bet_response("Vale Cuatro")
    
    def handle_player_bet_response(self, bet):
        """Handle the player's response to an AI bet"""
        print("\nHow do you respond?")
        
        if bet == "Truco":
            print("1. Accept (play for 2 points)")
            print("2. Raise to Retruco (3 points)")
            print("3. Decline (opponent gets 1 point)")
            max_choice = 3
        elif bet == "Retruco":
            print("1. Accept (play for 3 points)")
            print("2. Raise to Vale Cuatro (4 points)")
            print("3. Decline (opponent gets 2 points)")
            max_choice = 3
        elif bet == "Vale Cuatro":
            print("1. Accept (play for 4 points)")
            print("2. Decline (opponent gets 3 points)")
            max_choice = 2
            
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input("\nEnter your choice: "))
                if 1 <= choice <= max_choice:
                    if choice == 1:  # Accept
                        print(f"You accept the {bet}!")
                        self.current_bet = bet
                        if bet == "Truco":
                            self.bet_value = 2
                        elif bet == "Retruco":
                            self.bet_value = 3
                        elif bet == "Vale Cuatro":
                            self.bet_value = 4
                    elif choice == 2:
                        if bet != "Vale Cuatro":  # Raise
                            new_bet = "Retruco" if bet == "Truco" else "Vale Cuatro"
                            print(f"You raise to {new_bet}!")
                            
                            # AI responds to the raise
                            ai_response = self.ai_respond_to_bet(new_bet)
                            
                            if ai_response == "accept":
                                print(f"Opponent accepts your {new_bet}!")
                                self.current_bet = new_bet
                                self.bet_value = 3 if new_bet == "Retruco" else 4
                            elif ai_response == "decline":
                                print(f"Opponent declines your {new_bet}! You win this hand.")
                                self.teams[0].add_score(2 if new_bet == "Retruco" else 3)
                                return
                        else:  # Decline Vale Cuatro
                            print("You decline the Vale Cuatro. Opponent wins this hand.")
                            self.teams[1].add_score(3)  # Opponent team gets 3 points
                            return
                    elif choice == 3:  # Decline
                        print(f"You decline the {bet}. Opponent wins this hand.")
                        points = 1 if bet == "Truco" else (2 if bet == "Retruco" else 3)
                        self.teams[1].add_score(points)
                        return
                        
                    valid_choice = True
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def ai_respond_to_bet(self, bet):
        """Determine how AI responds to a bet"""
        # Get a random AI player from team 2
        ai_players = [p for p in self.teams[1].players if not p.is_human]
        if not ai_players:
            return "accept"  # Fallback
            
        ai_player = random.choice(ai_players)
        
        # Calculate hand strength
        hand_strength = sum(card.value for card in ai_player.hand)
        
        # Respond based on hand strength and randomness (for bluffing)
        if bet == "Truco":
            if hand_strength > 25 or random.random() < 0.1:  # 10% chance to bluff and raise
                return "raise"
            elif hand_strength > 20 or random.random() < 0.7:  # 70% chance to accept with medium hand
                return "accept"
            else:
                return "decline"
        elif bet == "Retruco":
            if hand_strength > 30 or random.random() < 0.05:  # 5% chance to bluff and raise
                return "raise"
            elif hand_strength > 25 or random.random() < 0.6:  # 60% chance to accept with good hand
                return "accept"
            else:
                return "decline"
        elif bet == "Vale Cuatro":
            if hand_strength > 30 or random.random() < 0.5:  # 50% chance to accept with strong hand
                return "accept"
            else:
                return "decline"
        
        return "accept"  # Default fallback
    
    def determine_round_winner(self):
        """Determine the winner of the current round"""
        if not self.round_cards:
            return
            
        # Find the highest card
        highest_card_value = -1
        highest_players = []
        
        for player, card in self.round_cards:
            if card.value > highest_card_value:
                highest_card_value = card.value
                highest_players = [player]
            elif card.value == highest_card_value:
                highest_players.append(player)
        
        # If there's a single winner
        if len(highest_players) == 1:
            winner = highest_players[0]
            self.round_winners.append(winner)
            
            # Determine which team won
            winning_team = self.teams[0].name if winner in self.teams[0].players else self.teams[1].name
            
            winning_card = next(card for p, card in self.round_cards if p == winner)
            print(f"\n🏆 {winner.name} wins round {self.current_round} for {winning_team}!")
            print(f"🃏 Winning card: {winning_card.get_display()} ({self.get_card_strength_description(winning_card)})")
        else:
            print(f"\n🔄 Round {self.current_round} is a tie!")
            
        # Show the current status of rounds
        if len(self.round_winners) > 0:
            print("\n📊 Rounds won:")
            team1_wins = sum(1 for winner in self.round_winners if winner in self.teams[0].players)
            team2_wins = sum(1 for winner in self.round_winners if winner in self.teams[1].players)
            
            print(f"- {self.teams[0].name}: {team1_wins}")
            print(f"- {self.teams[1].name}: {team2_wins}")
            
        # Always show human player's hand after the round
        human_player = next((p for p in self.players if p.is_human), None)
        if human_player and human_player.hand:
            print("\n🃏 Your remaining hand:")
            for i, card_display in enumerate(human_player.get_hand_display()):
                print(card_display)

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("🎮 Welcome to Argentinian Truco! 🎮")
    print("\n🎯 This game will teach you the fundamentals of Truco, especially the card values.")
    
    while True:
        print("\n👥 Select number of players:")
        print("1. 👤 vs 🤖 (2 players, 1 vs 1)")
        print("2. 👥 vs 🤖🤖 (4 players, 2 vs 2)")
        print("3. 👥👥 vs 🤖🤖🤖 (6 players, 3 vs 3)")
        
        try:
            choice = int(input("\n🔢 Enter your choice (1-3): "))
            if 1 <= choice <= 3:
                num_players = choice * 2
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    player_name = input("\n✍️ Enter your name: ")
    if not player_name.strip():
        player_name = "Player"
    
    clear_screen()
    game = TrucoGame(num_players)
    game.play_game()
    
    print("\n🎉 Thanks for playing Argentinian Truco!")
    print("🔄 Keep practicing and you'll master the card values in no time!")

if __name__ == "__main__":
    main()
