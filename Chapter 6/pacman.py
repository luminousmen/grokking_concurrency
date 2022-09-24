""" Pacman game implementation"""
import time
from random import randrange

# some pacman-specific behavior, probably the bad one, but who knows?
WORLD_STATE = {}


def get_user_input() -> None:
    """Gets the input from the controllers and save it in the game internal
    state """
    # getting the next user input
    if user_input := input().strip():
        print(f"user input: {user_input}\n")
        WORLD_STATE["user_input"] = user_input


def compute_game_world() -> None:
    """Computes game world according to the game rules, gamer’s input and
    game internal state """
    print(f"Pacman doing: {WORLD_STATE.get('user_input', 'user input was not provided')}")
    # computing the internal game world
    print("computing")
    WORLD_STATE["ghost1_position"] = randrange(10)
    WORLD_STATE["ghost2_position"] = randrange(10)
    WORLD_STATE["ghost3_position"] = randrange(10)
    time.sleep(1)


def render_next_screen() -> None:
    # rendering the next screen of the program
    print(f"Rendering pacman by user input: "
          f"{WORLD_STATE.get('user_input', 'not provided')}")
    print(f"Rendering ghost1 in position "
          f"{WORLD_STATE.get('ghost1_position', 0)}")
    print(f"Rendering ghost2 in position "
          f"{WORLD_STATE.get('ghost2_position', 0)}")
    print(f"Rendering ghost3 in position "
          f"{WORLD_STATE.get('ghost3_position', 0)}")
    time.sleep(0.5)
