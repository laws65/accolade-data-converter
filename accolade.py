import copy


accolades = ["gold", "silver", "bronze", "participation",
             "map", "moderation", "github", "community"]

output_data = []

default_player = {
    "name": "",
    "customhead": "",
    "cape": "",
    "gold": [],
    "silver": [],
    "bronze": [],
    "participation": [],
    "github": [],
    "community": [],
    "map": [],
    "moderation": [],
}


medals = ["gold", "silver", "bronze", "participation"]


def is_name(string):
    return string != "" and not string.startswith("\t")


def is_comment(string):
    return string.startswith("#")


with open("input.txt", "r", encoding="utf-8") as input_file:
    input_lines = input_file.readlines()

current_player = copy.deepcopy(default_player)

for i in input_lines:
    i = i.replace("    ", "\t")
    i = i.replace("\n", "")

    if is_comment(i):
        continue

    if is_name(i):
        if current_player["name"] != "": # if isn't default player
            output_data.append(current_player)  # append last player
        new_name = i.split(" =")[0]
        current_player = copy.deepcopy(default_player)
        current_player["name"] = new_name

    elif i.startswith("\t# "):  # is an accolade
        i = i.replace("\t# ", "")
        for accolade in accolades:
            if not i.startswith(accolade):
                continue
            # split string into type and justification
            accolade_type, justification = i.split(" - ", 1)
            accolade_type = accolade_type.split(" ")[0]
            justification = justification.rstrip()
            if accolade_type in medals:
                justification = str(
                    len(current_player[accolade_type])+1) + " - " + justification
            current_player[accolade_type].append(
                justification)  # add to current_player array
    elif i.startswith("\tcustomhead"):
        current_player["customhead"] = i
    elif i.startswith("\tcape"):
        current_player["cape"] = i

output_data.append(current_player)
output_data.sort(key=lambda x: x["name"].lower())

with open("accolade_data.cfg", "w", encoding="utf-8") as output_file:
    output_file.write(
"""# ACCOLADES
# Recognition for contribution and excellence in King Arthur's Gold.
#
# Available accolades + extra info:
#
#     (Functional accolades)
# customhead    - a custom in-game head for some special accolades
#               - tries to find the player head file based on username
#     award date    - unix time, leave 0 for patreon, -1 for permanent
#     months expiry - in 31 day months "for extra fairness", leave 0 for patreon, -1 for permanent
#
# cape          - a royal guard cape for some special accolades
#     award date    - unix time, leave 0 for patreon, -1 for permanent
#     months expiry - in 31 day months "for extra fairness", leave 0 for patreon, -1 for permanent
#
#
#     (Tournament medals)
# gold          - awarded for winning a qualifying tournament
#
# silver        - awarded for placing 2nd in a qualifying tournament
#
# bronze        - awarded for placing 3rd in a qualifying tournament
#
# participation - awarded for participating in a qualifying tournament
#
#
#     (Other significant contributions)
# github        - for submitting a pull request that is accepted on
#                 github or participating in a significant code review
#
# community     - for significant community contributions such as
#                 organising events, making videos, or similar
#
# map           - for making a map for the official map cycle
#
# moderation    - being an admin on the official servers or
#                 a moderator on the discord or forums
#
# Please get in touch if there's some area
# with under-recognised contribution!
#
""")
    for i in output_data:
        output_file.write("\n")
        output_file.write(i["name"] + " =\n")
        if i["customhead"] != "":
            output_file.write(i["customhead"] + "\n")
        if i["cape"] != "":
            output_file.write(i["cape"] + "\n")
        del i["name"]
        del i["customhead"]
        del i["cape"]
        for properties in i:
            if properties == []:
                continue
            # through all justifications of each player data property
            for justification in i[properties]:
                output_file.write(
                    "\t" + properties + "; # " + justification + "\n"
                    )
