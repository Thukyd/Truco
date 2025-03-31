#!/usr/bin/env python3

"""
Argentinian Truco - Game Launcher
This script brings together all the modules and launches the game with a user-friendly interface
"""

import os
import sys
import time
import random
from typing import List, Dict, Any, Optional

# Global settings - defined at module level
ENABLE_COLORS = True
SCREEN_WIDTH = 80
SCROLL_DELAY = 0.5

# Import the restructured module
try:
    from truco import TrucoGame, DisplayManager, TerminalColors
    from card_learning_system import TrucoCardTrainer
except ImportError:
    print("Error: Required modules not found.")
    print("Make sure truco_restructured.py and card_learning_system.py are in the same directory.")
    sys.exit(1)


class TrucoLauncher:
    """A launcher for the Argentinian Truco game with an improved interface"""
    
    def __init__(self):
        self.display_manager = DisplayManager()
        self.card_trainer = TrucoCardTrainer(self.display_manager)
    
    def show_title_screen(self):
        """Display a fancy title screen"""
        self.display_manager.clear_screen()
        
        title = [
            "╔═══════════════════════════════════════════════════════════╗",
            "║                                                           ║",
            "║   █████╗ ██████╗  ██████╗ ███████╗███╗   ██╗████████╗    ║",
            "║  ██╔══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ║",
            "║  ███████║██████╔╝██║  ███╗█████╗  ██╔██╗ ██║   ██║       ║",
            "║  ██╔══██║██╔══██╗██║   ██║██╔══╝  ██║╚██╗██║   ██║       ║",
            "║  ██║  ██║██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ║",
            "║  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ║",
            "║                                                           ║",
            "║                      ████████╗██████╗ ██╗   ██╗ ██████╗  ║",
            "║                      ╚══██╔══╝██╔══██╗██║   ██║██╔════╝  ║",
            "║                         ██║   ██████╔╝██║   ██║██║       ║",
            "║                         ██║   ██╔══██╗██║   ██║██║       ║",
            "║                         ██║   ██║  ██║╚██████╔╝╚██████╗  ║",
            "║                         ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ║",
            "║                                                           ║",
            "║             Learning Edition - Build Your Skills          ║",
            "║                                                           ║",
            "╚═══════════════════════════════════════════════════════════╝",
        ]
        
        # Print title with color if enabled
        for line in title:
            if ENABLE_COLORS:
                colored_line = TerminalColors.colorize(line, TerminalColors.BRIGHT_GREEN)
                print(colored_line)
            else:
                print(line)
        
        print("\n🃏 The classic Argentinian card game 🃏")
        print("Designed for beginners to learn and master the card values")
        
        # Wait for user input
        self.display_manager.press_any_key("\nPress Enter to start...")
    
    def show_about_truco(self):
        """Show information about Argentinian Truco"""
        self.display_manager.clear_screen()
        
        self.display_manager.section("ABOUT ARGENTINIAN TRUCO", color=TerminalColors.BRIGHT_YELLOW)
        
        about_text = [
            "Truco is a popular trick-taking card game played throughout South America,",
            "with particularly strong traditions in Argentina, Uruguay, and Brazil.",
            "",
            "🎮 Key Features of Argentinian Truco:",
            "",
            "• Uses a Spanish deck (40 cards)",
            "• Unique card ranking system unlike most other card games",
            "• Played between two teams (1v1, 2v2, or 3v3)",
            "• Combines strategy, psychology, and bluffing",
            "• Features a complex betting system (Truco, Retruco, Vale Cuatro)",
            "• Has a secondary betting feature (Envido)",
            "",
            "🌟 What Makes Truco Special:",
            "",
            "• Verbal banter and psychological warfare are essential parts of the game",
            "• The unusual card ranking makes it challenging for beginners",
            "• The game has deep cultural significance in Argentina",
            "• Blend of skill, luck, and social interaction",
            "",
            "This learning edition will help you master the card values and basic strategy!"
        ]
        
        for line in about_text:
            print(line)
            
        self.display_manager.press_any_key()
    
    def show_main_menu(self):
        """Display the main menu and handle user choices"""
        while True:
            self.display_manager.clear_screen()
            
            self.display_manager.section("ARGENTINIAN TRUCO - MAIN MENU", color=TerminalColors.BRIGHT_MAGENTA)
            
            menu_options = [
                "1. Play Truco",
                "2. Card Value Trainer",
                "3. About Argentinian Truco",
                "4. Game Settings",
                "5. Exit Game"
            ]
            
            for option in menu_options:
                print(option)
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.card_trainer.run_interactive_tutorial()
            elif choice == "3":
                self.show_about_truco()
            elif choice == "4":
                self.show_settings()
            elif choice == "5":
                self.display_manager.clear_screen()
                print("\nThank you for playing Argentinian Truco!")
                print("¡Hasta la próxima! (Until next time!)\n")
                return
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
    
    def show_settings(self):
        """Display and modify game settings"""
        # Declare globals at the beginning of the function
        global ENABLE_COLORS, SCREEN_WIDTH, SCROLL_DELAY
        
        self.display_manager.clear_screen()
        
        self.display_manager.section("GAME SETTINGS", color=TerminalColors.BRIGHT_CYAN)
        
        print("Current settings:")
        print(f"1. Terminal Colors: {'Enabled' if ENABLE_COLORS else 'Disabled'}")
        print(f"2. Screen Width: {SCREEN_WIDTH} characters")
        print(f"3. Scroll Delay: {SCROLL_DELAY} seconds")
        print("4. Return to Main Menu")
        
        choice = input("\nEnter setting to change (1-4): ").strip()
        
        if choice == "1":
            toggle = input("Enable terminal colors? (y/n): ").strip().lower()
            if toggle in ["y", "yes"]:
                ENABLE_COLORS = True
                print("Terminal colors enabled.")
            elif toggle in ["n", "no"]:
                ENABLE_COLORS = False
                print("Terminal colors disabled.")
        elif choice == "2":
            try:
                new_width = int(input("Enter new screen width (40-120): ").strip())
                if 40 <= new_width <= 120:
                    SCREEN_WIDTH = new_width
                    print(f"Screen width set to {SCREEN_WIDTH}.")
                else:
                    print("Width must be between 40 and 120.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "3":
            try:
                new_delay = float(input("Enter new scroll delay (0.0-2.0 seconds): ").strip())
                if 0.0 <= new_delay <= 2.0:
                    SCROLL_DELAY = new_delay
                    print(f"Scroll delay set to {SCROLL_DELAY} seconds.")
                else:
                    print("Delay must be between 0.0 and 2.0 seconds.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Small delay before returning
        time.sleep(1)
    
    def start_game(self):
        """Configure and start a new game of Truco"""
        self.display_manager.clear_screen()
        
        self.display_manager.section("NEW GAME SETUP", color=TerminalColors.BRIGHT_GREEN)
        
        # Choose number of players
        print("Select number of players:")
        print("1. 👤 vs 🤖 (2 players, 1 vs 1)")
        print("2. 👥 vs 🤖🤖 (4 players, 2 vs 2)")
        print("3. 👥👥 vs 🤖🤖🤖 (6 players, 3 vs 3)")
        
        num_players = 2  # Default
        while True:
            try:
                choice = input("\n🔢 Enter your choice (1-3): ").strip()
                if not choice:
                    break  # Use default
                choice = int(choice)
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
        
        # Enable Card Advisor?
        print("\n💡 The Card Value Advisor helps you learn the game by providing tips and strategic advice.")
        enable_advisor = input("Enable Card Value Advisor? (y/n, default: y): ").lower() != 'n'
        
        # Choose tutorial level
        print("\n📚 Choose tutorial level:")
        print("1. Full - Complete explanation of rules, card values, and strategy")
        print("2. Basic - Quick overview of essential rules and card values")
        print("3. Minimal - Just the card ranking, for experienced players")
        
        tutorial_level = "full"  # Default
        while True:
            try:
                level_choice = input("\n🔢 Enter your choice (1-3, default: 1): ").strip()
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
        player_name = input("\n✍️ Enter your name: ").strip()
        if not player_name:
            player_name = "Player"
        
        # Enter AI opponent names (optional)
        self.display_manager.section("AI PLAYER NAMES", color=TerminalColors.BRIGHT_MAGENTA)
        print("Enter names for your AI opponents (or press Enter for default names)")
        print("Note: Spanish/Argentinian names add to the atmosphere!")
        
        ai_names = []
        for i in range(1, num_players):
            ai_name = input(f"AI Player {i}: ").strip()
            if ai_name:
                ai_names.append(ai_name)
            else:
                # Provide Spanish-sounding default names
                default_spanish_names = [
                    "Carlos", "Juan", "Miguel", "Diego", "Luis",
                    "Roberto", "Pablo", "Javier", "Martín", "Eduardo"
                ]
                ai_names.append(random.choice(default_spanish_names))
        
        # Create and start game
        game = TrucoGame(num_players, enable_envido, enable_advisor)
        game.setup_game(player_name, ai_names, tutorial_level)
        game.play_game()


if __name__ == "__main__":
    launcher = TrucoLauncher()
    launcher.show_title_screen()
    launcher.show_main_menu()