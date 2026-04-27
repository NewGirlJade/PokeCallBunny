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


def connect_to_database(path: str) -> tuple:
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return (connection, cursor)


def load_generation_lists() -> dict:
    gen_lists = {}
    response = requests.get("https://pokeapi.co/api/v2/generation/")
    generations = dict(json.loads(response.text))["results"]
    for gen, entry in enumerate(generations):
        response = requests.get(entry["url"])
        gen_data = dict(json.loads(response.text))
        species = gen_data["pokemon_species"]
        gen_lists[gen + 1] = species
    return gen_lists


def load_pokemon_list() -> dict:
    response = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=10000")
    return dict(json.loads(response.text))["results"]


def create_table(con, cur):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Pokemon(pokeID integer primary key, pokeName string not null, formName string, generation integer not null)"
    )


def populate_table(con, cur):
    pass


def insert_new(cur, data):
    cur.executemany(
        "INSERT OR IGNORE INTO Pokemon (pokeID, pokeName, formName, generation) VALUES (?,?,?,?)",
        data,
    )


def main():
    con, cur = connect_to_database("./pokemondb.sql")
    create_table(con, cur)
    insert_new(cur, [(618, "Pikchu", "Pika-at", 6), (222, "mawlie", "Mawlie-cute", 1)])
    con.commit()


if __name__ == "__main__":
    main()
