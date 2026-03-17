# PokeCallBunny
Quiz app to aid in my silly goal of memorizing every pokemon cry


## Development Notes
questions:
	Do I want this to be a web app? Yes. A Full stack application *french laugh*
	How to map the filenames to pokemon, especially where there are several calls per pokemon
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
	PokeAPI - I think I know how it works, but using it effectively will take some practice and thought.
	going to use the python wrapper PokeBase by Greg Hilmes
	for my purposes, I could probably just build a json using pokeAPI for all the pokemon I need and then I wouldn't have to hit their servers.
	App structure...
	Things I'm probably going to have to learn in order to make this work:
		How to play audio from python
		(maybe) how to play audio pitchshifted
		(maybe) how much to pitch-shift the audio
		how to make a website with a python backend and/or
		how to use git better
		! How to write tests in python? !
    How to write a fun little program that runs my tests for me

		To do next:
        wireframe the website - diagram
        pick out a tech stack for the app (vanilla HTML, python api framework (look at flask, fast API, dJango, others?))
        add tooling around tests and dependencies (UV)
        List of dependencies
