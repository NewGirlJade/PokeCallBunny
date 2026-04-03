import pokebase as pb
from pokebase import cache

chesto = pb.APIResource("berry", "chesto")
print(chesto.name)
print(chesto.natural_gift_type.name)

charmander = pb.pokemon("charmander")  # Quick lookup.
print(charmander)

print(pb.APIResource("pokemon", 7))

# s1 = pb.SpriteResource("pokemon", 17)
# s2 = pb.SpriteResource("pokemon", 1, other=True, official_artwork=True)
# s3 = pb.SpriteResource("pokemon", 3, female=True, back=True)
# print("1: " + s1 + " 2: " + s2 + " 3: " + s3)

# View Pokemon from this generation number.
GENERATION = 2

# Get API data associated with that particular generation.
gen_resource = pb.generation(GENERATION)

# Iterate through the list of Pokemon introduced in that generation.
for pokemon in gen_resource.pokemon_species:
    print(pokemon.name.title())
