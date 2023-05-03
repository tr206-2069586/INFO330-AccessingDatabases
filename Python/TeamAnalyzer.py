import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters
con = sqlite3.connect("../pokemon.sqlite")

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"
    weakness = []
    strong = []
    print("Analyzing " + arg)
    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    cursor = con.cursor()
    if (arg.isnumeric()):  # This will store the name, type1 and type2 of the pokemone based on it's pokedexid
        name_types = ("SELECT pokemon.name, pokemon_types_view.type1, pokemon_types_view.type2 FROM pokemon JOIN pokemon_types_view ON pokemon.name = pokemon_types_view.name WHERE pokemon.id = " + arg + ";")
        cursor.execute(name_types)
    elif (arg is not None): # This will store the name, type1 and type2 of the pokemone based on it's name
        name_types = ('SELECT pokemon.name, pokemon_types_view.type1, pokemon_types_view.type2 FROM pokemon JOIN pokemon_types_view ON pokemon.name = pokemon_types_view.name WHERE pokemon.name = "' + arg + '";')
        cursor.execute(name_types)
    result = cursor.fetchone()

    # This will pull the type and it's corresponding strength/weakness rating and then store it in the according array
    for type in types:
        sql = ("SELECT pokemon_types_battle_view.against_" + type + " " +
            "FROM pokemon_types_battle_view " +
            "WHERE type1name = '" + result[1] + "' AND type2name = '" + result[2] +"';")
        cursor.execute(sql)
        test = cursor.fetchone()
        if (test[0] > 1.0):
            weakness.append(type)
        elif (test[0] < 1.0):
            strong.append(type)
    # This will print the pokemone name type and it's strengths and weaknesses
    print(result[0] + " (" + result[1] + " " + result[2] + ") " + "is strong against", strong ,"but is weak against", weakness)
con.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")