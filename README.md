# PokeCallBunny
Quiz app to aid in my silly goal of memorizing every pokemon cry

# Getting started
1. clone the repository
2. install UV according to Astral's directions (https://docs.astral.sh/uv/getting-started/installation/)
3. Build your Pokemon database by running:
		`uv run database_generator.py`
		**NOTE** This will take a while to complete
4. (optional) Run tests by running:
		`uv run pytest'
5. Get started memorizing with:
		`uv run core.py
x. If you get stuck, the core loop almost always takes help as an argument. Good luck, have fun!

# Dependencies
This project uses UV for dependancy management.

Dependencies are declared in pyproject.toml and are automatically installed by UV when running the program with the command:

uv run core.py
It's as simple as that! At least for now.


## Development Notes
The project is in a good spot right now. A website hosting a prettier version of the app is in the early design stages right now, but isn't my top priority at the moment.
		
Settings menu ideas:
		Reset streak
		import/export streak
		volume
		prefer legacy, only legacy, only new versions
		include fainted cries
		ignore alternate forms
		number of multiple choice options
