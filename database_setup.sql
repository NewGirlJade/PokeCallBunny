
CREATE TABLE IF NOT EXISTS pokemon (
pokeid integer PRIMARY KEY,--Pokemon ID number as found on https://pokeapi.co/api/v2/pokemon
pokename string NOT NULL,--Pokemon name (not including form)
formname string, --if a pokemon has multiple forms, this should contain
generation integer NOT NULL--generation in which the base form of this pokemon first appears
);

CREATE TABLE IF NOT EXISTS guesses (
guessid integer PRIMARY KEY,
timestamp integer NOT NULL,
pokemon integer NOT NULL,
guess string NOT NULL,
is_correct boolean,
FOREIGN key(pokemon) REFERENCES pokemon(pokeid)
);

CREATE TABLE IF NOT EXISTS custom_1 (
listorder integer PRIMARY KEY,
pokemon integer NOT NULL,
FOREIGN KEY (pokemon) REFERENCES pokemon(pokeid)
);