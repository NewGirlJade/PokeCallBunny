# PokeCallBunny
Quiz app to aid in my silly goal of memorizing every pokemon cry

# Dependencies
This project uses UV for dependancy management. To get started, clone the repository, install UV according to Astral's directions (https://docs.astral.sh/uv/getting-started/installation/),

Dependencies are declared in pyproject.toml and are automatically installed by UV when running the program with the command:

uv run main.py

It's as simple as that! At least for now.

## Development Notes
questions:
	Do I want this to be a web app? Yes. A Full stack application *french laugh*
	How to map the filenames to pokemon, especially where there are several cries per pokemon
	What's the minimum viable product?
		click a button, hear a random cry, click reveal, see the name. repeat.
	What features would I like in the best case?
		Pictures revealed along with name
		multiple choice of any length or name input
		score keeper and streak records
		ability to pick which generations to test from
		searchable list of all pokemon with each cry associated with each.
		ability to make groups to compare similar sounding calls
		add fainted cries (pitch shifted down)
    spaced repitition
		scoreboard on the right side or something.
	PokeAPI - I think I know how it works, but using it effectively will take some practice and thought.
	Going to start by using the python wrapper PokeBase by Greg Hilmes
	eventually I'm going to take Ben's advice and switch to direct API calls to get more experience with those.
	App structure...
	Things I'm probably going to have to learn in order to make this work:
		(maybe) how to play audio pitchshifted
		(maybe) how much to pitch-shift the audio
		how to make a website with a python backend
		how to use git better
		! How to write tests in python? !
    How to write a fun little program that runs my tests for me
	Settings menu ideas:
		Reset streak
		import/export streak
		volume
		prefer legacy, only legacy, only new versions
		include fainted cries
		ignore alternate forms
		number of multiple choice options
	Pokemon forms are best accessed though pokeapi by going to https://pokeapi.co/api/v2/pokemon-species/
	note the use of species- that's important. Then the forms are at the bottom labeled as "varieties". At least for switchable varieties like tornadus.

Data needed for this project:
Core:
list of pokemon
	numbers
	where to find their sound files
	has_mega
		where to find mega cry soundfile
	alternate_forms
		where to find alternate cry soundfile
OR
list of all pokemon including forms
	- where to find their cry
	- has_alternate_form
	- form name (if other than base form) OR alternate name(s)
	- connections to other pokemon (evolutions, pre-evolutions, alternate forms, mega evolutions)
	- what generation the pokemon belongs to
bonus:
	records of successes & failures
	history of guesses for spaced repitition
	custom cry pool lists
	where to find each form's picture(or pictures for pokemon with multiple forms that share a cry)
	which pokemon all share the same sound file
	
	Glossary:
		Form:
		
