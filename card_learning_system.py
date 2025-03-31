"""
Card Learning System for Argentinian Truco
A supplementary module that provides interactive card value learning features
"""

import os
import random
import time
from typing import List, Dict, Any, Optional


class TrucoCardTrainer:
    """A learning system to help beginners memorize Argentinian Truco card values"""
    
    def __init__(self, display_manager=None):
        self.display_manager = display_manager
        self.card_tiers = {
            "top": [
                {"suit": "Espadas", "rank": "1", "description": "Highest card in the game (Macho)"},
                {"suit": "Bastos", "rank": "1", "description": "Second highest card"},
                {"suit": "Espadas", "rank": "7", "description": "Third highest card"},
                {"suit": "Oros", "rank": "7", "description": "Fourth highest card"}
            ],
            "strong": [
                {"suit": "Any", "rank": "3", "description": "All 3s are strong (5th-8th rank)"},
                {"suit": "Any", "rank": "2", "description": "All 2s are strong (9th-12th rank)"},
                {"suit": "Oros", "rank": "1", "description": "Regular 1s (13th-14th rank)"},
                {"suit": "Copas", "rank": "1", "description": "Regular 1s (13th-14th rank)"}
            ],
            "medium": [
                {"suit": "Any", "rank": "Rey", "description": "All Kings are medium strength (15th-18th)"},
                {"suit": "Any", "rank": "Caballo", "description": "All Knights are medium strength (19th-22nd)"},
                {"suit": "Any", "rank": "Sota", "description": "All Jacks are medium strength (23rd-26th)"}
            ],
            "weak": [
                {"suit": "Bastos", "rank": "7", "description": "Other 7s are weak (27th-28th)"},
                {"suit": "Copas", "rank": "7", "description": "Other 7s are weak (27th-28th)"},
                {"suit": "Any", "rank": "6", "description": "All 6s are weak (29th-32nd)"},
                {"suit": "Any", "rank": "5", "description": "All 5s are weak (33rd-36th)"},
                {"suit": "Any", "rank": "4", "description": "All 4s are weakest (37th-40th)"}
            ]
        }
        self.suit_symbols = {
            'Espadas': '🗡️',  # Sword
            'Bastos': '🏑',   # Club
            'Oros': '🪙',     # Coin
            'Copas': '🏆'     # Cup
        }
        self.performance = {
            "questions": 0,
            "correct": 0,
            "tier_performance": {
                "top": {"correct": 0, "total": 0},
                "strong": {"correct": 0, "total": 0},
                "medium": {"correct": 0, "total": 0},
                "weak": {"correct": 0, "total": 0}
            }
        }
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_card(self, suit, rank):
        """Format a card for display"""
        if rank in ['Sota', 'Caballo', 'Rey']:
            rank_display = {'Sota': 'J', 'Caballo': 'C', 'Rey': 'R'}[rank]
        else:
            rank_display = rank
        
        # If suit is "Any", select a random suit for display
        if suit == "Any":
            suit = random.choice(["Espadas", "Bastos", "Oros", "Copas"])
            
        symbol = self.suit_symbols.get(suit, '')
        return f"{rank_display}{symbol} ({rank} of {suit})"
    
    def run_interactive_tutorial(self):
        """Run an interactive tutorial about card values"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("🃏 INTERACTIVE TRUCO CARD VALUE TRAINER 🃏".center(60))
        print("=" * 60 + "\n")
        
        print("This interactive tutorial will help you learn the unique")
        print("card rankings in Argentinian Truco through practice and quizzes.\n")
        
        input("Press Enter to start learning...")
        
        while True:
            self.clear_screen()
            print("\n" + "=" * 60)
            print("🃏 TRUCO CARD VALUE TRAINER 🃏".center(60))
            print("=" * 60 + "\n")
            
            print("Choose an option:")
            print("1. Learn about card tiers")
            print("2. Practice comparing card strengths")
            print("3. Take a quiz")
            print("4. Show card ranking cheat sheet")
            print("5. Exit to game")
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                if choice == "1":
                    self.show_card_tiers()
                elif choice == "2":
                    self.practice_comparing_cards()
                elif choice == "3":
                    self.take_quiz()
                elif choice == "4":
                    self.show_cheat_sheet()
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)
    
    def show_card_tiers(self):
        """Show detailed information about card tiers"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("🃏 TRUCO CARD TIER SYSTEM 🃏".center(60))
        print("=" * 60 + "\n")
        
        print("Truco has a unique card ranking system different from other card games.\n")
        
        # Top tier
        print("⭐⭐⭐ TIER 1: THE SPECIAL FOUR ⭐⭐⭐")
        for i, card in enumerate(self.card_tiers["top"]):
            print(f"{i+1}. {self.format_card(card['suit'], card['rank'])} - {card['description']}")
        print()
        
        # Strong tier
        print("⭐⭐ TIER 2: THE STRONG CARDS ⭐⭐")
        for i, card in enumerate(self.card_tiers["strong"]):
            print(f"{i+1}. {self.format_card(card['suit'], card['rank'])} - {card['description']}")
        print()
        
        # Medium tier
        print("⭐ TIER 3: THE MEDIUM CARDS ⭐")
        for i, card in enumerate(self.card_tiers["medium"]):
            print(f"{i+1}. {self.format_card(card['suit'], card['rank'])} - {card['description']}")
        print()
        
        # Weak tier
        print("⚪ TIER 4: THE WEAK CARDS ⚪")
        for i, card in enumerate(self.card_tiers["weak"]):
            print(f"{i+1}. {self.format_card(card['suit'], card['rank'])} - {card['description']}")
        print()
        
        input("Press Enter to continue...")
    
    def practice_comparing_cards(self):
        """Interactive practice comparing card strengths"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("🃏 CARD COMPARISON PRACTICE 🃏".center(60))
        print("=" * 60 + "\n")
        
        print("I'll show you two cards, and you tell me which one is stronger!\n")
        
        correct = 0
        total = 5
        
        for _ in range(total):
            # Select two different tiers for comparison
            tier1, tier2 = random.sample(["top", "strong", "medium", "weak"], 2)
            
            # Ensure tier1 is stronger than tier2
            if self._get_tier_strength(tier1) > self._get_tier_strength(tier2):
                tier1, tier2 = tier2, tier1
                
            # Select random cards from each tier
            card1 = random.choice(self.card_tiers[tier1])
            card2 = random.choice(self.card_tiers[tier2])
            
            # Format the cards for display
            card1_display = self.format_card(card1["suit"], card1["rank"])
            card2_display = self.format_card(card2["suit"], card2["rank"])
            
            # Randomly determine which option is the correct one
            if random.choice([True, False]):
                print(f"Card A: {card1_display}")
                print(f"Card B: {card2_display}")
                answer = "B" if self._get_tier_strength(tier2) < self._get_tier_strength(tier1) else "A"
            else:
                print(f"Card A: {card2_display}")
                print(f"Card B: {card1_display}")
                answer = "A" if self._get_tier_strength(tier2) < self._get_tier_strength(tier1) else "B"
            
            user_answer = input("\nWhich card is stronger? (A/B): ").strip().upper()
            
            if user_answer == answer:
                print("\n✅ Correct! Well done!")
                correct += 1
            else:
                print(f"\n❌ Incorrect. The correct answer is {answer}.")
                
                # Provide explanation
                if answer == "A":
                    stronger_card = card2 if random.choice([True, False]) else card1
                    weaker_card = card1 if stronger_card == card2 else card2
                else:
                    stronger_card = card1 if random.choice([True, False]) else card2
                    weaker_card = card2 if stronger_card == card1 else card1
                    
                print(f"\nExplanation: {self.format_card(stronger_card['suit'], stronger_card['rank'])} is stronger than")
                print(f"{self.format_card(weaker_card['suit'], weaker_card['rank'])} because {stronger_card['description']}.")
            
            print("\n" + "-" * 40)
            input("\nPress Enter for the next question...")
            print()
        
        print(f"\nYou got {correct} out of {total} correct!")
        input("\nPress Enter to continue...")
    
    def take_quiz(self):
        """Take a quiz on card rankings"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("🃏 TRUCO CARD RANKING QUIZ 🃏".center(60))
        print("=" * 60 + "\n")
        
        print("Test your knowledge of Truco card rankings!\n")
        
        questions = 10
        correct = 0
        
        for i in range(questions):
            self.performance["questions"] += 1
            
            # Different types of questions
            question_type = random.choice([
                "compare_two_cards",
                "identify_tier",
                "strongest_in_set",
                "true_false"
            ])
            
            if question_type == "compare_two_cards":
                correct += self._quiz_compare_two_cards(i+1)
            elif question_type == "identify_tier":
                correct += self._quiz_identify_tier(i+1)
            elif question_type == "strongest_in_set":
                correct += self._quiz_strongest_in_set(i+1)
            elif question_type == "true_false":
                correct += self._quiz_true_false(i+1)
        
        self.performance["correct"] += correct
        
        # Calculate performance percentage
        percentage = (correct / questions) * 100
        
        print(f"\nQuiz complete! You got {correct} out of {questions} correct ({percentage:.1f}%).")
        
        # Provide personalized feedback
        if percentage >= 90:
            print("\n🏆 Excellent! You're a Truco master!")
        elif percentage >= 75:
            print("\n👍 Good job! You're getting the hang of it.")
        elif percentage >= 50:
            print("\n🤔 Not bad, but there's room for improvement.")
        else:
            print("\n📚 Keep practicing - card rankings take time to learn!")
            
        # Show weak areas
        if self.performance["questions"] >= 5:
            print("\nYour performance by card tier:")
            for tier, data in self.performance["tier_performance"].items():
                if data["total"] > 0:
                    tier_percentage = (data["correct"] / data["total"]) * 100
                    print(f"- {tier.capitalize()} cards: {tier_percentage:.1f}%")
            
            # Identify weakest tier
            weakest_tier = min(
                self.performance["tier_performance"].items(),
                key=lambda x: x[1]["correct"] / max(x[1]["total"], 1)
            )[0]
            
            print(f"\nFocus on improving your knowledge of {weakest_tier.upper()} cards.")
        
        input("\nPress Enter to continue...")
    
    def _quiz_compare_two_cards(self, question_num):
        """Generate a question about comparing two cards"""
        # Select two different tiers for comparison
        tier1 = random.choice(["top", "strong", "medium", "weak"])
        tier2 = random.choice(["top", "strong", "medium", "weak"])
        while tier1 == tier2:
            tier2 = random.choice(["top", "strong", "medium", "weak"])
        
        # Select random cards from each tier
        card1 = random.choice(self.card_tiers[tier1])
        card2 = random.choice(self.card_tiers[tier2])
        
        # Format the cards for display
        card1_display = self.format_card(card1["suit"], card1["rank"])
        card2_display = self.format_card(card2["suit"], card2["rank"])
        
        # Update tier tracking
        self.performance["tier_performance"][tier1]["total"] += 1
        self.performance["tier_performance"][tier2]["total"] += 1
        
        print(f"Question {question_num}: Which card is stronger?")
        print(f"A) {card1_display}")
        print(f"B) {card2_display}")
        
        # Determine correct answer
        correct_answer = "A" if self._get_tier_strength(tier1) < self._get_tier_strength(tier2) else "B"
        
        user_answer = input("\nYour answer (A/B): ").strip().upper()
        
        if user_answer == correct_answer:
            print("\n✅ Correct!")
            self.performance["tier_performance"][tier1]["correct"] += 1
            self.performance["tier_performance"][tier2]["correct"] += 1
            return 1
        else:
            print(f"\n❌ Incorrect. The correct answer is {correct_answer}.")
            return 0
    
    def _quiz_identify_tier(self, question_num):
        """Generate a question about identifying a card's tier"""
        tier = random.choice(["top", "strong", "medium", "weak"])
        card = random.choice(self.card_tiers[tier])
        card_display = self.format_card(card["suit"], card["rank"])
        
        # Update tier tracking
        self.performance["tier_performance"][tier]["total"] += 1
        
        print(f"Question {question_num}: Which tier does this card belong to?")
        print(f"Card: {card_display}")
        print("A) Top tier (Special four)")
        print("B) Strong tier (3s, 2s, regular 1s)")
        print("C) Medium tier (Kings, Knights, Jacks)")
        print("D) Weak tier (regular 7s, 6s, 5s, 4s)")
        
        # Map tier to answer option
        tier_to_option = {
            "top": "A",
            "strong": "B",
            "medium": "C",
            "weak": "D"
        }
        
        correct_answer = tier_to_option[tier]
        
        user_answer = input("\nYour answer (A/B/C/D): ").strip().upper()
        
        if user_answer == correct_answer:
            print("\n✅ Correct!")
            self.performance["tier_performance"][tier]["correct"] += 1
            return 1
        else:
            print(f"\n❌ Incorrect. The correct answer is {correct_answer}.")
            print(f"This card belongs to the {tier.upper()} tier.")
            return 0
    
    def _quiz_strongest_in_set(self, question_num):
        """Generate a question about identifying the strongest card in a set"""
        # Create a set of cards from different tiers
        cards = []
        for tier in ["top", "strong", "medium", "weak"]:
            card = random.choice(self.card_tiers[tier])
            cards.append((tier, card))
        
        # Shuffle the cards
        random.shuffle(cards)
        
        # Update tier tracking
        for tier, _ in cards:
            self.performance["tier_performance"][tier]["total"] += 1
        
        print(f"Question {question_num}: Which card is the strongest?")
        options = ["A", "B", "C", "D"]
        
        # Track the correct answer
        correct_answer = None
        strongest_tier_value = float('inf')  # Higher tier value means weaker
        
        for i, (tier, card) in enumerate(cards):
            card_display = self.format_card(card["suit"], card["rank"])
            print(f"{options[i]}) {card_display}")
            
            tier_value = self._get_tier_strength(tier)
            if tier_value < strongest_tier_value:
                strongest_tier_value = tier_value
                correct_answer = options[i]
        
        user_answer = input("\nYour answer (A/B/C/D): ").strip().upper()
        
        if user_answer == correct_answer:
            print("\n✅ Correct!")
            # Mark correct for all tiers
            for tier, _ in cards:
                self.performance["tier_performance"][tier]["correct"] += 1
            return 1
        else:
            print(f"\n❌ Incorrect. The correct answer is {correct_answer}.")
            return 0
    
    def _quiz_true_false(self, question_num):
        """Generate a true/false question about card rankings"""
        # List of true statements
        true_statements = [
            ("The 1 of Espadas is the strongest card in Truco.", "top"),
            ("All 3s are stronger than all 2s in Truco.", "strong"),
            ("The 7 of Espadas is stronger than the 7 of Oros.", "top"),
            ("Kings (Rey) are stronger than Knights (Caballo).", "medium"),
            ("The 1 of Bastos is the second strongest card in the game.", "top"),
            ("The 4s are the weakest cards in Truco.", "weak"),
            ("The 7 of Espadas is one of the top four cards.", "top"),
            ("Regular 1s (not Espadas or Bastos) are weaker than 3s.", "strong")
        ]
        
        # List of false statements
        false_statements = [
            ("The 7 of Copas is stronger than the 7 of Espadas.", "top"),
            ("Knights (Caballo) are stronger than Kings (Rey).", "medium"),
            ("The 5 of Oros is stronger than the 3 of Copas.", "weak"),
            ("The 1 of Copas is the strongest card in the game.", "strong"),
            ("All 7s have the same strength in Truco.", "top"),
            ("Face cards (Rey, Caballo, Sota) are stronger than number cards.", "medium"),
            ("The 4 of Espadas is stronger than the 6 of Bastos.", "weak"),
            ("The 2 of Oros is stronger than the 3 of Bastos.", "strong")
        ]
        
        # Choose whether to ask a true or false statement
        if random.choice([True, False]):
            statement, tier = random.choice(true_statements)
            is_true = True
        else:
            statement, tier = random.choice(false_statements)
            is_true = False
        
        # Update tier tracking
        self.performance["tier_performance"][tier]["total"] += 1
        
        print(f"Question {question_num}: True or False?")
        print(f"\"{statement}\"")
        
        user_answer = input("\nYour answer (T/F): ").strip().upper()
        
        correct_answer = "T" if is_true else "F"
        
        if user_answer == correct_answer or user_answer == "TRUE" and is_true or user_answer == "FALSE" and not is_true:
            print("\n✅ Correct!")
            self.performance["tier_performance"][tier]["correct"] += 1
            return 1
        else:
            print(f"\n❌ Incorrect. The statement is {correct_answer}.")
            return 0
    
    def _get_tier_strength(self, tier):
        """Get numerical strength value for a tier (lower is stronger)"""
        tier_values = {
            "top": 1,
            "strong": 2,
            "medium": 3,
            "weak": 4
        }
        return tier_values.get(tier, 5)
    
    def show_cheat_sheet(self):
        """Show a compact cheat sheet for card ranking"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("🃏 TRUCO CARD RANKING CHEAT SHEET 🃏".center(60))
        print("=" * 60 + "\n")
        
        cheat_sheet = [
            "┌─────────── TRUCO CARD VALUES CHEAT SHEET ───────────┐",
            "│                                                      │",
            "│  TOP CARDS:                                          │",
            "│  1. 1🗡️(Espadas)  2. 1🏑(Bastos)  3. 7🗡️(Espadas)  4. 7🪙(Oros) │",
            "│                                                      │",
            "│  STRONG:          MEDIUM:           WEAK:           │",
            "│  5-8. All 3s      15-18. Kings      27-28. Other 7s │",
            "│  9-12. All 2s     19-22. Knights    29-32. All 6s   │",
            "│  13-14. Other 1s  23-26. Jacks      33-40. 5s & 4s  │",
            "│                                                      │",
            "└──────────────────────────────────────────────────────┘",
            "",
            "💡 QUICK TIPS:",
            "- The 1 of Espadas and 1 of Bastos are exceptions to the normal ranking",
            "- 7 of Espadas and 7 of Oros are much stronger than other 7s",
            "- Within the same category, all cards have the same power",
            "- Face cards are all medium strength despite being 'royalty'",
            "- In Truco, number cards (especially 3s) are often stronger than face cards!"
        ]
        
        for line in cheat_sheet:
            print(line)
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Stand-alone testing
    trainer = TrucoCardTrainer()
    trainer.run_interactive_tutorial()
