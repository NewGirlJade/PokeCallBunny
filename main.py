from openal import *
import time
import random  # import randrange, choice
import pokebase as pb
from pokebase import cache
import requests
import json
import os, os.path


class Context:
    def __init__(self):
        self.pokemon_count = fetch_pokemon_count()


def get_audio_path(poke_number: int) -> str:
    """the audio_path() function takes a pokemon's national Pokedex number as an integer and returns a string corresponding to the soundfile of that pokemon's cry in the host filesystem"""
    return "./audio/cries-main/cries/pokemon/latest/" + str(poke_number) + ".ogg"


def fetch_pokemon_by_name(name: str) -> dict:
    """downloads cries as needed from pokeAPI and returns the filepath where the cry has been cached. Probably currently conflicts with get_audio_path()"""
    # just make it work with the default cry for now

    with open("./pokemon-data.json") as file:
        pokemon_data = dict(json.loads(file.read()))
        results = pokemon_data["results"]
        for pokemon in results:
            if pokemon["name"] == name:
                url = pokemon["url"]
                response = requests.get(url)
                data = dict(json.loads(response.text))
                return data
        return "could not find match"


def get_name_from_number():
    pass


def get_number_from_name():
    pass


def fetch_pokemon_by_number(number: int) -> str:
    pass


def play_cry(poke_number: int) -> None:
    """The play_cry() function takes a pokemon's national Pokedex number and opens a PyOpenAL Source object in order to play the audio file."""
    audio = oalOpen(get_audio_path(poke_number))
    audio.play()
    while audio.get_state() == AL_PLAYING:
        time.sleep(0.01)

    # sourceStream = oalStream("/home/jayda/Source/PokeCallBunny/test_samples/25.ogg")
    # sourceStream.play()
    # while sourceStream.get_state() == AL_PLAYING:
    #     sourceStream.update()
    # time.sleep(5)


def prompt_loop(context: Context):
    """prints stuff to terminal and reads user input"""
    print(
        "  Type a Pokemon's name or ID \n  [r/rand/random] for random \n  [q, quit, exit] to quit"
    )
    while True:
        directive = input().lower()
        if directive == "q" or directive == "quit" or directive == "exit":
            break
        elif directive.isdigit():
            directive = int(directive)
            if directive > context.pokemon_count or directive <= 0:
                print(
                    "That number doesn't represent a pokemon known to the scientific community yet. Please try again."
                )
            else:
                poke_name = str(pb.APIResource("pokemon", directive))
                play_cry(directive)
                print("That was the cry of " + poke_name + " (#" + str(directive) + ")")
        elif directive == "random" or directive == "rand" or directive == "r":
            poke_number = gen_random_pokenumber(context)
            poke_name = str(pb.APIResource("pokemon", poke_number))
            play_cry(poke_number)
            print("That was the cry of " + poke_name + " (#" + str(poke_number) + ")")
        elif directive == "help":
            print(
                "Type a Pokemon's name or ID \n  [r/rand/random] for random \n  [q, quit, exit] to quit"
            )
        else:
            print("Fetching Pokemon by name: " + directive)
            data = fetch_pokemon_by_name(directive)
            id = data["id"]
            play_cry(int(id))
            print("That was the cry of " + directive + "(#" + str(id) + ")")


def fetch_pokemon_count() -> int:
    """the fetch_pokemon_count() function fetches the current pokemon count from PokeAPI"""

    req = requests.get("https://pokeapi.co/api/v2/pokemon-species/?limit=1")
    species = dict(json.loads(req.text))
    return species["count"]


def gen_random_pokenumber(context: Context) -> int:
    """the get_random_pokenumber() function takes no arguments (currently) and returns a random pokemon's number from a pool of all current pokemon as fetched earlier from PokeAPI and stored in the context"""
    return random.randrange(context.pokemon_count)


# TODO: add optional arguments of generations to include and only return a random pokemon from those generations.


def cleanup() -> None:
    """the oalQuit() function exits out of OpenAL and destroys all existing Sources and Buffers. It's strongly reccommended to call it before quitting the program (I'm guessing the OS would probably do this automatically but it never hurts to leave less to chance)"""
    oalQuit()


def main():

    # print(random.choice(os.listdir("./audio/cries-main/cries/pokemon/latest/")))
    context = Context()
    print("Hello from pokecallbunny!")
    prompt_loop(context)
    # poke_number = gen_random_pokenumber()
    # poke_name = str(pb.APIResource("pokemon", poke_number))
    # play_cry(poke_number)
    # print("That was the cry of " + poke_name)
    cleanup()


if __name__ == "__main__":
    main()
