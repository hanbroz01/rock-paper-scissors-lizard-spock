#!/usr/bin/env python3
import time
import random

"""
# -------------------------------------
# 🖖 Rock, Paper, Scissors, Lizard, Spock
# -------------------------------------

A console-based game where a human player can compete against
various AI strategies: Random, Reflect, or Cycle.

Features:
- 5 rounds per game with score tracking
- Colored text output
- Multiple AI strategies
- Replay option
"""


def text_color(message, color, background=False):
    # Allows different text color
    soc = '\33[48;5;' if background else '\33[38;5;'
    eoc = '\033[0m'
    return f"{soc}{color}m{message}{eoc}"


def print_pause(message_to_print, delay=1):  # Allows delays in printing text
    time.sleep(delay)
    print(message_to_print)


def valid_input(prompt, options):  # Creates a way to deal with unknown input
    while True:
        option = input(prompt).lower()
        if option in options:
            return option
        print_pause(f'Sorry, I do not understand "{option}".')


class Player:  # Base class for all players
    moves = ['rock', 'paper', 'scissors', 'lizard', 'spock']

    def move(self):
        return 'rock'

    def __init__(self):
        # Initialisation of the List for move function
        self.my_move = self.moves
        self.their_move = random.choice(self.moves)

    def learn(self, my_move, their_move):
        pass


class RandomPlayer(Player):  # Plays Random move
    def move(self):
        return random.choice(self.moves)


class HumanPlayer(Player):  # Human Player input
    def move(self):
        answer = valid_input(
            "Please Enter Rock, Paper, Scissors, Lizard or Spock\n",
            ["rock", "paper", "scissors", "lizard", "spock"]
            )
        self.human_move = answer
        return self.human_move


class ReflectPlayer(Player):  # Plays what human played in previous round
    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move

    def move(self):
        return self.their_move


class CyclePlayer(Player):  # Plays through cycle of moves
    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move

    def move(self):
        if self.my_move == self.moves[0]:
            return self.moves[1]
        elif self.my_move == self.moves[1]:
            return self.moves[2]
        elif self.my_move == self.moves[2]:
            return self.moves[3]
        elif self.my_move == self.moves[3]:
            return self.moves[4]
        else:
            return self.moves[0]


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock') or
            (one == 'rock' and two == 'lizard') or
            (one == 'scissors' and two == 'lizard') or
            (one == 'paper' and two == 'spock') or
            (one == 'lizard' and two == 'paper') or
            (one == 'lizard' and two == 'spock') or
            (one == 'spock' and two == 'scissors') or
            (one == 'spock' and two == 'rock'))


class Game:   # Manages a game between two players
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):  # Play a single round and update scores
        move1 = self.p1.move()
        move2 = self.p2.move()
        print_pause(f"Player 1: {move1}  Player 2: {move2}")

        if beats(move1, move2) is True:
            # If Human wins, score increase by 1
            self.p1_wins += 1
            print_pause("** Player one wins **")
            print_pause(
                f"Score: Player One - {self.p1_wins}, "
                f"Player two - {self.p2_wins}\n")
        elif beats(move2, move1) is True:
            # If Computer wins, score increase by 1
            self.p2_wins += 1
            print_pause("** Player two wins **")
            print_pause(
                f"Score: Player One - {self.p1_wins}, "
                f"Player two - {self.p2_wins}\n")
        else:
            print_pause("** Tied game **")  # If both playes play same move
            print_pause(
                f"Score: Player One - {self.p1_wins}, "
                f"Player two - {self.p2_wins}\n")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        self.p1_wins = 0  # Re sets scores if player wished to play again
        self.p2_wins = 0
        color = 10
        text_title = text_color("Rock Paper Scissors Lizard Spock, Go!", color)
        print_pause(f"{text_title}")
        time.sleep(1)
        print_pause("Can you beat the computer in 5 rounds?\n")
        text_rules = text_color("Rules:", color)
        print_pause(f"{text_rules}")
        print_pause("Rock     -> beats Scissors AND Lizard", 2)
        print_pause("Paper    -> beats Rock AND Spock", 2)
        print_pause("Scissors -> beats Paper AND Lizard", 2)
        print_pause("Lizard   -> beats Spock AND Paper", 2)
        print_pause("Spock    -> beats Rock AND Scissors\n", 2)

        self.rounds = 5   
        for rounds in range(self.rounds):  # Plays 5 rounds in total
            color = 105
            round_color = text_color(f"Round -- {rounds + 1} --", color)
            print_pause(f"{round_color}")
            time.sleep(1)
            self.play_round()

        # Final results printed
        print_pause(f"Player One won {self.p1_wins} time(s)")
        print_pause(f"Player Two won {self.p2_wins} time(s)")

        if self.p1_wins > self.p2_wins:  # Works out who wins
            print_pause("** Player One Wins **\n")
        elif self.p2_wins > self.p1_wins:
            print_pause("** Player Two Wins **\n")
        else:
            print_pause("** Tied Game **")

        play_again()


def play_again():  # Game will automatically exit if no is chosen
    color = 160
    text_red = text_color("-->GAME OVER--<\n", color)
    print_pause(f"{text_red}")
    time.sleep(2)
    answer = valid_input("Play again? Yes or No\n", ["yes", "no"])

    if 'no' in answer:
        print_pause("Ok, Goodbye!")
        exit()
    else:
        game.play_game()

# Instantiate random players
players = (ReflectPlayer(), RandomPlayer(), CyclePlayer(), Player())
random_players = random.choice(players)

# This block ensures that the following code only runs when
# this file is executed directly, not when imported as a module.
if __name__ == '__main__':
    # Create a new Game instance with:
    # - HumanPlayer() as Player 1
    # - A randomly chosen AI player as Player 2
    game = Game(HumanPlayer(), random_players)

    # Start the game loop
    game.play_game()
