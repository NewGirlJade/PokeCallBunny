from openal import *
import time
from random import randrange
import pokebase as pb
from pokebase import cache
import requests
import json


def get_audio_path(poke_number: int) -> str:
    """the audio_path() function takes a pokemon's national Pokedex number as an integer and returns a string corresponding to the soundfile of that pokemon's cry in the host filesystem"""
    return "./audio/cries-main/cries/pokemon/latest/" + str(poke_number) + ".ogg"


def fetch_pokemon_cry(pokemon: str) -> str:
    """downloads cries as needed from pokeAPI and returns the filepath where the cry has been cached. Probably currently conflicts with get_audio_path()"""
    # just make it work with the default cry for now
    pass


def play_cry(poke_number: int) -> None:
    """The play_cry() function takes a pokemon's national Pokedex number and opens a PyOpenAL Source object in order to play the audio file."""
    audio = oalOpen(get_audio_path(poke_number))
    audio.play()
    while audio.get_state() == AL_PLAYING:
        time.sleep(1)

    # sourceStream = oalStream("/home/jayda/Source/PokeCallBunny/test_samples/25.ogg")
    # sourceStream.play()
    # while sourceStream.get_state() == AL_PLAYING:
    #     sourceStream.update()
    # time.sleep(5)


def prompt_loop():
    """prints stuff to terminal and reads user input"""
    should_stop = 0
    while True:
        print("type anything:")
        directive = input()
        print(directive.isdigit())
        if directive.isdigit():
            directive = int(directive)
            if directive > fetch_pokemon_count() or directive <= 0:
                print("Unrecognized command. Please try again.")
            else:
                poke_name = str(pb.APIResource("pokemon", directive))
                play_cry(directive)
                print("That was the cry of " + poke_name)
        break
        # case "q" or "quit" or "exit" break


def fetch_pokemon_count() -> int:
    """the fetch_pokemon_count() function fetches the current pokemon count from PokeAPI"""

    req = requests.get("https://pokeapi.co/api/v2/pokemon-species/?limit=1")
    species = dict(json.loads(req.text))
    return species["count"]


def gen_random_pokenumber() -> int:
    """the get_random_pokenumber() function takes no arguments (currently) and returns a random pokemon's number from a pool of all current pokemon as fetched from PokeAPI"""
    return randrange(fetch_pokemon_count())


# TODO: add optional arguments of generations to include and only return a random pokemon from those generations.


def cleanup() -> None:
    """the oalQuit() function exits out of OpenAL and destroys all existing Sources and Buffers. It's strongly reccommended to call it before quitting the program (I'm guessing the OS would probably do this automatically but it never hurts to leave less to chance)"""
    oalQuit()


def main():
    print("Hello from pokecallbunny!")
    prompt_loop()
    # poke_number = gen_random_pokenumber()
    # poke_name = str(pb.APIResource("pokemon", poke_number))
    # play_cry(poke_number)
    # print("That was the cry of " + poke_name)
    cleanup()


if __name__ == "__main__":
    main()
