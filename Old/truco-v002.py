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
            
    def get_detailed_description(self):
        """Returns a detailed description of the card including its relative strength"""
        # Special named cards first
        if self.suit == 'Espadas' and self.rank == '1':
            return "1 of Espadas (🗡️) - The BEST card in the game! This is the anchor of any good hand."
        elif self.suit == 'Bastos' and self.rank == '1':
            return "1 of Bastos (🏑) - The 2nd best card. Very powerful and worth keeping."
        elif self.suit == 'Espadas' and self.rank == '7':
            return "7 of Espadas (🗡️) - The 3rd best card. Much stronger than other 7s!"
        elif self.suit == 'Oros' and self.rank == '7':
            return "7 of Oros (🪙) - The 4th best card. Special among 7s!"
        
        # Card categories
        elif self.rank == '3':
            return f"3 of {self.suit} - Very strong card (5th-8th best in game)"
        elif self.rank == '2':
            return f"2 of {self.suit} - Strong card (9th-12th best in game)"
        elif self.rank == '1' and self.suit in ['Oros', 'Copas']:
            return f"1 of {self.suit} - Good card (13th-14th best in game)"
        elif self.rank == 'Rey':
            return f"Rey (King) of {self.suit} - Medium strength (15th-18th best)"
        elif self.rank == 'Caballo':
            return f"Caballo (Knight) of {self.suit} - Medium strength (19th-22nd best)"
        elif self.rank == 'Sota':
            return f"Sota (Jack) of {self.suit} - Medium strength (23rd-26th best)"
        elif self.rank == '7' and self.suit in ['Bastos', 'Copas']:
            return f"7 of {self.suit} - Weak-Medium strength (27th-28th best)"
        elif self.rank == '6':
            return f"6 of {self.suit} - Weak card (29th-32nd best)"
        elif self.rank == '5':
            return f"5 of {self.suit} - Weak card (33rd-36th best)"
        elif self.rank == '4':
            return f"4 of {self.suit} - Weakest card (37th-40th in rank)"
        else:
            return f"{self.rank} of {self.suit}"


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
        
    @staticmethod
    def get_card_rank_explanation():
        """Returns a detailed explanation of card ranking in Truco"""
        explanation = [
            "🃏 CARD RANKING IN ARGENTINIAN TRUCO (from strongest to weakest) 🃏",
            "",
            "⭐⭐⭐ TIER 1: THE SPECIAL FOUR ⭐⭐⭐",
            "1. 1 of Espadas (🗡️) - The most powerful card",
            "2. 1 of Bastos (🏑) - Second most powerful",
            "3. 7 of Espadas (🗡️) - Third most powerful (note: much stronger than other 7s!)",
            "4. 7 of Oros (🪙) - Fourth most powerful (note: much stronger than other 7s!)",
            "",
            "⭐⭐ TIER 2: THE STRONG CARDS ⭐⭐",
            "5-8. All 3s - Very powerful cards",
            "9-12. All 2s - Strong cards",
            "13-14. Other 1s (of Oros and Copas) - Good cards",
            "",
            "⭐ TIER 3: THE MEDIUM CARDS ⭐",
            "15-18. Rey (Kings) - Medium strength",
            "19-22. Caballo (Knights) - Medium strength",
            "23-26. Sota (Jacks) - Medium strength",
            "",
            "⚪ TIER 4: THE WEAK CARDS ⚪",
            "27-28. Other 7s (of Bastos and Copas) - Weak-Medium cards",
            "29-32. All 6s - Weak cards",
            "33-36. All 5s - Weak cards",
            "37-40. All 4s - Weakest cards"
        ]
        return "\n".join(explanation)


class Player:
    def __init__(self, name, is_human=False, personality="normal"):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.team = None
        self.personality = personality  # Could be "aggressive", "cautious", "bluffer", etc.
        
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

    def get_player_names(self):
        """Returns a comma-separated list of player names in this team"""
        return ", ".join(p.name for p in self.players)


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
            
    @staticmethod
    def get_card_value_emoji(value):
        """Returns emoji based on card value from 1-14"""
        if value >= 14:  # 1 of Espadas
            return "🔴"  # Red circle
        elif value >= 13:  # 1 of Bastos
            return "🟠"  # Orange circle
        elif value >= 12:  # 7 of Espadas
            return "🟡"  # Yellow circle
        elif value >= 11:  # 7 of Oros
            return "🟢"  # Green circle
        elif value >= 10:  # 3s
            return "🔵"  # Blue circle
        elif value >= 9:   # 2s
            return "🟣"  # Purple circle
        elif value >= 8:   # 1s (not special)
            return "🟤"  # Brown circle
        elif value >= 7:   # Rey
            return "⚪"  # White circle
        elif value >= 6:   # Caballo
            return "⚫"  # Black circle
        elif value >= 5:   # Sota
            return "🔘"  # Button 
        elif value >= 4:   # Other 7s
            return "◽"  # White small square
        elif value >= 3:   # 6s
            return "◾"  # Black small square
        elif value >= 2:   # 5s
            return "▫️"  # White medium small square
        else:             # 4s
            return "▪️"  # Black medium small square


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
        
        # Get the full explanation
        print(Deck.get_card_rank_explanation())
        
        print("\n🔑 Remember: This ranking is unique to Truco and mastering it is key to success!")
        print("\n💡 During the game, we'll show each card's relative strength to help you learn.")
        print("\n💬 You can use the Card Advisor (type 'help' during your turn) for guidance.")
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
        
    @staticmethod
    def show_verbal_aspect_tutorial():
        """Explain the verbal/psychological aspects of Truco"""
        DisplayUtils.show_big_message("THE ART OF BLUFFING IN TRUCO", "🎭")
        print("\nTruco is as much about psychology as it is about cards:")
        print("\n🗣️ Verbal taunts and bluffs are a huge part of the game")
        print("🃏 Players often bet aggressively with weak hands to trick opponents")
        print("🎭 Reactions when playing cards can mislead others about your hand")
        print("😏 Experienced players develop their own betting and bluffing style")
        print("🤔 Watch for patterns in how opponents bet to guess their strategy")
        print("\n💡 In this version, AI players will have unique personalities and verbal styles")
        print("   Pay attention to their comments - they might reveal their strategy... or not!")
        print("="*60)
        input("\nPress Enter to continue...")
        
    @staticmethod
    def show_help_during_game():
        """Display a brief help message during the game"""
        DisplayUtils.show_big_message("TRUCO HELP", "❓")
        print("\n🃏 Card Ranking (from strongest to weakest):")
        print("1. 1 of Espadas (🗡️) - ⭐⭐⭐")
        print("2. 1 of Bastos (🏑) - ⭐⭐")
        print("3. 7 of Espadas (🗡️) - ⭐")
        print("4. 7 of Oros (🪙) - ✨")
        print("5. 3s - 💪")
        print("6. 2s - 👍")
        print("7. Other 1s - 👌")
        print("8. Face cards - ➖")
        print("9. Other 7s - 🔽")
        print("10. 6s, 5s, 4s - 👎")
        
        print("\n💬 Commands:")
        print("- Type 'help' during your turn for this help menu")
        print("- Type 'advisor' to get advice on which card to play")
        print("- Type 'ranking' to see the full card ranking chart")
        print("- Type 'values' to see your hand with detailed card descriptions")
        print("- Type a number (1-3) to play that card from your hand")
        print("="*60)


# ============== ADVISOR SYSTEM ===============

class CardAdvisor:
    """Provides strategic advice about cards and gameplay"""
    
    @staticmethod
    def analyze_hand(hand):
        """Analyzes a hand of cards and provides general advice"""
        if not hand:
            return "You have no cards left in your hand."
            
        # Sort hand by value (highest to lowest)
        sorted_hand = sorted(hand, key=lambda card: card.value, reverse=True)
        
        # Count cards by tier
        top_tier = sum(1 for card in hand if card.value >= 11)  # Top 4 cards
        high_tier = sum(1 for card in hand if 8 <= card.value < 11)  # 3s, 2s, 1s
        mid_tier = sum(1 for card in hand if 5 <= card.value < 8)  # Face cards
        low_tier = sum(1 for card in hand if card.value < 5)  # 7s, 6s, 5s, 4s
        
        # Provide general advice based on hand strength
        advice = ["🧠 Hand Analysis:"]
        
        # Describe hand in terms of strength
        if top_tier >= 1:
            advice.append(f"- You have {top_tier} top-tier card(s) (one of the 4 strongest cards)")
        if high_tier >= 1:
            advice.append(f"- You have {high_tier} high-tier card(s) (3s, 2s, or 1s)")
        if mid_tier >= 1:
            advice.append(f"- You have {mid_tier} mid-tier card(s) (face cards)")
        if low_tier >= 1:
            advice.append(f"- You have {low_tier} low-tier card(s) (weak numbered cards)")
        
        # Overall strength assessment
        total_strength = sum(card.value for card in hand)
        max_possible = 14 * len(hand)  # If all cards were 1 of Espadas
        strength_percentage = (total_strength / max_possible) * 100
        
        if strength_percentage > 80:
            advice.append("\n💯 This is an extremely strong hand! Consider betting aggressively.")
        elif strength_percentage > 60:
            advice.append("\n💪 This is a very strong hand. Good for betting.")
        elif strength_percentage > 40:
            advice.append("\n👍 This is a decent hand. Be strategic about betting.")
        elif strength_percentage > 20:
            advice.append("\n🤔 This is a below-average hand. Play cautiously.")
        else:
            advice.append("\n😬 This is a weak hand. Consider bluffing or playing defensively.")
            
        return "\n".join(advice)
    
    @staticmethod
    def get_play_advice(hand, round_cards=None, is_first_player=False):
        """Provides advice on which card to play next"""
        if not hand:
            return "You have no cards left to play."
            
        if is_first_player or not round_cards:
            # We're playing first in the round
            advice = ["🧠 Strategy for playing first:"]
            
            # Sort hand by value (highest to lowest)
            sorted_hand = sorted(hand, key=lambda card: card.value, reverse=True)
            
            # Check if we have any top cards
            if sorted_hand[0].value >= 11:  # One of the top 4 cards
                advice.append(f"- You have {sorted_hand[0].get_display()} ({CardUtils.get_card_strength_description(sorted_hand[0])})")
                advice.append("- Playing your strongest card first can intimidate opponents.")
                advice.append(f"- Consider playing card #{hand.index(sorted_hand[0])+1}")
            elif sorted_hand[0].value >= 8:  # Good cards (3s, 2s, 1s)
                advice.append(f"- Your strongest card is {sorted_hand[0].get_display()} ({CardUtils.get_card_strength_description(sorted_hand[0])})")
                advice.append("- Playing a strong card first can help win the round.")
                advice.append(f"- Consider playing card #{hand.index(sorted_hand[0])+1}")
            else:
                # We don't have any strong cards
                advice.append("- You don't have any particularly strong cards.")
                advice.append(f"- Your strongest is {sorted_hand[0].get_display()} ({CardUtils.get_card_strength_description(sorted_hand[0])})")
                advice.append("- Consider playing your weakest card to save stronger ones.")
                advice.append(f"- Consider playing card #{hand.index(sorted_hand[-1])+1}")
                
            return "\n".join(advice)
            
        else:
            # We're responding to cards already played
            advice = ["🧠 Response strategy:"]
            
            # Find the highest card played so far
            highest_card = max((card for _, card in round_cards), key=lambda x: x.value)
            advice.append(f"- Highest card played: {highest_card.get_display()} ({CardUtils.get_card_strength_description(highest_card)})")
            
            # Check if we have any cards that can beat it
            better_cards = [card for card in hand if card.value > highest_card.value]
            if better_cards:
                # Find the lowest card that can still win
                min_winner = min(better_cards, key=lambda x: x.value)
                advice.append(f"- You can win with {min_winner.get_display()} ({CardUtils.get_card_strength_description(min_winner)})")
                advice.append(f"- Consider playing card #{hand.index(min_winner)+1}")
            else:
                # We can't win this round
                advice.append("- You can't beat the highest card played.")
                advice.append("- Consider playing your weakest card to minimize losses.")
                advice.append(f"- Consider playing card #{hand.index(min(hand, key=lambda x: x.value))+1}")
                
            return "\n".join(advice)
    
    @staticmethod
    def get_betting_advice(hand, current_bet="No bet", opponent_called=False):
        """Provides advice on betting strategy"""
        if not hand:
            return "You have no cards left to consider for betting."
            
        # Calculate hand strength
        total_strength = sum(card.value for card in hand)
        max_possible = 14 * len(hand)
        strength_percentage = (total_strength / max_possible) * 100
        
        # Get our strongest card
        strongest_card = max(hand, key=lambda card: card.value)
        
        advice = ["🧠 Betting strategy:"]
        advice.append(f"- Hand strength: {strength_percentage:.1f}%")
        advice.append(f"- Your strongest card: {strongest_card.get_display()} ({CardUtils.get_card_strength_description(strongest_card)})")
        
        if current_bet == "No bet":
            # Should we initiate a bet?
            if strength_percentage > 70 or strongest_card.value >= 12:
                advice.append("\n💯 You have a strong hand. Consider calling Truco.")
            elif strength_percentage > 50 or strongest_card.value >= 10:
                advice.append("\n👍 You have a decent hand. Calling Truco could be advantageous.")
            elif strength_percentage > 30:
                advice.append("\n🤔 You have a medium hand. Calling Truco is risky but could work as a bluff.")
            else:
                advice.append("\n😬 You have a weak hand. Calling Truco would be a pure bluff.")
        elif current_bet == "Truco" and opponent_called:
            # Responding to Truco
            if strength_percentage > 70 or strongest_card.value >= 12:
                advice.append("\n💪 Your hand is strong. Consider raising to Retruco.")
            elif strength_percentage > 50 or strongest_card.value >= 10:
                advice.append("\n✅ Decent hand. Accepting Truco is reasonable.")
            elif strength_percentage > 30:
                advice.append("\n⚖️ Medium hand. Accepting is risky but possible.")
            else:
                advice.append("\n❌ Weak hand. Consider declining unless bluffing.")
        elif current_bet == "Retruco" and opponent_called:
            # Responding to Retruco
            if strength_percentage > 80 or strongest_card.value >= 13:
                advice.append("\n🔥 Very strong hand. Consider raising to Vale Cuatro.")
            elif strength_percentage > 60 or strongest_card.value >= 11:
                advice.append("\n✅ Strong hand. Accepting Retruco is reasonable.")
            else:
                advice.append("\n❌ Not strong enough. Consider declining unless bluffing.")
        elif current_bet == "Vale Cuatro" and opponent_called:
            # Responding to Vale Cuatro
            if strength_percentage > 80 or strongest_card.value >= 13:
                advice.append("\n✅ Very strong hand. Accepting Vale Cuatro could be worth it.")
            else:
                advice.append("\n❌ This is the highest bet. Unless you're very confident, consider declining.")
        
        return "\n".join(advice)
    
    @staticmethod
    def get_envido_advice(hand):
        """Provides advice on Envido strategy"""
        if not hand:
            return "You have no cards to evaluate for Envido."
            
        # Calculate Envido points
        cards_by_suit = {}
        for card in hand:
            if card.suit not in cards_by_suit:
                cards_by_suit[card.suit] = []
            cards_by_suit[card.suit].append(card)
        
        advice = ["🧠 Envido Analysis:"]
        
        # Check each suit
        for suit, cards in cards_by_suit.items():
            if len(cards) >= 2:
                # Calculate points for this suit
                cards.sort(key=lambda c: c.get_envido_value(), reverse=True)
                points = 20 + cards[0].get_envido_value() + cards[1].get_envido_value()
                
                # Display the cards that make up this combination
                card_str = " + ".join([f"{c.get_display()} ({c.get_envido_value()})" for c in cards[:2]])
                
                advice.append(f"- {suit}: {points} points (20 + {card_str})")
            elif len(cards) == 1:
                points = cards[0].get_envido_value()
                advice.append(f"- {suit}: {points} points ({cards[0].get_display()})")
        
        # Determine best suit and points
        best_suit = max(cards_by_suit.items(), key=lambda x: len(x[1]))[0]
        cards_in_best_suit = cards_by_suit[best_suit]
        
        if len(cards_in_best_suit) >= 2:
            cards_in_best_suit.sort(key=lambda c: c.get_envido_value(), reverse=True)
            best_points = 20 + cards_in_best_suit[0].get_envido_value() + cards_in_best_suit[1].get_envido_value()
        else:
            best_points = max(card.get_envido_value() for card in hand)
        
        advice.append(f"\n💯 Your best Envido is {best_points} points")
        
        # Provide strategy advice based on points
        if best_points >= 33:
            advice.append("- Excellent Envido! Consider calling Envido or even Real Envido.")
        elif best_points >= 29:
            advice.append("- Very good Envido. Calling Envido could be advantageous.")
        elif best_points >= 25:
            advice.append("- Decent Envido. You could call, but it's a bit risky.")
        elif best_points >= 20:
            advice.append("- Average Envido. Calling would be risky.")
        else:
            advice.append("- Weak Envido. Better not to call unless bluffing.")
            
        return "\n".join(advice)
    
    @staticmethod
    def show_card_values_detail(hand):
        """Shows detailed information about card values in the hand"""
        if not hand:
            return "You have no cards in your hand."
            
        # Sort hand by value (highest to lowest)
        sorted_hand = sorted(hand, key=lambda card: card.value, reverse=True)
        
        display = ["🃏 Detailed Card Analysis:"]
        
        for i, card in enumerate(sorted_hand):
            value_emoji = CardUtils.get_card_value_emoji(card.value)
            display.append(f"\n{value_emoji} {card.get_detailed_description()}")
            display.append(f"   Value: {card.value}/14 (where 14 is highest possible)")
            
            # Add specific advice for this card
            if card.value >= 11:  # Top 4 cards
                display.append("   💡 Tip: This is one of the 4 best cards! Save it for important rounds.")
            elif card.value >= 8:  # Good cards
                display.append("   💡 Tip: This is a strong card. Use it to win crucial rounds.")
            elif card.value >= 5:  # Medium cards
                display.append("   💡 Tip: Medium strength card. Useful when opponents have played their best cards.")
            else:
                display.append("   💡 Tip: Weak card. Consider using it in early rounds or when you can't win.")
                
        return "\n".join(display)


# ============== VERBAL COMMENTS SYSTEM ===============

class CommentGenerator:
    """Generates verbal comments for AI players based on game state and personality"""
    
    # Different types of comments by category
    TRUCO_CALL = [
        "¡Truco!",
        "TRUCO! What do you say?",
        "Let's make it interesting... Truco!",
        "I'm feeling lucky. Truco!",
        "Time to raise the stakes! Truco!",
        "You don't look so confident. Truco!",
        "Truco! Can you handle it?",
    ]
    
    TRUCO_CALL_CAUTIOUS = [
        "Truco?", 
        "I think... Truco?", 
        "Maybe Truco?"
    ]
    
    TRUCO_CALL_BLUFFER = [
        "TRUCO! (But am I bluffing?)", 
        "Truco! Don't look at my face!"
    ]
    
    RETRUCO_CALL = [
        "¡Retruco!",
        "RETRUCO! Let's see what you've got!",
        "Not enough? Then RETRUCO!",
        "I'm doubling down! Retruco!",
        "Retruco! Getting nervous yet?",
        "Let's turn up the heat! Retruco!",
    ]
    
    VALE_CUATRO_CALL = [
        "¡Vale cuatro!",
        "VALE CUATRO! All in!",
        "Vale Cuatro! No turning back now!",
        "Going all the way! Vale Cuatro!",
        "I'm not bluffing now! VALE CUATRO!",
        "Vale Cuatro! This hand is mine!",
    ]
    
    ACCEPT_BET = [
        "Quiero!",
        "I'm in!",
        "Challenge accepted!",
        "Let's do this!",
        "I'll take that bet!",
        "Game on!",
        "You're on!",
    ]
    
    ACCEPT_BET_AGGRESSIVE = [
        "Quiero! Bring it on!", 
        "Quiero! You're going down!"
    ]
    
    ACCEPT_BET_CAUTIOUS = [
        "Hmm... Quiero, I guess.", 
        "I'll accept, cautiously."
    ]
    
    ACCEPT_BET_BLUFFER = [
        "Quiero! (Was that too eager?)", 
        "Sure, I'll play along."
    ]
    
    DECLINE_BET = [
        "No quiero.",
        "I'll pass this time.",
        "Not worth it.",
        "I'm out.",
        "Take the points, I'm saving for later.",
        "You win this one.",
        "I don't like my chances.",
    ]
    
    DECLINE_BET_CAUTIOUS = [
        "No quiero. Too risky.", 
        "I'll pass on that."
    ]
    
    PLAY_STRONG_CARD = [
        "Take that!",
        "Beat this if you can!",
        "How's this for a card?",
        "Watch and learn!",
        "Got something better?",
        "Top that!",
    ]
    
    PLAY_STRONG_CARD_AGGRESSIVE = [
        "Take THAT!", 
        "BOOM! Try to beat that!"
    ]
    
    PLAY_WEAK_CARD = [
        "Let's see what happens...",
        "Just warming up.",
        "Hmm, not my best...",
        "Saving the good ones for later.",
        "Sometimes you have to lose a battle to win the war.",
        "This isn't my strongest suit.",
    ]
    
    PLAY_WEAK_CARD_BLUFFER = [
        "This should do it!", 
        "Let's see you beat this!"
    ]
    
    BLUFF_COMMENTS = [
        "I've got this hand locked down!",
        "You should probably fold now...",
        "The best cards always seem to find me!",
        "This might be my best hand ever!",
        "Sometimes you just get lucky!",
        "I can see you're getting worried!",
    ]
    
    WIN_COMMENTS = [
        "¡Así se juega!",
        "That's how it's done!",
        "Was there ever any doubt?",
        "Just as I planned!",
        "Did you see that coming?",
        "That's what I'm talking about!",
    ]
    
    LOSE_COMMENTS = [
        "Nicely played!",
        "Hmm, not what I expected.",
        "You got lucky there.",
        "Don't get used to winning.",
        "Enjoy it while it lasts!",
        "I'll remember that move.",
    ]
    
    LOSE_COMMENTS_AGGRESSIVE = [
        "Just luck!", 
        "Don't get cocky!", 
        "This isn't over!"
    ]
    
    ENVIDO_CALL = [
        "¡Envido!",
        "ENVIDO! Let's see those suits!",
        "How about some Envido?",
        "Feeling confident? Envido!",
        "My suits are looking good. Envido!",
    ]
    
    REAL_ENVIDO_CALL = [
        "¡Real Envido!",
        "REAL ENVIDO! This is getting serious!",
        "I'll raise you to Real Envido!",
        "Let's make it Real Envido!",
        "My cards are too good for just Envido. Real Envido!",
    ]
    
    FALTA_ENVIDO_CALL = [
        "¡Falta Envido!",
        "FALTA ENVIDO! All or nothing!",
        "Let's settle this right now! Falta Envido!",
        "I'm going for the win! Falta Envido!",
        "My cards are unbeatable! Falta Envido!",
    ]
    
    @staticmethod
    def get_truco_call(personality="normal"):
        """Get a Truco call comment"""
        if personality == "aggressive":
            return f"🗣️ {random.choice(CommentGenerator.TRUCO_CALL)}"
        elif personality == "cautious":
            return f"🗣️ {random.choice(CommentGenerator.TRUCO_CALL_CAUTIOUS)}"
        elif personality == "bluffer":
            return f"🗣️ {random.choice(CommentGenerator.TRUCO_CALL_BLUFFER)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.TRUCO_CALL)}"
    
    @staticmethod
    def get_retruco_call(personality="normal"):
        """Get a Retruco call comment"""
        if personality == "aggressive":
            return f"🗣️ {random.choice(CommentGenerator.RETRUCO_CALL)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.RETRUCO_CALL)}"
    
    @staticmethod
    def get_vale_cuatro_call(personality="normal"):
        """Get a Vale Cuatro call comment"""
        if personality == "aggressive":
            return f"🗣️ {random.choice(CommentGenerator.VALE_CUATRO_CALL)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.VALE_CUATRO_CALL)}"
    
    @staticmethod
    def get_envido_call(personality="normal"):
        """Get an Envido call comment"""
        return f"🗣️ {random.choice(CommentGenerator.ENVIDO_CALL)}"
    
    @staticmethod
    def get_real_envido_call(personality="normal"):
        """Get a Real Envido call comment"""
        return f"🗣️ {random.choice(CommentGenerator.REAL_ENVIDO_CALL)}"
    
    @staticmethod
    def get_falta_envido_call(personality="normal"):
        """Get a Falta Envido call comment"""
        return f"🗣️ {random.choice(CommentGenerator.FALTA_ENVIDO_CALL)}"
    
    @staticmethod
    def get_accept_comment(personality="normal"):
        """Get a comment for accepting a bet"""
        if personality == "aggressive":
            return f"🗣️ {random.choice(CommentGenerator.ACCEPT_BET_AGGRESSIVE)}"
        elif personality == "cautious":
            return f"🗣️ {random.choice(CommentGenerator.ACCEPT_BET_CAUTIOUS)}"
        elif personality == "bluffer":
            return f"🗣️ {random.choice(CommentGenerator.ACCEPT_BET_BLUFFER)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.ACCEPT_BET)}"
    
    @staticmethod
    def get_decline_comment(personality="normal"):
        """Get a comment for declining a bet"""
        if personality == "cautious":
            return f"🗣️ {random.choice(CommentGenerator.DECLINE_BET_CAUTIOUS)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.DECLINE_BET)}"
    
    @staticmethod
    def get_play_card_comment(card, personality="normal"):
        """Get a comment for playing a card based on its strength"""
        # Determine if this is a strong or weak card
        is_strong = False
        if card.value >= 10 or card.rank in ['1', '2', '3']:  # Top cards and strong number cards
            is_strong = True
        
        if is_strong:
            if personality == "aggressive":
                return f"🗣️ {random.choice(CommentGenerator.PLAY_STRONG_CARD_AGGRESSIVE)}"
            elif personality == "bluffer":
                # Sometimes bluff about strong cards too
                if random.random() < 0.3:
                    return f"🗣️ {random.choice(['Hmm, not great...', 'This might not be enough...'])}"
                else:
                    return f"🗣️ {random.choice(CommentGenerator.PLAY_STRONG_CARD)}"
            else:
                return f"🗣️ {random.choice(CommentGenerator.PLAY_STRONG_CARD)}"
        else:
            if personality == "bluffer" and random.random() < 0.6:
                return f"🗣️ {random.choice(CommentGenerator.PLAY_WEAK_CARD_BLUFFER)}"
            else:
                return f"🗣️ {random.choice(CommentGenerator.PLAY_WEAK_CARD)}"
    
    @staticmethod
    def get_win_comment(personality="normal"):
        """Get a comment for winning a round/hand"""
        return f"🗣️ {random.choice(CommentGenerator.WIN_COMMENTS)}"
    
    @staticmethod
    def get_lose_comment(personality="normal"):
        """Get a comment for losing a round/hand"""
        if personality == "aggressive":
            return f"🗣️ {random.choice(CommentGenerator.LOSE_COMMENTS_AGGRESSIVE)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.LOSE_COMMENTS)}"
    
    @staticmethod
    def get_bluff_comment(personality="normal"):
        """Get a random bluffing comment"""
        if personality == "bluffer":
            return f"🗣️ {random.choice(CommentGenerator.BLUFF_COMMENTS)}"
        else:
            return f"🗣️ {random.choice(CommentGenerator.BLUFF_COMMENTS)}"

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
            
        # Offer advice option
        print("3. 💡 Get betting advice")
        
        valid_choice = False
        while not valid_choice:
            try:
                choice = input("\n💬 Do you want to bet? Enter your choice: ")
                
                # Check for help commands
                if choice.lower() in ['help', 'h', '?']:
                    TutorialManager.show_help_during_game()
                    continue
                elif choice.lower() == 'advisor':
                    print(CardAdvisor.get_play_advice(player.hand, game.round_cards, len(game.round_cards) == 0))
                    continue
                elif choice.lower() == 'values':
                    print(CardAdvisor.show_card_values_detail(player.hand))
                    continue
                elif choice.lower() == 'ranking':
                    print(Deck.get_card_rank_explanation())
                    continue
                
                choice = int(choice)
                
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
                        # Get a random opponent to respond
                        ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                        if ai_player:
                            comment = CommentGenerator.get_accept_comment(ai_player.personality)
                            print(f"{ai_player.name}: {comment}")
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
                            # Get a random opponent to respond
                            ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                            if ai_player:
                                comment = CommentGenerator.get_retruco_call(ai_player.personality)
                                print(f"{ai_player.name}: {comment}")
                            print("⬆️ Opponent raises to Retruco!")
                            # Ask player to accept, raise to Vale Cuatro, or fold
                            TrucoBetting.handle_player_bet_response(game, "Retruco")
                        elif new_bet == "Retruco":
                            # Get a random opponent to respond
                            ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                            if ai_player:
                                comment = CommentGenerator.get_vale_cuatro_call(ai_player.personality)
                                print(f"{ai_player.name}: {comment}")
                            print("⬆️ Opponent raises to Vale Cuatro!")
                            # Ask player to accept or fold
                            TrucoBetting.handle_player_bet_response(game, "Vale Cuatro")
                    elif ai_response == "decline":
                        # Get a random opponent to respond
                        ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                        if ai_player:
                            comment = CommentGenerator.get_decline_comment(ai_player.personality)
                            print(f"{ai_player.name}: {comment}")
                        print("❌ Opponent declines your bet! You win this hand.")
                        
                        game.teams[0].add_score(1 if game.current_bet == "No bet" else game.bet_value)
                        DisplayUtils.show_celebration(game.teams[0].name, 1 if game.current_bet == "No bet" else game.bet_value, True)
                        return True  # Early end to hand
                    
                    valid_choice = True
                elif choice == 3:
                    # Show betting advice
                    advice = CardAdvisor.get_betting_advice(player.hand, game.current_bet)
                    print(f"\n{advice}")
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                if choice.strip():  # Only show error for non-empty input
                    print("❌ Please enter a valid number or command.")
        
        return False  # Continue hand
    
    @staticmethod
    def handle_ai_truco_betting(game, player):
        """Handle AI betting decisions"""
        # Simple AI betting strategy based on hand strength
        hand_strength = sum(card.value for card in player.hand)
        
        # Decide to make a bet based on hand strength and personality
        bluff_threshold = 0.2  # Default bluff probability
        if player.personality == "bluffer":
            bluff_threshold = 0.4  # Bluffers bluff more
        elif player.personality == "cautious":
            bluff_threshold = 0.1  # Cautious players bluff less
        elif player.personality == "aggressive":
            bluff_threshold = 0.3  # Aggressive players bluff more
        
        # Based on hand strength, decide whether to bet
        if hand_strength > 25 or random.random() < bluff_threshold:  # Sometimes bluff
            if game.current_bet == "No bet":
                new_bet = "Truco"
                comment = CommentGenerator.get_truco_call(player.personality)
                print(f"{player.name}: {comment}")
                print(f"\n🤖 {player.name} calls Truco!")
                
                # Ask human to respond
                return TrucoBetting.handle_player_bet_response(game, "Truco", player)
                
            elif game.current_bet == "Truco" and (hand_strength > 30 or random.random() < bluff_threshold/2):
                new_bet = "Retruco"
                comment = CommentGenerator.get_retruco_call(player.personality)
                print(f"{player.name}: {comment}")
                print(f"\n🤖 {player.name} calls Retruco!")
                
                # Ask human to respond
                return TrucoBetting.handle_player_bet_response(game, "Retruco", player)
                
            elif game.current_bet == "Retruco" and (hand_strength > 35 or random.random() < bluff_threshold/3):
                new_bet = "Vale Cuatro"
                comment = CommentGenerator.get_vale_cuatro_call(player.personality)
                print(f"{player.name}: {comment}")
                print(f"\n🤖 {player.name} calls Vale Cuatro!")
                
                # Ask human to respond
                return TrucoBetting.handle_player_bet_response(game, "Vale Cuatro", player)
        
        return False  # Continue hand
    
    @staticmethod
    def handle_player_bet_response(game, bet, betting_player=None):
        """Handle the player's response to an AI bet"""
        print("\n💬 How do you respond?")
        
        if bet == "Truco":
            print("1. ✅ Accept (play for 2 points)")
            print("2. ⬆️ Raise to Retruco (3 points)")
            print("3. ❌ Decline (opponent gets 1 point)")
            print("4. 💡 Get betting advice")
            max_choice = 4
        elif bet == "Retruco":
            print("1. ✅ Accept (play for 3 points)")
            print("2. ⬆️ Raise to Vale Cuatro (4 points)")
            print("3. ❌ Decline (opponent gets 2 points)")
            print("4. 💡 Get betting advice")
            max_choice = 4
        elif bet == "Vale Cuatro":
            print("1. ✅ Accept (play for 4 points)")
            print("2. ❌ Decline (opponent gets 3 points)")
            print("3. 💡 Get betting advice")
            max_choice = 3
            
        # Find the human player
        human_player = next((p for p in game.players if p.is_human), None)
        
        valid_choice = False
        while not valid_choice:
            try:
                choice = input("\n🔢 Enter your choice: ")
                
                # Check for help commands
                if choice.lower() in ['help', 'h', '?']:
                    TutorialManager.show_help_during_game()
                    continue
                elif choice.lower() == 'advisor':
                    print(CardAdvisor.get_play_advice(human_player.hand, game.round_cards, len(game.round_cards) == 0))
                    continue
                elif choice.lower() == 'values':
                    print(CardAdvisor.show_card_values_detail(human_player.hand))
                    continue
                elif choice.lower() == 'ranking':
                    print(Deck.get_card_rank_explanation())
                    continue
                    
                choice = int(choice)
                
                if bet == "Vale Cuatro":
                    # Adjust choice for Vale Cuatro (only 3 options)
                    if choice == 3:
                        # Show betting advice
                        advice = CardAdvisor.get_betting_advice(human_player.hand, bet, True)
                        print(f"\n{advice}")
                        continue
                
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
                            ai_response = TrucoBetting.ai_respond_to_bet(game, new_bet, betting_player)
                            
                            if ai_response == "accept":
                                # Get response from the betting player if available
                                if betting_player:
                                    comment = CommentGenerator.get_accept_comment(betting_player.personality)
                                    print(f"{betting_player.name}: {comment}")
                                print(f"✅ Opponent accepts your {new_bet}!")
                                
                                game.current_bet = new_bet
                                game.bet_value = 3 if new_bet == "Retruco" else 4
                            elif ai_response == "decline":
                                # Get response from the betting player if available
                                if betting_player:
                                    comment = CommentGenerator.get_decline_comment(betting_player.personality)
                                    print(f"{betting_player.name}: {comment}")
                                print(f"❌ Opponent declines your {new_bet}! You win this hand.")
                                
                                game.teams[0].add_score(2 if new_bet == "Retruco" else 3)
                                DisplayUtils.show_celebration(game.teams[0].name, 2 if new_bet == "Retruco" else 3, True)
                                return True  # End hand early
                        else:  # Decline Vale Cuatro
                            print("❌ You decline the Vale Cuatro. Opponent wins this hand.")
                            game.teams[1].add_score(3)  # Opponent team gets 3 points
                            DisplayUtils.show_celebration(game.teams[1].name, 3, True)
                            return True  # End hand early
                    elif choice == 3:
                        if bet != "Vale Cuatro":  # Decline Truco or Retruco
                            print(f"❌ You decline the {bet}. Opponent wins this hand.")
                            points = 1 if bet == "Truco" else (2 if bet == "Retruco" else 3)
                            game.teams[1].add_score(points)
                            DisplayUtils.show_celebration(game.teams[1].name, points, True)
                            return True  # End hand early
                        else:  # Show betting advice for Vale Cuatro
                            advice = CardAdvisor.get_betting_advice(human_player.hand, bet, True)
                            print(f"\n{advice}")
                            continue
                    elif choice == 4:  # Show betting advice
                        advice = CardAdvisor.get_betting_advice(human_player.hand, bet, True)
                        print(f"\n{advice}")
                        continue
                        
                    valid_choice = True
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                if choice.strip():  # Only show error for non-empty input
                    print("❌ Please enter a valid number or command.")
        
        return False  # Continue hand
    
    @staticmethod
    def ai_respond_to_bet(game, bet, original_better=None):
        """Determine how AI responds to a bet"""
        # Get a random AI player from team 2
        ai_players = [p for p in game.teams[1].players if not p.is_human]
        if not ai_players:
            return "accept"  # Fallback
            
        # If we know who made the original bet, prioritize them for responding
        if original_better and original_better in ai_players:
            ai_player = original_better
        else:
            ai_player = random.choice(ai_players)
        
        # Calculate hand strength
        hand_strength = sum(card.value for card in ai_player.hand)
        
        # Adjust thresholds based on personality
        raise_threshold = 0.1  # Default raise probability
        accept_threshold = 0.7  # Default accept probability
        
        if ai_player.personality == "aggressive":
            raise_threshold = 0.25
            accept_threshold = 0.8
        elif ai_player.personality == "cautious":
            raise_threshold = 0.05
            accept_threshold = 0.6
        elif ai_player.personality == "bluffer":
            raise_threshold = 0.15
            accept_threshold = 0.75
        
        # Respond based on hand strength and randomness (for bluffing)
        if bet == "Truco":
            if hand_strength > 25 or random.random() < raise_threshold:  # chance to bluff and raise
                return "raise"
            elif hand_strength > 20 or random.random() < accept_threshold:  # chance to accept with medium hand
                return "accept"
            else:
                return "decline"
        elif bet == "Retruco":
            if hand_strength > 30 or random.random() < raise_threshold/2:  # chance to bluff and raise
                return "raise"
            elif hand_strength > 25 or random.random() < accept_threshold-0.1:  # chance to accept with good hand
                return "accept"
            else:
                return "decline"
        elif bet == "Vale Cuatro":
            if hand_strength > 30 or random.random() < accept_threshold-0.2:  # chance to accept with strong hand
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
            
            # Determine bluffing probability based on personality
            bluff_threshold = 0.3  # Default probability
            if ai_player.personality == "bluffer":
                bluff_threshold = 0.5
            elif ai_player.personality == "cautious":
                bluff_threshold = 0.15
            elif ai_player.personality == "aggressive":
                bluff_threshold = 0.4
                
            # AI is more likely to call Envido with higher points
            if ai_points > 25 or random.random() < bluff_threshold:  # 30% chance to bluff
                comment = CommentGenerator.get_envido_call(ai_player.personality)
                print(f"{ai_player.name}: {comment}")
                print(f"\n🤖 {ai_player.name} calls Envido!")
                ai_called_envido = True
                return EnvidoBetting.handle_player_envido_response(game, "Envido", ai_player)
        
        if not ai_called_envido:
            # Ask human if they want to call Envido
            print("\n💰 Envido options:")
            print("1. ➡️ Continue without calling Envido")
            print("2. 🎲 Call Envido (2 points)")
            print("3. 💡 Get Envido advice")
            
            valid_choice = False
            while not valid_choice:
                try:
                    choice = input("\n💬 Do you want to call Envido? Enter your choice: ")
                    
                    # Check for help commands
                    if choice.lower() in ['help', 'h', '?']:
                        TutorialManager.show_help_during_game()
                        continue
                    elif choice.lower() == 'advisor':
                        print(CardAdvisor.get_play_advice(human_player.hand, game.round_cards, len(game.round_cards) == 0))
                        continue
                    elif choice.lower() == 'values':
                        print(CardAdvisor.show_card_values_detail(human_player.hand))
                        continue
                    elif choice.lower() == 'ranking':
                        print(Deck.get_card_rank_explanation())
                        continue
                        
                    choice = int(choice)
                    
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
                            # Get a random AI player to respond
                            ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                            if ai_player:
                                comment = CommentGenerator.get_accept_comment(ai_player.personality)
                                print(f"{ai_player.name}: {comment}")
                            print("✅ Opponent accepts your Envido!")
                            # Compare Envido points
                            return EnvidoBetting.compare_envido_points(game)
                            
                        elif ai_response == "quiero":
                            # Get a random AI player to respond
                            ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                            if ai_player:
                                comment = CommentGenerator.get_accept_comment(ai_player.personality)
                                print(f"{ai_player.name}: {comment}")
                            print("🎯 Opponent says 'Quiero'!")
                            # Compare Envido points
                            return EnvidoBetting.compare_envido_points(game)
                            
                        elif ai_response == "raise":
                            # Get a random AI player to respond
                            ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                            if ai_player:
                                comment = CommentGenerator.get_real_envido_call(ai_player.personality)
                                print(f"{ai_player.name}: {comment}")
                            print("⬆️ Opponent raises to Real Envido!")
                            # Ask player to accept, raise to Falta Envido, or decline
                            return EnvidoBetting.handle_player_envido_response(game, "Real Envido", ai_player)
                            
                        elif ai_response == "decline":
                            # Get a random AI player to respond
                            ai_player = next((p for p in game.teams[1].players if not p.is_human), None)
                            if ai_player:
                                comment = CommentGenerator.get_decline_comment(ai_player.personality)
                                print(f"{ai_player.name}: {comment}")
                            print("❌ Opponent declines your Envido! You win 1 point.")
                            
                            game.teams[0].add_score(1)
                            DisplayUtils.show_celebration(game.teams[0].name, 1, True)
                            return True  # End hand early
                        
                        valid_choice = True
                    elif choice == 3:
                        # Show Envido advice
                        advice = CardAdvisor.get_envido_advice(human_player.hand)
                        print(f"\n{advice}")
                    else:
                        print("❌ Invalid choice. Please try again.")
                except ValueError:
                    if choice.strip():  # Only show error for non-empty input
                        print("❌ Please enter a valid number or command.")
        
        return False  # Continue hand
    
    @staticmethod
    def handle_player_envido_response(game, bet, betting_player=None):
        """Handle the player's response to an AI Envido bet"""
        print("\n💬 How do you respond to the Envido?")
        
        # Find the human player
        human_player = next((p for p in game.players if p.is_human), None)
        
        if bet == "Envido":
            print("1. ✅ Accept (play for 2 points)")
            print("2. ⬆️ Raise to Real Envido (3 more points)")
            print("3. 🚀 Raise to Falta Envido (enough to win)")
            print("4. ❌ Decline (opponent gets 1 point)")
            print("5. 💡 Get Envido advice")
            max_choice = 5
        elif bet == "Real Envido":
            print("1. ✅ Accept (play for 3 more points)")
            print("2. 🚀 Raise to Falta Envido (enough to win)")
            print("3. ❌ Decline (opponent gets previous points)")
            print("4. 💡 Get Envido advice")
            max_choice = 4
        elif bet == "Falta Envido":
            print("1. ✅ Accept (play for enough points to win)")
            print("2. ❌ Decline (opponent gets previous points)")
            print("3. 💡 Get Envido advice")
            max_choice = 3
            
        valid_choice = False
        while not valid_choice:
            try:
                choice = input("\n🔢 Enter your choice: ")
                
                # Check for help commands
                if choice.lower() in ['help', 'h', '?']:
                    TutorialManager.show_help_during_game()
                    continue
                elif choice.lower() == 'advisor':
                    print(CardAdvisor.get_play_advice(human_player.hand, game.round_cards, len(game.round_cards) == 0))
                    continue
                elif choice.lower() == 'values':
                    print(CardAdvisor.show_card_values_detail(human_player.hand))
                    continue
                elif choice.lower() == 'ranking':
                    print(Deck.get_card_rank_explanation())
                    continue
                
                choice = int(choice)
                
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
                            ai_response = EnvidoBetting.ai_respond_to_envido(game, new_bet, betting_player)
                            
                            if ai_response == "accept" or ai_response == "quiero":
                                # Get response from the betting player if available
                                if betting_player:
                                    comment = CommentGenerator.get_accept_comment(betting_player.personality)
                                    print(f"{betting_player.name}: {comment}")
                                print(f"✅ Opponent accepts your {new_bet}!")
                                
                                # Compare Envido points
                                return EnvidoBetting.compare_envido_points(game, new_bet)
                            elif ai_response == "decline":
                                # Get response from the betting player if available
                                if betting_player:
                                    comment = CommentGenerator.get_decline_comment(betting_player.personality)
                                    print(f"{betting_player.name}: {comment}")
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
                            ai_response = EnvidoBetting.ai_respond_to_envido(game, "Falta Envido", betting_player)
                            
                            if ai_response == "accept" or ai_response == "quiero":
                                # Get response from the betting player if available
                                if betting_player:
                                    comment = CommentGenerator.get_accept_comment(betting_player.personality)
                                    print(f"{betting_player.name}: {comment}")
                                print(f"✅ Opponent accepts your Falta Envido!")
                                
                                # Compare Envido points
                                return EnvidoBetting.compare_envido_points(game, "Falta Envido")
                            elif ai_response == "decline":
                                # Get response from the betting player if available
                                if betting_player:
                                    comment = CommentGenerator.get_decline_comment(betting_player.personality)
                                    print(f"{betting_player.name}: {comment}")
                                print(f"❌ Opponent declines your Falta Envido!")
                                
                                points = 2  # Points from previous Envido
                                game.teams[0].add_score(points)
                                DisplayUtils.show_celebration(game.teams[0].name, points, True)
                                return True  # End hand early
                        elif bet == "Real Envido":  # Decline Real Envido
                            print("❌ You decline the Real Envido.")
                            points = 1  # Points from previous Envido
                            game.teams[1].add_score(points)
                            DisplayUtils.show_celebration(game.teams[1].name, points, True)
                            return True  # End hand early
                        else:  # Get Envido advice
                            advice = CardAdvisor.get_envido_advice(human_player.hand)
                            print(f"\n{advice}")
                            continue
                    elif choice == 4:
                        if bet == "Envido":  # Decline Envido
                            print("❌ You decline the Envido.")
                            points = 1
                            game.teams[1].add_score(points)
                            DisplayUtils.show_celebration(game.teams[1].name, points, True)
                            return True  # End hand early
                        else:  # Get Envido advice
                            advice = CardAdvisor.get_envido_advice(human_player.hand)
                            print(f"\n{advice}")
                            continue
                    elif choice == 5:  # Get Envido advice
                        advice = CardAdvisor.get_envido_advice(human_player.hand)
                        print(f"\n{advice}")
                        continue
                        
                    valid_choice = True
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                if choice.strip():  # Only show error for non-empty input
                    print("❌ Please enter a valid number or command.")
        
        return False  # Continue hand
    
    @staticmethod
    def ai_respond_to_envido(game, bet, original_better=None):
        """Determine how AI responds to an Envido bet"""
        # Get a random AI player from team 2
        ai_players = [p for p in game.teams[1].players if not p.is_human]
        if not ai_players:
            return "quiero"  # Fallback
            
        # If we know who made the original bet, prioritize them for responding
        if original_better and original_better in ai_players:
            ai_player = original_better
        else:
            ai_player = random.choice(ai_players)
        
        # Calculate Envido points
        envido_points = ai_player.calculate_envido_points()
        
        # Adjust thresholds based on personality
        raise_threshold = 0.1  # Default raise probability
        accept_threshold = 0.6  # Default accept probability
        
        if ai_player.personality == "aggressive":
            raise_threshold = 0.2
            accept_threshold = 0.7
        elif ai_player.personality == "cautious":
            raise_threshold = 0.05
            accept_threshold = 0.5
        elif ai_player.personality == "bluffer":
            raise_threshold = 0.15
            accept_threshold = 0.65
        
        # Respond based on Envido points and randomness (for bluffing)
        if bet == "Envido":
            if envido_points > 28 or random.random() < raise_threshold:  # 10% chance to bluff and raise
                return "raise"
            elif envido_points > 25 or random.random() < accept_threshold:  # 60% chance to accept with decent points
                return "quiero"
            else:
                return "decline"
        elif bet == "Real Envido":
            if envido_points > 30 or random.random() < raise_threshold/2:  # 5% chance to bluff and raise
                return "raise"
            elif envido_points > 27 or random.random() < accept_threshold-0.1:  # 50% chance to accept with good points
                return "quiero"
            else:
                return "decline"
        elif bet == "Falta Envido":
            if envido_points > 31 or random.random() < accept_threshold-0.3:  # 30% chance to accept with strong points
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
            
            # Add a celebration comment from a human player
            human_player = next((p for p in team1_players if p.is_human), None)
            if human_player:
                print(f"{human_player.name}: 🗣️ My Envido is better! {team1_points}!")
                
            # Add a losing comment from an AI player
            ai_player = next((p for p in team2_players if not p.is_human), None)
            if ai_player:
                comment = CommentGenerator.get_lose_comment(ai_player.personality)
                print(f"{ai_player.name}: {comment}")
                
        elif team2_points > team1_points:
            winner = game.teams[1]
            loser = game.teams[0]
            
            # Add a celebration comment from an AI player
            ai_player = next((p for p in team2_players if not p.is_human), None)
            if ai_player:
                comment = CommentGenerator.get_win_comment(ai_player.personality)
                print(f"{ai_player.name}: {comment}")
                
            # Add a losing comment from a human player
            human_player = next((p for p in team1_players if p.is_human), None)
            if human_player:
                print(f"{human_player.name}: 🗣️ You got me on the Envido this time...")
                
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
    def __init__(self, num_players=2, envido_enabled=True, advisor_enabled=True):
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
        self.advisor_enabled = advisor_enabled
        self.current_bet = "No bet"
        self.bet_value = 1
        self.round_cards = []
        self.round_winners = []
        
    def setup_game(self, player_name="Player", ai_names=None, tutorial_level="full"):
        """Initialize the game with players and teams"""
        # Create players
        team_size = self.num_players // 2  # Either 1, 2, or 3 players per team
        
        # Create human player
        human_player = Player(player_name, is_human=True)
        self.players.append(human_player)
        
        # If AI names weren't provided, use defaults
        if not ai_names:
            ai_names = [f"AI Player {i}" for i in range(1, self.num_players)]
        else:
            # Make sure we have enough names
            while len(ai_names) < self.num_players - 1:
                ai_names.append(f"AI Player {len(ai_names) + 1}")
        
        # Create AI players with different personalities
        personalities = ["aggressive", "cautious", "bluffer", "normal"]
        for i in range(1, self.num_players):
            personality = random.choice(personalities)
            ai_player = Player(ai_names[i-1], is_human=False, personality=personality)
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
        print(f"- {self.teams[0].name}: {self.teams[0].get_player_names()}")
        print(f"- {self.teams[1].name}: {self.teams[1].get_player_names()}")
        
        # Show AI personalities
        print("\n🎭 AI Player Personalities:")
        for player in self.players:
            if not player.is_human:
                personality_emoji = {
                    "aggressive": "😈", 
                    "cautious": "🤔", 
                    "bluffer": "😏", 
                    "normal": "😐"
                }.get(player.personality, "😐")
                print(f"- {player.name}: {personality_emoji} {player.personality.capitalize()}")
        
        # Show tutorial information based on level
        if tutorial_level in ["full", "basic", "minimal"]:
            TutorialManager.show_card_ranking_tutorial()
            
        if tutorial_level in ["full", "basic"]:
            TutorialManager.show_betting_tutorial()
            
        if tutorial_level == "full":
            TutorialManager.show_envido_tutorial()
            TutorialManager.show_verbal_aspect_tutorial()
            
        # Show advisor information if enabled
        if self.advisor_enabled:
            DisplayUtils.show_big_message("CARD VALUE ADVISOR ENABLED", "💡")
            print("\nThe Card Value Advisor is here to help you learn Truco!")
            print("During your turn, you can use these commands:")
            print("- Type 'help' for a quick reference guide")
            print("- Type 'advisor' for advice on which card to play")
            print("- Type 'values' to see detailed information about your cards")
            print("- Type 'ranking' to see the full card ranking chart")
            print("\nYou can also get specific advice during betting phases.")
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
                
            # If advisor is enabled, provide hand analysis
            if self.advisor_enabled:
                print("\n" + CardAdvisor.analyze_hand(human_player.hand))
            
            # Add a random comment from an AI player at the start of a new hand
            ai_player = next((p for p in self.players if not p.is_human), None)
            if ai_player and random.random() < 0.7:  # 70% chance for a comment
                # Different comments based on the score situation
                if self.teams[0].score > self.teams[1].score:
                    comments = [
                        "Time to catch up!",
                        "You won't be ahead for long!",
                        "Let's see if your luck continues...",
                        "Don't get too confident!",
                    ]
                elif self.teams[0].score < self.teams[1].score:
                    comments = [
                        "I'm feeling good about this hand!",
                        "We're on a roll now!",
                        "Try to keep up, will you?",
                        "This game is ours!",
                    ]
                else:  # Tied score
                    comments = [
                        "Time to break this tie!",
                        "Let's see who takes the lead!",
                        "May the best team win!",
                        "This hand will be decisive!",
                    ]
                
                print(f"\n{ai_player.name}: 🗣️ {random.choice(comments)}")
        
    def play_game(self):
        """Main game loop"""
        self.setup_game()
        
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
                
                # Add celebration comment from winning team
                if winning_team == self.teams[0]:
                    human_player = next((p for p in self.teams[0].players if p.is_human), None)
                    if human_player:
                        print(f"\n{human_player.name}: 🗣️ What a game! We did it!")
                else:
                    ai_player = next((p for p in self.teams[1].players if not p.is_human), None)
                    if ai_player:
                        comments = [
                            "Better luck next time!",
                            "That was a good game! Thanks for playing!",
                            "We make a great team!",
                            "That's how it's done in Argentina!",
                            "Victory is sweet!",
                        ]
                        print(f"\n{ai_player.name}: 🗣️ {random.choice(comments)}")
                break
                
            input("\n⏸️ Press Enter to continue to the next hand...")
    

    def play_hand(self):
        """Play a complete hand (3 rounds)"""
        # Main hand loop - always play up to 3 rounds unless someone wins 2 rounds early
        round_to_play = 3  # Always play up to 3 rounds to complete the hand
        
        for _ in range(round_to_play):
            if self.current_round >= 3:
                break  # Don't play more than 3 rounds
                
            self.current_round += 1
            DisplayUtils.show_big_message(f"ROUND {self.current_round}", "🎯")
            
            # Always display human player's hand at the beginning of each round
            human_player = next((p for p in self.players if p.is_human), None)
            if human_player:
                print("\n🃏 Your Current Hand:")
                for i, card_display in enumerate(human_player.get_hand_display()):
                    print(card_display)
                
                # If advisor is enabled, provide round-specific advice
                if self.advisor_enabled and self.current_round > 1:
                    is_first_player = len(self.round_cards) == 0
                    advice = CardAdvisor.get_play_advice(human_player.hand, self.round_cards, is_first_player)
                    print(f"\n{advice}")
            
            self.round_cards = []
            
            # Each player plays one card
            for _ in range(self.num_players):
                current_player = self.players[self.current_player_index]
                
                if current_player.is_human:
                    end_hand = self.human_turn()
                    if end_hand:
                        return  # Early end due to betting decline
                else:
                    end_hand = self.ai_turn()
                    if end_hand:
                        return  # Early end due to betting decline
                
                # Move to next player
                self.current_player_index = (self.current_player_index + 1) % self.num_players
            
            # Determine round winner
            self.determine_round_winner()
            
            # Pause after each round so player can see what happened
            if self.current_round < 3:
                input("\n⏸️ Press Enter to continue...")
            
            # Check if a team has already won 2 rounds (early victory)
            winning_team = self.get_winning_team()
            if winning_team:
                winning_team.add_score(self.bet_value)
                
                # Add celebration comments from winning team
                if winning_team == self.teams[0]:
                    human_player = next((p for p in self.teams[0].players if p.is_human), None)
                    if human_player:
                        celebration_comments = [
                            "That's how it's done!",
                            "Great hand, team!",
                            "We played that perfectly!",
                            "That's what I'm talking about!",
                            "Let's keep this momentum going!",
                        ]
                        print(f"\n{human_player.name}: 🗣️ {random.choice(celebration_comments)}")
                else:
                    ai_player = next((p for p in self.teams[1].players if not p.is_human), None)
                    if ai_player:
                        comment = CommentGenerator.get_win_comment(ai_player.personality)
                        print(f"\n{ai_player.name}: {comment}")
                
                DisplayUtils.show_celebration(winning_team.name, self.bet_value, True)
                break
        
        # After all rounds are played or a team has won early, determine the final result
        # This handles cases where we've played all 3 rounds but no team won 2 rounds
        if self.current_round == 3 and not self.get_winning_team():
            # Handle tie situations
            team1_wins = sum(1 for winner in self.round_winners if winner in self.teams[0].players)
            team2_wins = sum(1 for winner in self.round_winners if winner in self.teams[1].players)
            
            if team1_wins == team2_wins:
                # It's a complete tie, no points awarded
                DisplayUtils.show_tie_message()
                print("\nThe hand ends in a tie! No points awarded.")
            elif team1_wins > team2_wins:
                # Team 1 won more rounds (1-0-2 or 2-1-0)
                self.teams[0].add_score(self.bet_value)
                DisplayUtils.show_celebration(self.teams[0].name, self.bet_value, True)
            else:
                # Team 2 won more rounds (0-1-2 or 1-2-0)
                self.teams[1].add_score(self.bet_value)
                DisplayUtils.show_celebration(self.teams[1].name, self.bet_value, True)

    # Fix for the get_winning_team method to properly determine when a team has won the hand
    def get_winning_team(self):
        """Determine if there's a winning team based on round winners
        A team needs to win at least 2 rounds to win the hand"""
        
        # Count how many times each team won
        team_wins = {team: 0 for team in self.teams}
        
        for winner in self.round_winners:
            for team in self.teams:
                if winner in team.players:
                    team_wins[team] += 1
        
        # A team needs to win at least 2 rounds to win the hand
        for team, wins in team_wins.items():
            if wins >= 2:
                return team
                
        # No team has won 2 rounds yet
        return None
        
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
        
        # If advisor is enabled, provide a hint
        if self.advisor_enabled:
            is_first_player = len(self.round_cards) == 0
            print("\nType 'help' for commands, 'advisor' for play advice, or a number to play a card.")
        
        valid_choice = False
        while not valid_choice:
            try:
                choice = input("\n🤔 Which card do you want to play? (Enter the number or command): ")
                
                # Check for help commands
                if choice.lower() in ['help', 'h', '?']:
                    TutorialManager.show_help_during_game()
                    continue
                elif choice.lower() == 'advisor':
                    print(CardAdvisor.get_play_advice(player.hand, self.round_cards, len(self.round_cards) == 0))
                    continue
                elif choice.lower() == 'values':
                    print(CardAdvisor.show_card_values_detail(player.hand))
                    continue
                elif choice.lower() == 'ranking':
                    print(Deck.get_card_rank_explanation())
                    continue
                
                card_index = int(choice) - 1  # Convert to 0-based index
                
                if 0 <= card_index < len(player.hand):
                    card = player.play_card(card_index)
                    self.round_cards.append((player, card))
                    print(f"\n🎯 You played: {card.get_display()} ({CardUtils.get_card_strength_description(card)})")
                    
                    # Add a verbal comment that matches the card's strength
                    is_strong = False
                    if card.value >= 10 or card.rank in ['1', '2', '3']:  # Top cards and strong number cards
                        is_strong = True
                        
                    if is_strong:
                        comments = [
                            "Take that!",
                            "Beat this if you can!",
                            "How's this for a card?",
                            "Watch and learn!",
                            "This should do the trick!",
                        ]
                        print(f"{player.name}: 🗣️ {random.choice(comments)}")
                    elif random.random() < 0.4:  # 40% chance to bluff with a weak card
                        comments = [
                            "I've got this round secured!",
                            "Let's see you top that!",
                            "I'm feeling good about this play!",
                            "The best card at the perfect time!",
                        ]
                        print(f"{player.name}: 🗣️ {random.choice(comments)}")
                    
                    valid_choice = True
                else:
                    print("❌ Invalid card number. Please try again.")
            except ValueError:
                if choice.strip() and not choice.lower() in ['help', 'h', '?', 'advisor', 'values', 'ranking']:
                    # Only show error for non-empty, non-command input
                    print("❌ Please enter a valid number or command.")
        
        return False
    
    def ai_turn(self):
        """Handle an AI player's turn"""
        player = self.players[self.current_player_index]
        
        # Always display human player's hand before AI makes a move
        human_player = next((p for p in self.players if p.is_human), None)
        if human_player and human_player != player and human_player.hand:
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
        
        # Add a verbal comment based on the card played and personality
        comment = CommentGenerator.get_play_card_comment(card, player.personality)
        print(f"{player.name}: {comment}")
        
        # Add occasional random bluffing comment
        if player.personality == "bluffer" and random.random() < 0.3:
            bluff_comment = CommentGenerator.get_bluff_comment()
            print(f"{player.name}: {bluff_comment}")
        
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
            winning_team = self.teams[0] if winner in self.teams[0].players else self.teams[1]
            
            winning_card = next(card for p, card in self.round_cards if p == winner)
            print(f"\n🏆 {winner.name} wins round {self.current_round} for {winning_team.name}!")
            print(f"🃏 Winning card: {winning_card.get_display()} ({CardUtils.get_card_strength_description(winning_card)})")
            
            # Highlight why this card won (for educational purposes)
            if self.advisor_enabled:
                print(f"\n💡 Learning Point: {winning_card.get_display()} won because:")
                print(f"   - Card value: {winning_card.value}/14 (higher is better)")
                print(f"   - {winning_card.get_detailed_description()}")
            
            # Add victory/defeat comments
            if winner.is_human:
                # Human player wins
                comments = [
                    "Got it!",
                    "That's how it's done!",
                    "Perfect timing!",
                    "Just as I planned!",
                ]
                print(f"{winner.name}: 🗣️ {random.choice(comments)}")
                
                # AI player loses
                losing_player = next((p for p, _ in self.round_cards if p != winner and not p.is_human), None)
                if losing_player:
                    comment = CommentGenerator.get_lose_comment(losing_player.personality)
                    print(f"{losing_player.name}: {comment}")
            else:
                # AI player wins
                comment = CommentGenerator.get_win_comment(winner.personality)
                print(f"{winner.name}: {comment}")
                
                # Human player loses
                losing_player = next((p for p, _ in self.round_cards if p != winner and p.is_human), None)
                if losing_player:
                    comments = [
                        "Nice play.",
                        "You got me there.",
                        "I'll get you in the next round.",
                        "Well played.",
                    ]
                    print(f"{losing_player.name}: 🗣️ {random.choice(comments)}")
            
            # Show celebration message
            DisplayUtils.show_celebration(winning_team.name, 0, False)
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
                
            # If advisor is enabled and this isn't the last round, provide advice
            if self.advisor_enabled and self.current_round < 3 and len(human_player.hand) > 0:
                advice = CardAdvisor.analyze_hand(human_player.hand)
                print(f"\n{advice}")


# ============== MAIN FUNCTION ===============

def main():
    DisplayUtils.clear_screen()
    print("🎮 Welcome to Argentinian Truco! 🎮")
    print("\n🎯 This game will teach you the fundamentals of Truco, especially the card values.")
    print("The Card Value Advisor will help you learn and master the game.")
    
    # Choose number of players
    while True:
        print("\n👥 Select number of players:")
        print("1. 👤 vs 🤖 (2 players, 1 vs 1)")
        print("2. 👥 vs 🤖🤖 (4 players, 2 vs 2)")
        print("3. 👥👥 vs 🤖🤖🤖 (6 players, 3 vs 3)")
        
        try:
            choice = input("\n🔢 Enter your choice (1-3): ")
            if choice.isdigit() and 1 <= int(choice) <= 3:
                num_players = int(choice) * 2
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Enable Envido?
    print("\n🎮 Envido is a betting feature at the start of each hand.")
    enable_envido = input("Enable Envido? (y/n, default: y): ").lower() != 'n'
    
    # Enable Card Advisor?
    print("\n💡 The Card Value Advisor helps you learn the game by providing tips and strategic advice.")
    enable_advisor = input("Enable Card Value Advisor? (y/n, default: y): ").lower() != 'n'
    
    # Choose tutorial level
    print("\n📚 Choose tutorial level:")
    print("1. Full - Complete explanation of rules, card values, and strategy")
    print("2. Basic - Quick overview of essential rules and card values")
    print("3. Minimal - Just the card ranking, for experienced players")
    
    tutorial_level = "full"
    while True:
        try:
            level_choice = input("\n🔢 Enter your choice (1-3, default: 1): ")
            if not level_choice:
                break  # Use default
            level_choice = int(level_choice)
            if 1 <= level_choice <= 3:
                tutorial_level = ["full", "basic", "minimal"][level_choice-1]
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Enter player name
    player_name = input("\n✍️ Enter your name: ")
    if not player_name.strip():
        player_name = "Player"
    
    # Enter AI opponent names (optional)
    print("\n✍️ Enter names for your AI opponents (or press Enter for default names)")
    print("   Note: Spanish/Argentinian names add to the atmosphere!")
    ai_names = []
    for i in range(1, num_players):
        ai_name = input(f"AI Player {i}: ")
        if ai_name.strip():
            ai_names.append(ai_name)
        else:
            ai_names.append(f"AI Player {i}")
    
    # Create and start game
    DisplayUtils.clear_screen()
    game = TrucoGame(num_players, enable_envido, enable_advisor)
    game.setup_game(player_name, ai_names, tutorial_level)
    game.play_game()
    
    print("\n🎉 Thanks for playing Argentinian Truco!")
    print("🔄 Keep practicing and you'll master the card values in no time!")
    print("\n💡 Did the Card Value Advisor help you learn? We hope so!")


if __name__ == "__main__":
    main()