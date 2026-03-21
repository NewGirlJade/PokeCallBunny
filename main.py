from openal import *
import time
from random import randrange
import pokebase as pb
from pokebase import cache


def fetch_pokemon_cry(pokemon: str) -> str:
    # downloads cries as needed from pokeAPI and returns the filepath where the cry has been cached```
    # just make it work with the default cry for now
    pass


def prompt_loop():
    # prints stuff to terminal and reads user input```
    # while !should_stop:
    # implement this one second
    pass


def play_cry(poke_number: int) -> None:
    # implement this one first- one PR per function
    audio_path = "./audio/cries-main/cries/pokemon/latest/" + str(poke_number) + ".ogg"
    print(audio_path)
    audio = oalOpen(audio_path)
    audio.play()
    while audio.get_state() == AL_PLAYING:
        time.sleep(1)

    # sourceStream = oalStream("/home/jayda/Source/PokeCallBunny/test_samples/25.ogg")
    # sourceStream.play()
    # while sourceStream.get_state() == AL_PLAYING:
    #     sourceStream.update()
    # time.sleep(5)


def cleanup() -> None:
    oalQuit()


def main():
    print("Hello from pokecallbunny!")

    poke_number = randrange(1025)
    poke_name = str(pb.APIResource("pokemon", poke_number))

    play_cry(poke_number)

    print("That was the cry of " + poke_name)
    cleanup()


if __name__ == "__main__":
    main()
