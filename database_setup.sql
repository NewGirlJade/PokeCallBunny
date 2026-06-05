
CREATE TABLE IF NOT EXISTS pokemon (
pokeid integer PRIMARY KEY,--Pokemon ID number as found on https://pokeapi.co/api/v2/pokemon
pokename string NOT NULL,--Pokemon base form name
formname string, --none if the pokemon only has one form
generation integer NOT NULL,--generation in which the base form of this pokemon first appears
baseformid string NOT NULL, --ID of the base form of this pokemon, will be the same as pokeid if there aren't any alternate forms
latestcry string,--url to the latest version of the pokemon's cry in PokeAPI if it exists
legacycry string--url to the legacy cry if it exists in PokeAPI
);

CREATE TABLE IF NOT EXISTS guesses (
guessid integer PRIMARY KEY,
timestamp integer NOT NULL,
pokemon integer NOT NULL,
guess string NOT NULL,
is_correct boolean,
FOREIGN key(pokemon) REFERENCES pokemon(pokeid)
);

-- CREATE TABLE IF NOT EXISTS custom_1 (
-- listorder integer PRIMARY KEY,
-- pokemon integer NOT NULL,
-- FOREIGN KEY (pokemon) REFERENCES pokemon(pokeid)
-- );
