import requests
import json
import os, os.path
import sqlite3


def non_alternate_forms():
    """this is a list of pokemon with hyphens in their names that don't have alternate forms. it's neccesary because of how I'm parsing pokemon form data into the sql database"""
    return [
        29,
        32,
        122,
        250,
        439,
        474,
        772,
        782,
        783,
        784,
        785,
        786,
        787,
        788,
        866,
        984,
        985,
        986,
        987,
        988,
        989,
        990,
        991,
        992,
        993,
        994,
        995,
        1001,
        1002,
        1003,
        1004,
        1005,
        1006,
        1009,
        1010,
        1020,
        1021,
        1022,
        1023,
    ]


def connect_to_database(path: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return (connection, cursor)


def create_tables(con: sqlite3.Connection, cur: sqlite3.Cursor):
    with open("database_setup.sql") as file:
        setup = file.read()
        cur.executescript(setup)


def load_pokemon_list() -> dict:
    response = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=10000")
    return dict(json.loads(response.text))["results"]


def load_generation_lists() -> dict:
    gen_lists = {}
    response = requests.get("https://pokeapi.co/api/v2/generation/")
    generations = dict(json.loads(response.text))["results"]
    for gen, entry in enumerate(generations):
        response = requests.get(entry["url"])
        gen_data = dict(json.loads(response.text))
        species = gen_data["pokemon_species"]
        just_names = [entry["name"] for entry in species]
        gen_lists[gen + 1] = just_names
    return gen_lists


def populate_pokemon_table(con: sqlite3.Connection, cur: sqlite3.Cursor):
    pokemon_list = load_pokemon_list()
    generation_lists = load_generation_lists()
    tabledata = []
    skip_list = non_alternate_forms()
    for pokemon in pokemon_list:
        output = {}
        pokeID = (
            pokemon["url"].replace("https://pokeapi.co/api/v2/pokemon/", "").strip("/")
        )
        output["pokeID"] = int(pokeID)
        output["formName"] = None
        output["pokeName"] = pokemon["name"]
        output["generation"] = None
        if "-" in output["pokeName"] and output["pokeID"] not in skip_list:
            output["formName"] = output["pokeName"]
            output["pokeName"], _, _ = output["pokeName"].partition("-")
            # I'm special casing these two pokemon in as they have both an alternate form and a hyphen in their name so it breaks the parsing logic a little.
            if output["pokeID"] == 10146:
                output["pokeName"] = "kommo-o"
                output["formName"] = "kommo-o-totem"
            if output["pokeID"] == 10168:
                output["pokeName"] = "mr-mime"
                output["formName"] = "mr-mime-galar"
        for gen in generation_lists:
            if output["pokeName"] in generation_lists[gen]:
                output["generation"] = gen
                break
        if output["generation"] == None:
            raise ValueError("no generation found for ", output)
        tabledata.append(output)
    insert_new_pokemon(cur, tabledata)


def insert_new_pokemon(cur, data):
    cur.executemany(
        "INSERT OR IGNORE INTO Pokemon (pokeID, pokeName, formName, generation) VALUES (:pokeID, :pokeName, :formName, :generation)",
        data,
    )


def main():
    con, cur = connect_to_database("./pokemon.db")
    create_tables(con, cur)
    populate_pokemon_table(con, cur)
    con.commit()


if __name__ == "__main__":
    main()
