import json
import os
from engine.core.exceptions import NoJsonFile
from engine.systems.commands import get_command

# *****************
# *** VARIABLES ***
# *****************

PLAYERS = "engine/data/events/events_players.json"
ENEMIES = "engine/data/events/events_enemies.json"
OBJECTS = "engine/data/events/events_objects.json"

# ***************
# *** CLASSES ***
# ***************

class EventEdit():
    def __init__(self, data):
        self.data = data

# *****************
# *** FUNCTIONS ***
# *****************

def load(path_load):
    if not os.path.exists(path_load):
        raise NoJsonFile()
    
    with open(path_load, "r") as f:
        return json.load(f)
    
def choose_event():
    while True:
        print("Choose: Players/Enemies/Objects")
        choose = get_command()
        choose = choose.strip().upper()
        if choose in ('P', 'PLAYERs', 'E', 'ENEMIES', 'O', 'OBJECTS'):
            return choose
        else:
            print("Wrong choose.\n")

def initial_choice(choose):
    match choose:
        case 'P' | 'PLAYERS':
            file = load(PLAYERS)
            file_path = PLAYERS
        case 'E' | 'ENEMIES':
            file = load(ENEMIES)
            file_path = ENEMIES
        case 'O' | 'OBJECTS':
            file = load(OBJECTS)
            file_path = OBJECTS
    return file, file_path

def menu_event_choice(file):
    while True:
        print([k for k in file])
        print("Choose event.")
        event_choice = get_command()
        for key in file:
            check = False
            if event_choice == key:
                event = file[key]
                event_name = key
                return event, event_name

        if not check:
            print("Wrong choose.\n")

def menu_action_choice():
    while True:
        print("Choose: Data/Logic/Save")
        action_choice = get_command()
        action_choice = action_choice.strip().upper()

        if action_choice in ('D', 'DATA', 'L', 'LOGIC', 'S', 'SAVE'):
            return action_choice
        else:
            print("Wrong choose.\n")
        
def menu_field_choice(action_choice, event, event_name):
    while True:
        match action_choice:
            case 'D' | 'DATA':
                print([key for key in event['Data'].keys()])
                print("\nWhat you want to edit?\n")
                field_choice = get_command()
                field_choice = field_choice.strip()

                for key in event['Data']:
                    if field_choice == key:
                        return field_choice

                print("Wrong choose.\n")       
                        
            case 'L' | 'LOGIC':
                print([key for key in event['Logic'].keys()])
                print("\nWhat you want to edit?\n")
                field_choice = get_command()
                field_choice = field_choice.strip()

                for key in event['Logic']:
                    if field_choice == key:
                        return field_choice

                print("Wrong choose.\n")   

            case 'S' | 'SAVE':
                return action_choice
            
def edit(choose, event, action_choice):
    while True:
        print(f"Edit {choose}")
        value_edit = get_command() 
        try:
            match action_choice:
                case 'D' | 'DATA':
                    if type(event['Data'][choose]) == type(1):
                        value_edit = int(value_edit)
                        if value_edit < 0:
                            print("Invalide number. You can type only whole numbers and at least 0.\n")
                            continue
                    return value_edit
                case 'L' | 'LOGIC':
                    if type(event['Logic'][choose]) == type(1):
                        value_edit = int(value_edit)
                        if value_edit < 0:
                            print("Invalide number. You can type only whole numbers and at least 0.\n")
                            continue
                    return value_edit

        except ValueError:
            print("Invalide number. You can type only whole numbers and at least 0.\n")

def save(dictionary, character, file_path):
    while True:
        print("Choose: Yes/No")
        choose = get_command("Do you want to save character? It will change Json file.:\n")
        choose = choose.strip().upper()
        match choose:
            case 'Y' | 'YES':
                # try:
                    new_key = character

                    dictionary[new_key] = dictionary.pop(character)
                    data = dict(sorted(dictionary.items()))

                    with open(file=file_path, mode="w") as file:
                        json.dump(data, file, indent=4)

                        print("Json file was created.\n")
                    return True
                # except Exception:
                #     print("Something went wrong.\n")
                # return False
            case 'N' | 'NO':
                return False
            case _:
                print("Wrong choose.\n")

# ************
# *** MAIN ***
# ************

def main():
    pass

if __name__ == '__main__':
    main()