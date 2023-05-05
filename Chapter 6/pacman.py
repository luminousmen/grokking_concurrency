""" Pacman game implementation - bug bounty is now open"""
import os
import sys
import time
import random

# Define the game world size
GAME_WIDTH = 20
GAME_HEIGHT = 20
DELAY = 1

# Define the current state of the game world
pacman = (0, 0)
ghosts = [(5, 5), (10, 10)]
score = -10
is_game_over = False
# Define a set to keep track of the locations of the dots
dots = {(x, y) for x in range(GAME_WIDTH) for y in range(GAME_HEIGHT)}


def get_user_input() -> None:
    """Gets the input from the controllers and save it in the game internal
    state"""
    while True:
        global pacman, ghosts, is_game_over
        if is_game_over:
            sys.exit()

        # Process the user input
        user_input = input()
        # Update the game state based on the user input
        if user_input == "q":
            is_game_over = True
            # Quit the game if the user presses "q"
            sys.exit()
        else:
            global pacman
            if user_input == "w":
                # Move the pacman up if the user presses "w"
                pacman = (pacman[0], pacman[1] - 1)
            elif user_input == "a":
                # Move the pacman left if the user presses "a"
                pacman = (pacman[0] - 1, pacman[1])
            elif user_input == "s":
                # Move the pacman down if the user presses "s"
                pacman = (pacman[0], pacman[1] + 1)
            elif user_input == "d":
                # Move the pacman right if the user presses "d"
                pacman = (pacman[0] + 1, pacman[1])
            else:
                # Ignore any other input
                pass


def compute_game_world() -> None:
    """Computes game world according to the game rules, gamer’s input and
    game internal state """
    while True:
        global pacman, ghosts, is_game_over, score
        if is_game_over:
            sys.exit()
        # Move the ghosts randomly
        for i, ghost in enumerate(ghosts):
            new_ghost_x = ghost[0] + random.choice([-1, 0, 1])
            new_ghost_y = ghost[1] + random.choice([-1, 0, 1])
            new_ghost_x = new_ghost_x if 0 <= new_ghost_x < GAME_WIDTH else ghost[0]
            new_ghost_y = new_ghost_y if 0 <= new_ghost_y < GAME_HEIGHT else ghost[1]
            ghosts[i] = (new_ghost_x, new_ghost_y)

        # Check if the ghosts caught the pacman
        if pacman in ghosts:
            is_game_over = True
            sys.exit()

        # Check if pacman has eaten a dot
        if pacman in dots:
            dots.remove(pacman)
            score += 10

        # Check if all dots have been eaten
        if not dots:
            is_game_over = True
            sys.exit()

        # Sleep for a short time to avoid excessive CPU usage
        time.sleep(DELAY)


def render_next_screen() -> None:
    """Render the next frame of the game"""
    while True:
        global pacman, ghosts, score, is_game_over, dots
        # Clear the terminal screen
        os.system("clear")

        if is_game_over:
            print("GAME OVER!")
            print(f"Your score: {score}. Press Enter")
            sys.exit()

        # Render the game world on the terminal
        game_world = []
        for y in range(GAME_HEIGHT):
            row = []
            for x in range(GAME_WIDTH):
                if (x, y) == pacman:
                    row.append("P")
                elif (x, y) in ghosts:
                    row.append("G")
                elif (x, y) in dots:
                    row.append(".")
                else:
                    row.append(" ")
            game_world.append(" ".join(row))

        print(f"Score:{score}. Press 'q' to quit")
        print("\n".join(game_world))
        # Sleep for a short time to avoid excessive CPU usage
        time.sleep(DELAY)
