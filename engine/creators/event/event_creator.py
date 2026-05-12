# KLASA EVENT -> PUSTY
# JSON -> DANE I TRIGERY
# PYTHON -> LOGIKA
# 
# Aktualny kreator:
# - Sprite
# - Możliwość wklejenia logiki
# - Łączenie Danych z Json
#
import json
import os
from ...systems.commands import get_command
import engine.utils.terminal as terminal
import state

# *****************
# *** VARIABLES ***
# *****************




# ***************
# *** CLASSES ***
# ***************

class EventCreator():
    def __init__(self, data, logic):
        self.data = data
        self.logic = logic

    def get_export(self):
        for value in self.data.values():
            e_type = value['type']
            break
        match e_type:
            case 'player':
                file_path = f"{state.state.path}/data/events/events_players.json" 
            case 'enemy':
                file_path = f"{state.state.path}/data/events/events_enemies.json" 
            case 'object':
                file_path = f"{state.state.path}/data/events/events_objects.json"

        data = {}
        for key, value in self.data.items():
            data[key] = {'Data': value, 'Logic': self.logic}

        with open(file=file_path, mode="w") as file:
            json.dump(data, file, indent=4)

            print("Json file was created.\n")

# *****************
# *** FUNCTIONS ***
# *****************

def player_path():
    return f"{state.state.path}/data/players/players.json"

def enemy_path():
    return f"{state.state.path}/data/enemies/enemies.json"


def new_event():
    while True:
        print("Choose: Player/En-Enemy/Em-Empty")
        choose = get_command("Which template for event you want to create?:\n")
        choose = choose.strip().upper()
        if choose in ("P", "PLAYER", "EN", "ENEMY", "EM", "EMPTY"):
            return choose
        else:
            print("Wrong choose.\n")

def print_dict(choose):
    data = {}
    n = 1
    while True:
        if choose in ("P", "PLAYER"):
            player_json = player_path()
            print(data)
            with open(player_json, "r") as f:
                players = json.load(f)
            print([player for player in players])
            character = get_command("Choose created character\n")
            if character in ([k for k in players.keys()]):
                name = players[character]['name']
                data[f"{n}. {name}"] = players[character]
                print("Choose: Yes/No\n")
                another = get_command("Do you want to add another character as event?:\n")
                another = another.strip().upper()
                match another:
                    case 'Y' | 'YES':
                        n += 1
                    case 'N' | 'NO':
                        return data
                    case _:
                        print("Wrong choose.")
            else:
                print("Wrong choose.\n")

        elif choose in ("EN", "ENEMY"):
            enemy_json = enemy_path()
            with open(enemy_json, "r") as f:
                enemies = json.load(f)
            print([enemy for enemy in enemies])
            character = get_command("Choose created character\n")
            if character in ([k for k in enemies.keys()]):
                name = enemies[character]['name']
                data[f"{n}. {name}"] = enemies[character]
                print("Choose: Yes/No\n")
                another = get_command("Do you want to add another character as event?:\n")
                another = another.strip().upper()
                match another:
                    case 'Y' | 'YES':
                        n += 1
                    case 'N' | 'NO':
                        return data
                    case _:
                        print("Wrong choose.")
            else:
                print("Wrong choose.\n")

        elif choose in ("EM", "EMPTY"):
            print("How many?")
            ammount = get_command()
            try:
                ammount = int(ammount)
            except Exception:
                print("Wrong number. You can type only whole numbers")
            return empty_data(), ammount

def create_event(data):
    return EventCreator(data, empty_logic())

def empty_data():
    return {"name": None,
            "id": None,
            "type": "object",
            "priority": 1,
            "layer": 1,
            "symbol": None,
            "y": 0,
            "x": 0
            }

def empty_logic():
    return {"movement": None,
            "pathfinding": None,
            "condition": None
            }

def data_import(path_load):
    with open(path_load, "r") as f:
        return json.load(f)

# ************
# *** MAIN ***
# ************

def main():
    # data = data_import(PLAYER_PATH)
    # player = EventCreator(data, '')

    # print([character for character in player.data])
    # character = get_command("Enter character.\n")
    # player.set_sprite(character)
    # player1 = EventCreator(empty_data(), empty_logic())

    # player1.data['name'] = 'One'

    # player1.get_export()

    choose = new_event()
    data = print_dict(choose)
    player = create_event(data)
    player.logic['movement'] = 'eight_move_direction'
    player.get_export()

if __name__ == '__main__':
    main()