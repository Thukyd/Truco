import random
import os
import time
import sys
from typing import List, Tuple, Dict, Optional, Any

# ============== MODELS ===============

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
    
    def get_envido_value(self):
        """Returns the value of this card for Envido calculations"""
        if self.rank in ['Sota', 'Caballo', 'Rey']:
            return 0
        else:
            return int(self.rank)  # For cards 1-7, the value is the face value


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
            display.append(f"{i+1}: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
        return display
    
    def calculate_envido_points(self) -> int:
        """Calculate the Envido points for this player's hand"""
        if not self.hand:
            return 0
            
        # Group cards by suit
        cards_by_suit = {}
        for card in self.hand:
            if card.suit not in cards_by_suit:
                cards_by_suit[card.suit] = []
            cards_by_suit[card.suit].append(card)
        
        # Find the suit with the most cards
        best_suit = max(cards_by_suit.items(), key=lambda x: len(x[1]))[0]
        cards_in_best_suit = cards_by_suit[best_suit]
        
        # If we have at least 2 cards of the same suit
        if len(cards_in_best_suit) >= 2:
            # Sort by Envido value (descending)
            cards_in_best_suit.sort(key=lambda c: c.get_envido_value(), reverse=True)
            # Base 20 points + the two highest cards
            return 20 + cards_in_best_suit[0].get_envido_value() + cards_in_best_suit[1].get_envido_value()
        # If we only have one card of each suit, return the highest card value
        else:
            return max(card.get_envido_value() for card in self.hand)


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


# ============== UTILITIES ===============

class CardUtils:
    @staticmethod
    def get_card_strength_description(card):
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


class DisplayUtils:
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def show_big_message(message, emoji="🎮"):
        """Display a message with decorative borders"""
        print(f"\n{'='*60}")
        print(f"{emoji} {message} {emoji}".center(60))
        print(f"{'='*60}")
    
    @staticmethod
    def show_celebration(team_name, points, is_hand_win=False):
        """Show a celebration message when a team wins"""
        if is_hand_win:
            celebrations = [
                f"🎉 {team_name} wins the hand and scores {points} point(s)! 🎉",
                f"🏆 Impressive victory for {team_name}! +{points} point(s) 🏆",
                f"💯 {team_name} takes the hand! {points} point(s) awarded! 💯",
                f"🌟 Well played by {team_name}! They get {points} point(s)! 🌟"
            ]
        else:  # Round win
            celebrations = [
                f"✨ {team_name} takes the round! ✨",
                f"👏 Nice play by {team_name}! 👏",
                f"🔥 {team_name} is on fire! 🔥",
                f"💪 Strong move by {team_name}! 💪"
            ]
        
        print(f"\n{random.choice(celebrations)}")
    
    @staticmethod
    def show_tie_message():
        """Show a message when there's a tie"""
        tie_messages = [
            "🔄 It's a tie! The cards are perfectly matched! 🔄",
            "⚖️ Balance of power - this round is tied! ⚖️",
            "🤝 Both sides equally matched - it's a tie! 🤝",
            "📏 Too close to call - this round ends in a tie! 📏"
        ]
        print(f"\n{random.choice(tie_messages)}")


class TutorialManager:
    @staticmethod
    def show_card_ranking_tutorial():
        """Display the card ranking in Truco to help the player learn"""
        DisplayUtils.show_big_message("CARD RANKING IN ARGENTINIAN TRUCO", "🃏")
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
    
    @staticmethod
    def show_betting_tutorial():
        """Display information about betting in Truco"""
        DisplayUtils.show_big_message("BETTING IN ARGENTINIAN TRUCO", "💰")
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
    
    @staticmethod
    def show_envido_tutorial():
        """Display information about Envido in Truco"""
        DisplayUtils.show_big_message("ENVIDO IN ARGENTINIAN TRUCO", "💡")
        print("\nEnvido is a separate betting feature in Truco:")
        print("\n🔸 Envido is played at the beginning of each hand, before playing cards")
        print("🔸 Players bet on having the highest point total from cards of the same suit")
        print("🔸 Only cards 1-7 count for Envido points:")
        print("  - Cards 1-7 are worth their face value")
        print("  - Face cards (Sota, Caballo, Rey) are worth 0 points")
        print("🔸 Envido point calculation:")
        print("  - 20 points base for having two or more cards of the same suit")
        print("  - Add the values of your two highest cards of that suit")
        print("  - Example: Having 7🗡️ and 4🗡️ = 20 + 7 + 4 = 31 points")
        print("\n🔸 Common Envido bets:")
        print("  - Envido: Worth 2 points")
        print("  - Real Envido: Worth 3 points")
        print("  - Falta Envido: Worth enough points to win the game")
        print("\n🎮 In this game you'll be able to use Envido betting!")
        print("="*60)
        input("\nPress Enter to continue...")


# ============== BETTING SYSTEMS ===============

class TrucoBetting:
    """Handles Truco betting mechanics"""
    
    @staticmethod
    def handle_truco_betting(game, player):
        """Handle betting options for human player"""
        print("\n💰 Betting options:")
        print("1. ➡️ Continue without betting")
        
        # Determine available bets based on current bet
        if game.current_bet == "No bet":
            print("2. 🎲 Truco (2 points)")
            bet_options = ["Continue", "Truco"]
        elif game.current_bet == "Truco":
            print("2. 🎯 Retruco (3 points)")
            bet_options = ["Continue", "Retruco"]
        elif game.current_bet == "Retruco":
            print("2. 🔥 Vale Cuatro (4 points)")
            bet_options = ["Continue", "Vale Cuatro"]
        else:
            # No more raising possible
            bet_options = ["Continue"]
            
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input("\n💬 Do you want to bet? Enter your choice: "))
                if choice == 1:
                    # Continue without betting
                    print("➡️ Continuing without betting.")
                    valid_choice = True
                elif choice == 2 and len(bet_options) > 1:
                    # Make a bet
                    new_bet = bet_options[1]
                    print(f"\n🎯 You called {new_bet}!")
                    
                    # AI response to the bet
                    ai_response = TrucoBetting.ai_respond_to_bet(game, new_bet)
                    
                    if ai_response == "accept":
                        print("✅ Opponent accepts your bet!")
                        game.current_bet = new_bet
                        if new_bet == "Truco":
                            game.bet_value = 2
                        elif new_bet == "Retruco":
                            game.bet_value = 3
                        elif new_bet == "Vale Cuatro":
                            game.bet_value = 4
                    elif ai_response == "raise":
                        if new_bet == "Truco":
                            print("⬆️ Opponent raises to Retruco!")
                            # Ask player to accept, raise to Vale Cuatro, or fold
                            TrucoBetting.handle_player_bet_response(game, "Retruco")
                        elif new_bet == "Retruco":
                            print("⬆️ Opponent raises to Vale Cuatro!")
                            # Ask player to accept or fold
                            TrucoBetting.handle_player_bet_response(game, "Vale Cuatro")
                    elif ai_response == "decline":
                        print("❌ Opponent declines your bet! You win this hand.")
                        game.teams[0].add_score(1 if game.current_bet == "No bet" else game.bet_value)
                        DisplayUtils.show_celebration(game.teams[0].name, 1 if game.current_bet == "No bet" else game.bet_value, True)
                        return True  # Early end to hand
                    
                    valid_choice = True
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        return False  # Continue hand
    
    @staticmethod
    def handle_ai_truco_betting(game, player):
        """Handle AI betting decisions"""
        # Simple AI betting strategy based on hand strength
        hand_strength = sum(card.value for card in player.hand)
        
        # Based on hand strength, decide whether to bet
        if hand_strength > 25 or random.random() < 0.2:  # Sometimes bluff
            if game.current_bet == "No bet":
                new_bet = "Truco"
                print(f"\n🤖 {player.name} calls Truco!")
                
                # Ask human to respond
                return TrucoBetting.handle_player_bet_response(game, "Truco")
            elif game.current_bet == "Truco" and (hand_strength > 30 or random.random() < 0.15):
                new_bet = "Retruco"
                print(f"\n🤖 {player.name} calls Retruco!")
                
                # Ask human to respond
                return TrucoBetting.handle_player_bet_response(game, "Retruco")
            elif game.current_bet == "Retruco" and (hand_strength > 35 or random.random() < 0.1):
                new_bet = "Vale Cuatro"
                print(f"\n🤖 {player.name} calls Vale Cuatro!")
                
                # Ask human to respond
                return TrucoBetting.handle_player_bet_response(game, "Vale Cuatro")
        
        return False  # Continue hand
    
    @staticmethod
    def handle_player_bet_response(game, bet):
        """Handle the player's response to an AI bet"""
        print("\n💬 How do you respond?")
        
        if bet == "Truco":
            print("1. ✅ Accept (play for 2 points)")
            print("2. ⬆️ Raise to Retruco (3 points)")
            print("3. ❌ Decline (opponent gets 1 point)")
            max_choice = 3
        elif bet == "Retruco":
            print("1. ✅ Accept (play for 3 points)")
            print("2. ⬆️ Raise to Vale Cuatro (4 points)")
            print("3. ❌ Decline (opponent gets 2 points)")
            max_choice = 3
        elif bet == "Vale Cuatro":
            print("1. ✅ Accept (play for 4 points)")
            print("2. ❌ Decline (opponent gets 3 points)")
            max_choice = 2
            
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input("\n🔢 Enter your choice: "))
                if 1 <= choice <= max_choice:
                    if choice == 1:  # Accept
                        print(f"✅ You accept the {bet}!")
                        game.current_bet = bet
                        if bet == "Truco":
                            game.bet_value = 2
                        elif bet == "Retruco":
                            game.bet_value = 3
                        elif bet == "Vale Cuatro":
                            game.bet_value = 4
                    elif choice == 2:
                        if bet != "Vale Cuatro":  # Raise
                            new_bet = "Retruco" if bet == "Truco" else "Vale Cuatro"
                            print(f"⬆️ You raise to {new_bet}!")
                            
                            # AI responds to the raise
                            ai_response = TrucoBetting.ai_respond_to_bet(game, new_bet)
                            
                            if ai_response == "accept":
                                print(f"✅ Opponent accepts your {new_bet}!")
                                game.current_bet = new_bet
                                game.bet_value = 3 if new_bet == "Retruco" else 4
                            elif ai_response == "decline":
                                print(f"❌ Opponent declines your {new_bet}! You win this hand.")
                                game.teams[0].add_score(2 if new_bet == "Retruco" else 3)
                                DisplayUtils.show_celebration(game.teams[0].name, 2 if new_bet == "Retruco" else 3, True)
                                return True  # End hand early
                        else:  # Decline Vale Cuatro
                            print("❌ You decline the Vale Cuatro. Opponent wins this hand.")
                            game.teams[1].add_score(3)  # Opponent team gets 3 points
                            DisplayUtils.show_celebration(game.teams[1].name, 3, True)
                            return True  # End hand early
                    elif choice == 3:  # Decline
                        print(f"❌ You decline the {bet}. Opponent wins this hand.")
                        points = 1 if bet == "Truco" else (2 if bet == "Retruco" else 3)
                        game.teams[1].add_score(points)
                        DisplayUtils.show_celebration(game.teams[1].name, points, True)
                        return True  # End hand early
                        
                    valid_choice = True
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        return False  # Continue hand
    
    @staticmethod
    def ai_respond_to_bet(game, bet):
        """Determine how AI responds to a bet"""
        # Get a random AI player from team 2
        ai_players = [p for p in game.teams[1].players if not p.is_human]
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


class EnvidoBetting:
    """Handles Envido betting mechanics"""
    
    @staticmethod
    def handle_envido_phase(game):
        """Handle the Envido betting phase at the beginning of a hand"""
        # Skip Envido phase if disabled
        if not game.envido_enabled:
            return False
            
        # Find the human player
        human_player = next((p for p in game.players if p.is_human), None)
        if not human_player:
            return False
            
        # Who starts the Envido betting? Rotate starting with the dealer
        current_player_index = game.current_player_index
        
        # Display Envido points for human player
        envido_points = human_player.calculate_envido_points()
        print(f"\n💡 Your Envido points: {envido_points}")
        
        # Determine if AI will call Envido
        ai_called_envido = False
        if current_player_index != 0:  # AI plays first
            ai_player = game.players[current_player_index]
            ai_points = ai_player.calculate_envido_points()
            # AI is more likely to call Envido with higher points
            if ai_points > 25 or random.random() < 0.3:  # 30% chance to bluff
                print(f"\n🤖 {ai_player.name} calls Envido!")
                ai_called_envido = True
                return EnvidoBetting.handle_player_envido_response(game, "Envido")
        
        if not ai_called_envido:
            # Ask human if they want to call Envido
            print("\n💰 Envido options:")
            print("1. ➡️ Continue without calling Envido")
            print("2. 🎲 Call Envido (2 points)")
            
            valid_choice = False
            while not valid_choice:
                try:
                    choice = int(input("\n💬 Do you want to call Envido? Enter your choice: "))
                    if choice == 1:
                        # Continue without calling Envido
                        print("➡️ Continuing without calling Envido.")
                        valid_choice = True
                    elif choice == 2:
                        # Call Envido
                        print(f"\n🎯 You called Envido!")
                        
                        # AI response to Envido
                        ai_response = EnvidoBetting.ai_respond_to_envido(game, "Envido")
                        
                        if ai_response == "accept":
                            print("✅ Opponent accepts your Envido!")
                            # Compare Envido points
                            return EnvidoBetting.compare_envido_points(game)
                        elif ai_response == "quiero":
                            print("🎯 Opponent says 'Quiero'!")
                            # Compare Envido points
                            return EnvidoBetting.compare_envido_points(game)
                        elif ai_response == "raise":
                            print("⬆️ Opponent raises to Real Envido!")
                            # Ask player to accept, raise to Falta Envido, or decline
                            return EnvidoBetting.handle_player_envido_response(game, "Real Envido")
                        elif ai_response == "decline":
                            print("❌ Opponent declines your Envido! You win 1 point.")
                            game.teams[0].add_score(1)
                            DisplayUtils.show_celebration(game.teams[0].name, 1, True)
                            return True  # End hand early
                        
                        valid_choice = True
                    else:
                        print("❌ Invalid choice. Please try again.")
                except ValueError:
                    print("❌ Please enter a valid number.")
        
        return False  # Continue hand
    
    @staticmethod
    def handle_player_envido_response(game, bet):
        """Handle the player's response to an AI Envido bet"""
        print("\n💬 How do you respond to the Envido?")
        
        if bet == "Envido":
            print("1. ✅ Accept (play for 2 points)")
            print("2. ⬆️ Raise to Real Envido (3 more points)")
            print("3. 🚀 Raise to Falta Envido (enough to win)")
            print("4. ❌ Decline (opponent gets 1 point)")
            max_choice = 4
        elif bet == "Real Envido":
            print("1. ✅ Accept (play for 3 more points)")
            print("2. 🚀 Raise to Falta Envido (enough to win)")
            print("3. ❌ Decline (opponent gets previous points)")
            max_choice = 3
        elif bet == "Falta Envido":
            print("1. ✅ Accept (play for enough points to win)")
            print("2. ❌ Decline (opponent gets previous points)")
            max_choice = 2
            
        valid_choice = False
        while not valid_choice:
            try:
                choice = int(input("\n🔢 Enter your choice: "))
                if 1 <= choice <= max_choice:
                    if choice == 1:  # Accept
                        print(f"✅ You accept the {bet}!")
                        # Compare Envido points
                        return EnvidoBetting.compare_envido_points(game, bet)
                    elif choice == 2:
                        if bet != "Falta Envido":  # Raise
                            new_bet = "Real Envido" if bet == "Envido" else "Falta Envido"
                            print(f"⬆️ You raise to {new_bet}!")
                            
                            # AI responds to the raise
                            ai_response = EnvidoBetting.ai_respond_to_envido(game, new_bet)
                            
                            if ai_response == "accept" or ai_response == "quiero":
                                print(f"✅ Opponent accepts your {new_bet}!")
                                # Compare Envido points
                                return EnvidoBetting.compare_envido_points(game, new_bet)
                            elif ai_response == "decline":
                                print(f"❌ Opponent declines your {new_bet}!")
                                points = 2 if bet == "Envido" else 3
                                game.teams[0].add_score(points)
                                DisplayUtils.show_celebration(game.teams[0].name, points, True)
                                return True  # End hand early
                        else:  # Decline Falta Envido
                            print("❌ You decline the Falta Envido.")
                            points = 3  # Points from previous Real Envido
                            game.teams[1].add_score(points)
                            DisplayUtils.show_celebration(game.teams[1].name, points, True)
                            return True  # End hand early
                    elif choice == 3:
                        if bet == "Envido":  # Raise to Falta Envido
                            print("🚀 You raise to Falta Envido!")
                            
                            # AI responds to Falta Envido
                            ai_response = EnvidoBetting.ai_respond_to_envido(game, "Falta Envido")
                            
                            if ai_response == "accept" or ai_response == "quiero":
                                print(f"✅ Opponent accepts your Falta Envido!")
                                # Compare Envido points
                                return EnvidoBetting.compare_envido_points(game, "Falta Envido")
                            elif ai_response == "decline":
                                print(f"❌ Opponent declines your Falta Envido!")
                                points = 2  # Points from previous Envido
                                game.teams[0].add_score(points)
                                DisplayUtils.show_celebration(game.teams[0].name, points, True)
                                return True  # End hand early
                        else:  # Decline Real Envido
                            print("❌ You decline the Real Envido.")
                            points = 1  # Points from previous Envido
                            game.teams[1].add_score(points)
                            DisplayUtils.show_celebration(game.teams[1].name, points, True)
                            return True  # End hand early
                    elif choice == 4:  # Decline Envido
                        print("❌ You decline the Envido.")
                        points = 1
                        game.teams[1].add_score(points)
                        DisplayUtils.show_celebration(game.teams[1].name, points, True)
                        return True  # End hand early
                        
                    valid_choice = True
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        return False  # Continue hand
    
    @staticmethod
    def ai_respond_to_envido(game, bet):
        """Determine how AI responds to an Envido bet"""
        # Get a random AI player from team 2
        ai_players = [p for p in game.teams[1].players if not p.is_human]
        if not ai_players:
            return "quiero"  # Fallback
            
        ai_player = random.choice(ai_players)
        
        # Calculate Envido points
        envido_points = ai_player.calculate_envido_points()
        
        # Respond based on Envido points and randomness (for bluffing)
        if bet == "Envido":
            if envido_points > 28 or random.random() < 0.1:  # 10% chance to bluff and raise
                return "raise"
            elif envido_points > 25 or random.random() < 0.6:  # 60% chance to accept with decent points
                return "quiero"
            else:
                return "decline"
        elif bet == "Real Envido":
            if envido_points > 30 or random.random() < 0.05:  # 5% chance to bluff and raise
                return "raise"
            elif envido_points > 27 or random.random() < 0.5:  # 50% chance to accept with good points
                return "quiero"
            else:
                return "decline"
        elif bet == "Falta Envido":
            if envido_points > 31 or random.random() < 0.3:  # 30% chance to accept with strong points
                return "quiero"
            else:
                return "decline"
        
        return "quiero"  # Default fallback
    
    @staticmethod
    def compare_envido_points(game, bet_type="Envido"):
        """Compare Envido points between teams and award score"""
        # Calculate points for each team
        team1_players = game.teams[0].players
        team2_players = game.teams[1].players
        
        team1_points = max(player.calculate_envido_points() for player in team1_players)
        team2_points = max(player.calculate_envido_points() for player in team2_players)
        
        # Display points
        print(f"\n💯 Envido points:")
        print(f"- {game.teams[0].name}: {team1_points}")
        print(f"- {game.teams[1].name}: {team2_points}")
        
        # Determine winner and award points
        if team1_points > team2_points:
            winner = game.teams[0]
            loser = game.teams[1]
        elif team2_points > team1_points:
            winner = game.teams[1]
            loser = game.teams[0]
        else:
            # In case of a tie, the team that did not call Envido wins
            # For simplicity, we'll always give it to team 1 (player's team) in a tie
            print("\n🤝 It's a tie! The dealer's team wins.")
            winner = game.teams[0]
            loser = game.teams[1]
        
        # Award points based on bet type
        if bet_type == "Envido":
            points = 2
        elif bet_type == "Real Envido":
            points = 3
        elif bet_type == "Falta Envido":
            # Calculate points needed to win
            points_to_win = 15 - winner.score
            points = max(3, points_to_win)  # At least 3 points
        else:
            points = 1  # Default
        
        winner.add_score(points)
        print(f"\n🏆 {winner.name} wins the Envido and gets {points} point(s)!")
        DisplayUtils.show_celebration(winner.name, points, True)
        
        return False  # Continue the hand after Envido


# ============== MAIN GAME CLASS ===============

class TrucoGame:
    def __init__(self, num_players=2, envido_enabled=True):
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
        self.envido_enabled = envido_enabled
        self.current_bet = "No bet"
        self.bet_value = 1
        self.round_cards = []
        self.round_winners = []
        
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
        
        DisplayUtils.show_big_message("WELCOME TO ARGENTINIAN TRUCO", "🎮")
        print(f"\n👥 Team setup:")
        print(f"- {self.teams[0].name}: {', '.join(p.name for p in self.teams[0].players)}")
        print(f"- {self.teams[1].name}: {', '.join(p.name for p in self.teams[1].players)}")
        
        # Show tutorial information
        TutorialManager.show_card_ranking_tutorial()
        TutorialManager.show_envido_tutorial()
        
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
        
        DisplayUtils.show_big_message(f"NEW HAND", "🎮")
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
        TutorialManager.show_betting_tutorial()
        
        while not any(team.has_won_game() for team in self.teams):
            self.deal_cards()
            # Wait for player to be ready to start the hand
            input("\n⏸️ Press Enter to start playing this hand...")
            
            # Handle Envido phase first
            if self.envido_phase and self.envido_enabled:
                end_hand = EnvidoBetting.handle_envido_phase(self)
                if end_hand:
                    input("\n⏸️ Press Enter to continue to the next hand...")
                    continue
            
            self.play_hand()
            
            # Check if any team has won
            if any(team.has_won_game() for team in self.teams):
                # Find the winning team
                winning_team = next(team for team in self.teams if team.has_won_game())
                DisplayUtils.show_big_message("GAME OVER", "🎉")
                print(f"\n🏆 {winning_team.name} wins the game with {winning_team.score} points!")
                print(f"\n📊 Final Score: {self.teams[0].name} {self.teams[0].score} - {self.teams[1].score} {self.teams[1].name}")
                break
                
            input("\n⏸️ Press Enter to continue to the next hand...")
            
    def play_hand(self):
        """Play a complete hand (3 rounds)"""
        # Main hand loop
        while len(self.round_winners) < 2 and self.current_round < 3:
            self.current_round += 1
            DisplayUtils.show_big_message(f"ROUND {self.current_round}", "🎯")
            
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
                    end_hand = self.human_turn()
                    if end_hand:
                        return
                else:
                    end_hand = self.ai_turn()
                    if end_hand:
                        return
                
                # Move to next player
                self.current_player_index = (self.current_player_index + 1) % self.num_players
            
            # Determine round winner
            self.determine_round_winner()
            
            # Pause after each round so player can see what happened
            input("\n⏸️ Press Enter to continue...")
            
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
                
                DisplayUtils.show_celebration(winning_team.name, self.bet_value, True)
                break
            
            # If we have a tie (or 1-1-1 situation), play another round
            if len(self.round_winners) == 0 and self.current_round == 3:
                DisplayUtils.show_tie_message()
                break
        
    def human_turn(self):
        """Handle a human player's turn"""
        player = self.players[self.current_player_index]
        
        # First check for betting options
        if self.current_bet == "No bet" and len(player.hand) > 0:
            end_hand = TrucoBetting.handle_truco_betting(self, player)
            if end_hand:
                return True
        
        print(f"\n👤 {player.name}'s turn:")
        print(f"💰 Current bet: {self.current_bet} ({self.bet_value} points)")
        
        if self.round_cards:
            print("\n🎮 Cards played this round:")
            for i, (p, card) in enumerate(self.round_cards):
                print(f"{p.name}: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
        
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
                    print(f"\n🎯 You played: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
                    valid_choice = True
                else:
                    print("❌ Invalid card number. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        return False
    
    def ai_turn(self):
        """Handle an AI player's turn"""
        player = self.players[self.current_player_index]
        
        # Always display human player's hand before AI makes a move
        human_player = next((p for p in self.players if p.is_human), None)
        if human_player and human_player != player:
            print("\n🃏 Your current hand:")
            for i, card_display in enumerate(human_player.get_hand_display()):
                print(card_display)
            
            # Show cards played so far in this round
            if self.round_cards:
                print("\n🎮 Cards played so far this round:")
                for p, card in self.round_cards:
                    print(f"{p.name}: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
        
        # Simple AI strategy
        # If it's the betting phase, sometimes make a bet
        if self.current_bet == "No bet" and random.random() < 0.3:
            end_hand = TrucoBetting.handle_ai_truco_betting(self, player)
            if end_hand:
                return True
        
        # Choose a card (simple strategy)
        if not player.hand:
            return False  # No cards to play
            
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
        
        print(f"\n🤖 {player.name} plays: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
        
        return False
    
    def determine_round_winner(self):
        """Determine the winner of the current round"""
        if not self.round_cards:
            return
            
        # Display all cards played in this round
        print("\n🃏 Cards played this round:")
        for player, card in self.round_cards:
            print(f"{player.name}: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
            
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
            print(f"🃏 Winning card: {winning_card.get_display()} ({CardUtils.get_card_strength_description(winning_card)})")
            
            # Show celebration message
            DisplayUtils.show_celebration(winning_team, 0, False)
        else:
            DisplayUtils.show_tie_message()
            
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


# ============== MAIN FUNCTION ===============

def main():
    DisplayUtils.clear_screen()
    print("🎮 Welcome to Argentinian Truco! 🎮")
    print("\n🎯 This game will teach you the fundamentals of Truco, especially the card values.")
    
    # Choose number of players
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
    
    # Enable Envido?
    print("\n🎮 Envido is a betting feature at the start of each hand.")
    enable_envido = input("Enable Envido? (y/n, default: y): ").lower() != 'n'
    
    # Enter player name
    player_name = input("\n✍️ Enter your name: ")
    if not player_name.strip():
        player_name = "Player"
    
    # Create and start game
    DisplayUtils.clear_screen()
    game = TrucoGame(num_players, enable_envido)
    game.play_game()
    
    print("\n🎉 Thanks for playing Argentinian Truco!")
    print("🔄 Keep practicing and you'll master the card values in no time!")
    print("\n💡 The code is modular and easy to modify. Feel free to enhance it further!")


if __name__ == "__main__":
    main()
