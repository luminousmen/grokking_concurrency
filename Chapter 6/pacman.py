""" Pacman game implementation"""
import sys
import time
import select
from random import randrange

# some pacman-specific behavior, probably the bad one, but who knows?
PACMAN_POSITION = {}


def get_user_input() -> None:
    """Gets the input from the controllers and save it in the game internal state"""
    # please do not use globals in your ordinary life!
    global PACMAN_POSITION
    # getting the next user input
    i, o, e = select.select([sys.stdin], [], [], 1)
    if i:
        user_input = sys.stdin.readline().strip()
        print(f"user input: {user_input}\n")
        PACMAN_POSITION["user_input"] = user_input


def compute_game_world() -> None:
    """Computes game world according to the game rules, gamer’s input and game internal state"""
    global PACMAN_POSITION
    print(f"Pacman doing: {PACMAN_POSITION.get('user_input', 'user input was not provided')}")
    # computing the internal game world
    print("computing")
    PACMAN_POSITION["position"] = randrange(10)
    time.sleep(1)


def render_next_screen() -> None:
    global PACMAN_POSITION
    print(f"Rendering pacman by user input: {PACMAN_POSITION.get('user_input', 'user input was not provided')} and "
          f"position {PACMAN_POSITION.get('position', 0)}")
    # rendering the next screen of the program
    print("rendering\n")
    time.sleep(0.5)
