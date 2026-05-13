from openal import *
import time
import os, os.path
import sqlite3
from Levenshtein import distance


class Context:
    """object to handle program state"""

    def __init__(self):
        self.con = sqlite3.connect("pokemon.db")
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        oal_cleanup()


def oal_cleanup() -> None:
    """this function exits out of OpenAL and destroys all existing Sources and Buffers. OAL strongly reccommends calling it before quitting the program"""
    oalQuit()
    print("OpenAL exited")


def get_audio_path(poke_number: int) -> str:
    """this function takes a pokemon's national Pokedex number as an integer and returns a string corresponding to the soundfile of that pokemon's cry in the host filesystem"""
    return "./audio/cries-main/cries/pokemon/latest/" + str(poke_number) + ".ogg"


# TODO: have this check for a perfer-legacy option in context and try to find a legacy cry if enabled


def play_cry(context: Context, poke_number: int, **kwargs) -> None:
    """this function takes a pokemon's national Pokedex number and opens a PyOpenAL Source object in order to play the audio file. It takes an optional keyword argument 'should_guess', which, if true, prompts the user to guess which pokemon the cry is from before continuing"""
    poke_name, form_name = get_pokemon_by_id(context, poke_number).values()
    if not poke_name:
        print(
            "That number doesn't represent a pokemon known to the scientific community yet. Please try again."
        )
    else:
        audio_path = get_audio_path(poke_number)
        if not os.path.isfile(audio_path):
            # TODO: add web request to pokeAPI to try to download sound file if not found
            print(
                "audio path for alternate form  ("
                + form_name
                + ", #"
                + str(poke_number)
                + ") not found, defaulting to base form."
            )
            poke_number = get_base_form_id(context, poke_number)
            audio_path = get_audio_path(poke_number)
            form_name = None
        shouldStop = False
        while not shouldStop:
            audio = oalOpen(audio_path)
            audio.play()
            while audio.get_state() == AL_PLAYING:
                time.sleep(0.01)
            shouldStop = True
            if kwargs.get("should_guess"):
                shouldStop = request_guess(poke_name, form_name)
        print(
            "That was the cry of "
            + (form_name if form_name else poke_name).capitalize()
            + " (#"
            + str(poke_number)
            + ")"
        )


def request_guess(source_pokename: str, source_formname: str) -> bool:
    """this function is called from the play_cry() function if "should_guess = true" is passed as a keyword argument. It compares info about the a random source pokemon to a user input string and gives feedback based on the Levenshtein distance between the two"""

    print("make a guess (enter r to repeat or enter to skip)")
    while True:
        guess = input().lower()
        if guess == "q":
            quit()
        if guess == "r":
            return False
        if guess == "help":
            print("make a guess (enter r to repeat or enter to skip)")
        source = source_formname if source_formname else source_pokename
        if guess == "":
            return True

        similarity = distance(source, guess)
        match similarity:
            case 0:
                print("Exactly!")
                return True
            case 1:
                print("Correct!")
                return True
            case 2 | 3 | 4:
                print("Almost right! Try again?")
            case 5 | 6:
                print("Not quite. Try again?")
            case _:
                print("Sorry, that's not it. Try again?")


def prompt_loop(context: Context):
    """main program loop"""
    print(
        "  Type a Pokemon's name or ID \n  [r/rand/random] for random \n  [q, quit, exit] to quit"
    )
    while True:
        directive = input().lower()
        if directive == "q" or directive == "quit" or directive == "exit":
            quit()
        elif directive.isdigit():
            directive = int(directive)
            play_cry(context, directive)
        elif directive == "random" or directive == "rand" or directive == "r":
            poke_number = gen_random_pokenumber(context)
            play_cry(context, poke_number, should_guess=True)
        # TODO: add a directive to list all forms of a species
        elif directive == "help":
            print(
                "Type a Pokemon's name or ID \n  [r/rand/random] for random \n  [q, quit, exit] to quit"
            )
        else:
            print("Fetching Pokemon call by name: " + directive)
            id = get_first_id_by_pokeName(context, directive)
            if id:
                play_cry(context, id)
            else:
                print("No pokemon matching that name was found,")
                allmons = sorted(get_forms_by_pokeName(context, directive).items())
                if len(allmons) > 0 and len(allmons) < 100:
                    print(
                        "but the following similar entries might be what you're looking for:"
                    )
                    for pokemon in allmons:
                        print(pokemon)
                print(str(len(allmons)), "similar entries found.")
                print("Please try again")


def gen_random_pokenumber(context: Context) -> int:
    """this function returns a random pokemon's ID from pokemon.db"""
    (id,) = context.cur.execute(
        "select pokeid from pokemon order by random() limit 1"
    ).fetchone()
    return id


# TODO: add optional arguments of generations to include and only return a
# random pokemon from those generations. Or, probably better, make commands
# that will set the generations to include in the context and have this
# function check when generating a random pokemon.

# TODO: add option to exclude alternate forms


def get_base_form_id(context: Context, id: int) -> int:
    """this function takes a pokemon's ID and returns the id of its base form."""
    pokename = context.cur.execute(
        "select pokeName from pokemon where PokeID = ?", (id,)
    ).fetchone()
    (base_id,) = context.cur.execute(
        "select pokeid from pokemon where pokename = ?", pokename
    ).fetchone()
    return base_id


# TODO: I feel like this is the usecase for a join but I'm not very confident with those yet and this works.


def get_forms_by_pokeName(context: Context, name: str) -> [(int,)]:
    """queries the database and returns a name and id for all pokemon similar to the name argument provided. Used when no direct match is found to a user input"""
    data = context.cur.execute(
        "select pokeid, pokename, formname from pokemon where PokeName like ?",
        ("%" + name + "%",),
    ).fetchall()
    data += context.cur.execute(
        "select pokeid, pokename, formname from pokemon where formname like ?",
        ("%" + name + "%",),
    ).fetchall()

    return {
        id: (formname if formname else pokename) for (id, pokename, formname) in data
    }


def get_first_id_by_pokeName(context: Context, name: str) -> int:
    """queries the database and returns the base form ID of the provided species name, and searches for an alternate form if no species match is found"""
    try:
        (id,) = context.cur.execute(
            "select pokeid from pokemon where PokeName = ?", (name,)
        ).fetchone()
    except TypeError:
        try:
            (id,) = context.cur.execute(
                "select pokeid from pokemon where FormName = ?", (name,)
            ).fetchone()
        except TypeError:
            id = None
    return id


def get_pokemon_by_id(context: Context, id: int) -> dict:
    """queries the database for a pokemon ID and returns a dictionary with the name and formname for that ID, if they're found"""
    try:
        name, formName = context.cur.execute(
            "select pokename, formname from pokemon where PokeID = ?", (id,)
        ).fetchone()
        names = {"name": name, "formName": formName}
    except TypeError:
        names = {"name": None, "formName": None}
    return names


def main():
    with Context() as context:
        print("Hello from pokecallbunny!")
        prompt_loop(context)


if __name__ == "__main__":
    main()
