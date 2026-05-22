import main
import pytest
import sqlite3


def test_get_audio_path():
    result = main.get_audio_path(420)
    assert result.startswith("./audio")
    assert result.endswith(".ogg")


def test_greet(capsys):
    main.greet()
    assert capsys.readouterr().out == "Hello from pokecallbunny!\n"


def test_context(capsys):
    with main.Context() as context:
        assert context.con != None
        assert context.cur != None
    assert capsys.readouterr().out == "OpenAL exited\n"


@pytest.fixture
def context():
    return main.Context()


def test_gen_random_pokenumber(context):
    assert context.con != None
    assert context.cur != None

    for _ in range(1000):
        number = main.gen_random_pokenumber(context)
        assert number > 0
        name, _ = main.get_pokemon_by_id(context, number).values()
        assert name != None


def test_get_pokemon_from_db(context):
    data = {
        False: {"pokemon": {"name": None, "formName": None}, "baseID": None},
        "string": {"pokemon": {"name": None, "formName": None}, "baseID": None},
        "pikachu": {"pokemon": {"name": None, "formName": None}, "baseID": None},
        -1: {"pokemon": {"name": None, "formName": None}, "baseID": None},
        0: {"pokemon": {"name": None, "formName": None}, "baseID": None},
        1: {"pokemon": {"name": "bulbasaur", "formName": None}, "baseID": 1},
        150: {"pokemon": {"name": "mewtwo", "formName": None}, "baseID": 150},
        10044: {
            "pokemon": {"name": "mewtwo", "formName": "mewtwo-mega-y"},
            "baseID": 150,
        },
    }
    for num, result in data.items():
        assert main.get_pokemon_by_id(context, num) == result["pokemon"]
        assert main.get_base_form_id(context, num) == result["baseID"]
        assert (
            main.get_first_id_by_pokeName(context, result["pokemon"]["name"])
            == result["baseID"]
        )


def test_play_cry(context, capsys):
    data = [False, True, -1, 0, 1, 100, 1000, 10000, 100000, "string"]
    for val in data:
        main.play_cry(context, val)
        stdout = capsys.readouterr().out
        assert (
            stdout
            == "That number doesn't represent a pokemon known to the scientific community yet. Please try again.\n"
            or stdout.startswith("That was the cry of")
            or stdout.startswith("audio path for alternate form")
        )
