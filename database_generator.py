import requests
import json
import os, os.path
import sqlite3


def connect_to_database(path: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return (connection, cursor)


def create_tables(con: sqlite3.Connection, cur: sqlite3.Cursor):
    with open("database_setup.sql") as file:
        setup = file.read()
        cur.executescript(setup)


def load_pokemon_list() -> dict:
    """returns a dict mapping the name of every pokemon form in the PokeAPI to the url of its data"""
    response = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=10000")
    return dict(json.loads(response.text))["results"]


def load_generation_lists() -> dict:
    """returns a map of all pokemon generations currently in the PokeAPI"""
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
    print("Populating table:")
    pokemon_list = load_pokemon_list()
    generation_lists = load_generation_lists()
    tabledata = []
    for pokemon in pokemon_list:
        apidata = dict(json.loads(requests.get(pokemon["url"]).text))
        species_name = apidata["species"]["name"]
        form_name = apidata["forms"][0]["name"]
        output = {}
        pokeID = (
            pokemon["url"].replace("https://pokeapi.co/api/v2/pokemon/", "").strip("/")
        )
        output["pokeID"] = int(pokeID)
        output["formName"] = form_name if species_name != form_name else None
        output["pokeName"] = species_name
        output["generation"] = None
        for gen in generation_lists:
            if output["pokeName"] in generation_lists[gen]:
                output["generation"] = gen
                break
        if output["generation"] == None:
            raise ValueError("no generation found for ", output)
        output["baseformid"] = (
            apidata["species"]["url"]
            .replace("https://pokeapi.co/api/v2/pokemon-species/", "")
            .strip("/")
        )
        output["latestcry"] = apidata.get("cries", {}).get("latest")
        output["legacycry"] = apidata.get("cries", {}).get("legacy")
        tabledata.append(output)
        print(output)
    insert_new_pokemon(cur, tabledata)


def insert_new_pokemon(cur: sqlite3.Cursor, data):
    # data:list[dict{pokeID: int, pokeName: str, formName: str, generation: int}])-> None
    # type definitions in python are so annoying.
    cur.executemany(
        "INSERT OR IGNORE INTO Pokemon (pokeID, pokeName, formName, generation, baseformid, latestcry, legacycry) VALUES (:pokeID, :pokeName, :formName, :generation, :baseformid, :latestcry, :legacycry)",
        data,
    )


def main():
    con, cur = connect_to_database("./pokemon.db")
    create_tables(con, cur)
    populate_pokemon_table(con, cur)
    con.commit()


if __name__ == "__main__":
    main()
