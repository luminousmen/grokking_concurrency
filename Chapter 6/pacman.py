""" Pacman game implementation"""
import sys
import time
import select
from random import randrange

# some pacman-specific behavior, probably the bad one, but who knows?
WORLD_STATE = {}


def get_user_input() -> None:
    """Gets the input from the controllers and save it in the game internal state"""
    # please do not use globals in your ordinary life!
    global WORLD_STATE
    # getting the next user input
    i, o, e = select.select([sys.stdin], [], [], 1)
    if i:
        user_input = sys.stdin.readline().strip()
        print(f"user input: {user_input}\n")
        WORLD_STATE["user_input"] = user_input


def compute_game_world() -> None:
    """Computes game world according to the game rules, gamer’s input and game internal state"""
    global WORLD_STATE
    print(f"Pacman doing: {WORLD_STATE.get('user_input', 'user input was not provided')}")
    # computing the internal game world
    print("computing")
    WORLD_STATE["ghost1_position"] = randrange(10)
    WORLD_STATE["ghost2_position"] = randrange(10)
    WORLD_STATE["ghost3_position"] = randrange(10)
    time.sleep(1)


def render_next_screen() -> None:
    global WORLD_STATE
    # rendering the next screen of the program
    print(f"Rendering pacman by user input: {WORLD_STATE.get('user_input', 'user input was not provided')}")
    print(f"Rendering ghost1 in position {WORLD_STATE.get('ghost1_position', 0)}")
    print(f"Rendering ghost2 in position {WORLD_STATE.get('ghost2_position', 0)}")
    print(f"Rendering ghost3 in position {WORLD_STATE.get('ghost3_position', 0)}")
    time.sleep(0.5)
