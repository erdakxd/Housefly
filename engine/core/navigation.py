import engine.core.exceptions as exceptions
from engine.systems.commands import get_command
import engine.utils.terminal as terminal
import test_game
import engine.creators.character.character_creator as character_creator
import engine.creators.map.map_creator as map_creator
import engine.creators.event.event_creator as event_creator
import engine.editors.map.map_editor as map_editor
import engine.editors.character.character_editor as character_editor
import engine.editors.event.event_editor as event_editor
import engine.entities.entities as entities
import engine.core.new_project as new_project

stack = []

class Menu:
    path = None

    def run(self):
        pass

# ---------------------------------------------------------------------------------------------------------------------

# *****************
# *** MAIN MENU ***
# *****************

class MainMenu(Menu):
    def run(self):
        terminal.clear()
        print("INFO: YOU CAN TYPE FIRST LETTER FROM OPTIONS AS A SHORTCUT.\nDOESN'T MATTER IF IT IS LOWER OR UPPER CASE.\n")
        while True:
                            
            print("Choose: Creator/Ed-Editor/En-Entities/Test Game")
            choose = get_command("Which creator you want to use?:\n")
            choose = choose.strip().upper()
            print()

            match choose:
                case 'C' | 'CREATOR':
                    stack.append(CreatorsMenu())
                    return

                case 'ED' | 'EDITOR':
                    stack.append(EditorsMenu())
                    return
                                
                case 'EN' | 'ENTITIES':
                    stack.append(EntitiesMap())
                    return
                                
                case 'T' | 'TEST GAME':
                    stack.append(TestGame())
                    return

                case _:
                    print(f"'{choose}' is a incorrect choose. Please choose only character or map.")

# *****************
# *** TEST GAME ***
# *****************

class TestGame(Menu):
    def run(self):
        test_game.main()
        stack.pop()
        return

# *********************
# *** ENTITIES MENU ***
# *********************

class EntitiesMap(Menu):
    def __init__(self):
        self.game_map = None
        self.events = None
        self.event = None

    def run(self):
        self.game_map = entities.load(entities.GAME_MAP)
        entities.entities_size(self.game_map)
        
        self.event = entities.menu_entities(self.events, self.event, self.game_map)
        stack.pop()
        return

# *********************
# *** CREATORS MENU ***
# *********************

class CreatorsMenu(Menu):
    def __init__(self):
        self.game_map = None

    def run(self):
        while True:
            print("Choose: Character/Map/Event")
            choose = get_command("Which creator you want to use?:\n")
            choose = choose.strip().upper()

            match choose:
                case 'C' | 'CHARACTER':
                    stack.append(CharacterCreator())
                    return

                case 'M' | 'MAP':
                    self.game_map = map_creator.GameMap
                    self.game_map.y = None
                    self.game_map.x = None
                    self.game_map.game_map = {}
                    stack.append(MapCreator(self.game_map))
                    return

                case 'E' | 'EVENT':
                    stack.append(EventCreator())
                    return

                case _:
                    print(f"'{choose}' is a incorrect choose. Please choose only character or map.")

# ***************
# *** EDITORS ***
# ***************

class EditorsMenu(Menu):
    def run(self):
        print("Choose: Map/Players/Ene-Enemies/Ev-Event")
        choose = get_command("Which editor you want to use?:\n")
        choose = choose.strip().upper()

        match choose:
            case 'M' | 'MAP':
                game_map = map_editor.load(map_editor.MAP_PATH)
                stack.append(map_editor.EditMap(game_map, map_editor.TEXTURES))
                return
            
            case 'P' | 'PLAYERS':
                stack.append(CharacterEditor("engine/data/players/players.json"))
                return

            case 'ENE' | 'ENEMIES':
                stack.append(CharacterEditor("engine/data/enemies/enemies.json"))
                return
            
            case 'EV' | 'EVENT':
                stack.append(EventEditor())
                return

            case _:
                print(f"'{choose}' is a incorrect choose. Please choose only character or map.")
    
# ^^^^^^^^^^^^^^^^^^^^
# ^^^ EVENT EDITOR ^^^
# ^^^^^^^^^^^^^^^^^^^^

class EventEditor(Menu):
    def __init__(self):
        self.choose = None
        self.path = None

    def run(self):
        choose = event_editor.choose_event()
        if choose in ('P', 'PlAYERS', 'E', 'ENEMIES', 'O', 'OBJECTS'):
            self.choose, self.path = event_editor.initial_choice(choose)
            stack.append(ChoiceEvent(self.choose, self.path))
            return

# ^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^ CHARACTER EDITOR ^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^

class CharacterEditor(Menu):
    def __init__(self, path):
        self.check = True
        self.character_path = path

    def run(self):
        character_dict = character_editor.load_map(self.character_path)

        if self.check:
            terminal.clear()
            self.check = False

        choose = character_editor.set_edit(character_dict)
        stack.append(EditCharacter(character_dict, choose, self.character_path))
        return

# ^^^^^^^^^^^^^^^^^^^^^
# ^^^ EVENT CREATOR ^^^
# ^^^^^^^^^^^^^^^^^^^^^

class EventCreator(Menu):
    def run(self):
        choose = event_creator.new_event()
        data = event_creator.print_dict(choose)
        event = event_creator.create_event(data)
        event.get_export()
        stack.pop()
        return

# ^^^^^^^^^^^^^^^^^^^
# ^^^ MAP CREATOR ^^^
# ^^^^^^^^^^^^^^^^^^^

class MapCreator(Menu):
    def __init__(self, game_map):
        self.game_map = game_map
        self.check = True

    def run(self):
        if self.check:
            terminal.clear()
            self.check = False
        
        while True:
            print("Choose: Layers/Size/Game Map/Clear/Export")
            choose = get_command("What do you want to change?:\n")
            choose = choose.strip().upper()
            match choose:
                case 'L' | 'LAYERS':
                    stack.append(Layer(self.game_map, None))
                    return
                case 'S' | 'SIZE':
                    stack.append(Size(self.game_map))
                    return
                case 'G' | 'GAME MAP':
                    stack.append(ShowDict(self.game_map))
                    return
                case 'C' | 'CLEAR':
                    stack.append(Clear(self.game_map))
                    return
                case 'E' | 'EXPORT':
                    stack.append(Export(self.game_map))
                    return
                case _:
                    print(f"\n{choose} is a incorrect choose.\n")
    
# ^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^ CHARACTER CREATOR ^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^

class CharacterCreator(Menu):
    def __init__(self):
        self.character = None

    def run(self):
        while True:
            print(f'Choose: Player/Enemy')
            choose = get_command("Enter a character you want to create:\n")
            choose = choose.strip().upper()
            match choose:
                case 'P' | 'PLAYER':
                    self.character = character_creator.Player
                    self.character.name = "None"
                    self.character.symbol = "None"
                    self.character.vision = 7
                    stack.append(Character(self.character))
                    return
            
                case 'E' | 'ENEMY':
                    self.character = character_creator.Enemy
                    self.character.name = "None"
                    self.character.symbol = "None"
                    self.character.vision = 7
                    stack.append(Character(self.character))
                    return
                
                case _:
                    print(f"'{choose}' is not correct choose. Please choose player or enemy.\n")

# --------------------
# --- CHOICE EVENT ---
# --------------------

class ChoiceEvent(Menu):
    def __init__(self, file, path):
        self.file = file
        self.path = path

        self.event = None
        self.event_name = None

    def run(self):
        self.event, self.event_name = event_editor.menu_event_choice(self.file)
        stack.append(EditEvent(self.file, self.path, self.event, self.event_name))
        return

class EditEvent(Menu):
    def __init__(self, file, path, event, event_name):
        self.file = file
        self.path = path
        self.event = event
        self.event_name = event_name
        self.action_choice = None

    def run(self):
        self.action_choice = event_editor.menu_action_choice()
        stack.append(FieldChoiceEvent(self.file, self.path, self.event, self.event_name, self.action_choice))
        return

class FieldChoiceEvent(Menu):
    def __init__(self, file, path, event, event_name, action_choice):
        self.file = file
        self.path = path
        self.event = event
        self.event_name = event_name
        self.action_choice = action_choice
        self.field_choice = None

    def run(self):
        self.field_choice = event_editor.menu_field_choice(self.action_choice, self.event, self.event_name)
        print(self.field_choice)
        if self.field_choice in ('S', 'SAVE'):
            event_editor.save(self.file, self.event_name, self.path)
            stack.pop()
            return
        else:
            stack.append(Edit('event', self.field_choice, self.event, self.event_name, self.action_choice))
            return
    
# ----------------------
# --- EDIT CHARACTER ---
# ----------------------

class EditCharacter(Menu):
    def __init__(self, character_dict, character, file_path):
        self.character_dict = character_dict
        self.character = character
        self.file_path = file_path
        self.check = True
    def run(self):
        if self.check:
            terminal.clear()
            self.check = False

        choose = character_editor.character_edit(self.character, self.character_dict)
        if choose in ('s', 'save'):
            stack.append(SaveForEdit(self.character_dict, self.character, self.file_path))
        else:
            stack.append(Edit('character', choose, self.character, self.character_dict))
        return

# -------------------------
# --- CHARACTER CREATOR ---
# -------------------------

class Character(Menu):
    def __init__(self, character):
        self.character = character
        self.check = True

    def run(self):
        if self.check:
            terminal.clear()
            self.check = False
        while True:
            print("Choose: Name/Sy-Symbol/Vision/Dictionary/Sa-Save/Clear/Export")
            choose = get_command("What do you want to change?:\n")
            choose = choose.strip().upper()
            match choose:
                case 'N' | 'NAME':
                    stack.append(Name(self.character))
                    return
                case 'SY' | 'SYMBOL':
                    stack.append(Symbol(self.character))
                    return
                case 'V' | 'VISION':
                    stack.append(Vision(self.character))
                    return
                case 'D' | 'DICTIONARY':
                    stack.append(ShowDict(self.character))
                    return
                case 'SA' | 'SAVE':
                    stack.append(Save(self.character))
                    return
                case 'C' | 'CLEAR':
                    stack.append(Clear(self.character))
                    return
                case 'E' | 'EXPORT':
                    stack.append(Export(self.character))
                    return
                case _:
                    print(f"\n{choose} is a incorrect choose.\n")

# ---------------------
# --- EVENT CREATOR ---
# ---------------------
class Event(Menu):
    pass

# --- GENERAL CLASSES ---

class Edit(Menu):
    def __init__(self, editor, choose, character, dictionary, action_choice):
        self.editor = editor
        self.choose = choose
        self.character = character
        self.dictionary = dictionary
        self.action_choice = action_choice

    def run(self):
        match self.editor:
            case 'character':
                edit_choose = character_editor.edit(self.choose, self.character, self.dictionary)
                self.dictionary[self.character][self.choose] = edit_choose
                stack.pop()
                return
            case 'event':
                edit_choose = event_editor.edit(self.choose, self.character, self.action_choice)
                match self.action_choice:
                    case 'D' | 'DATA':
                        self.character['Data'][self.choose] = edit_choose
                    case 'L' | 'LOGIC':
                        self.character['Logic'][self.choose] = edit_choose
                stack.pop()
                return

class Name(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            self.character.name = character_creator.get_name('player')
        elif self.character == character_creator.Enemy:
            self.character.name = character_creator.get_name('enemy')
        stack.pop()
        terminal.clear()
        return

class Symbol(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            self.character.symbol = character_creator.get_symbol('player')
        elif self.character == character_creator.Enemy:
            self.character.symbol = character_creator.get_symbol('enemy')
        stack.pop()
        terminal.clear()
        return

class Vision(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            self.character.vision = character_creator.get_vision('player')
        elif self.character == character_creator.Enemy:
            self.character.vision = character_creator.get_vision('enemy')
        stack.pop()
        terminal.clear()
        return
    
class SaveForEdit(Menu):
    def __init__(self, dictionary, character, file_path):
        self.dictionary = dictionary
        self.character = character
        self.file_path = file_path

    def run(self):
        check = character_editor.save(self.dictionary, self.character, self.file_path)
        if check:
            stack.pop()
        stack.pop()
        return
    
class Save(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        try:
            if self.character == character_creator.Player:
                character_creator.Player(self.character.name, self.character.symbol, self.character.vision)
            elif self.character == character_creator.Enemy:
                character_creator.Enemy(self.character.name, self.character.symbol, self.character.vision)
            self.character.name = None
            self.character.symbol = None
            self.character.vision = 7
        except AttributeError:
            terminal.clear
            print("They are some none element characters. Please set every element for character")
            stack.pop()
            return
        stack.pop()
        terminal.clear()
        return

class Delete(Menu):
    pass

class Clear(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        print("Choose: Yes/No")
        choose = get_command("Do you want to clear dictionary?:\n")
        choose = choose.strip().upper()
        match choose:
            case 'Y' | 'YES':
                if self.character == map_creator.GameMap:
                    self.character.game_map.clear()
                else:
                    self.character.characters.clear()
                terminal.clear()
            case 'N' | 'NO':
                terminal.clear()
            case _:
                terminal.clear()
                print("Wrong choose.\n")
        stack.pop()
        return

class ShowDict(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == map_creator.GameMap:
            map_creator.render_map()
        else: 
            character_creator.get_character_dict(self.character.characters)
        stack.pop()
        return

class Export(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            character_creator.get_export('players', character_creator.Player.characters)    
        elif self.character == character_creator.Enemy:
            character_creator.get_export('enemies', character_creator.Enemy.characters)
        elif self.character == map_creator.GameMap:
            map_creator.get_export('game_map', self.character.game_map)
        stack.pop()
        return

class Size(Menu):
    def __init__(self, game_map):
        self.game_map = game_map

    def run(self):
        if self.game_map == map_creator.GameMap:
            self.game_map.y = map_creator.map_position_xy('y')
            self.game_map.x = map_creator.map_position_xy('x')
            map_creator.game_size('0')
        stack.pop()
        terminal.clear()
        return

class Layer(Menu):
    def __init__(self, game_map, layer):
        self.game_map = game_map
        self.layer = layer

    def run(self):
        if self.game_map == map_creator.GameMap:
            map_creator.get_layer()

        else:
            self.layer = map_editor.set_layer(self.game_map)
        stack.pop()
        terminal.clear()
        return

class Texture(Menu):
    def __init__(self, editor):
        self.editor = editor

    def run(self):
        self.editor.texture = map_editor.set_texture()
        stack.pop()
        return

class Tool(Menu):
    def __init__(self, editor):
        self.editor = editor

    def run(self):
        self.editor.tool = map_editor.set_tool()
        stack.pop()
        return

class GameMap(Menu):
    def __init__(self, editor):
        self.editor = editor

    def run(self):
        self.editor.game_map = map_editor.edit_map()
        stack.pop()
        return

# ************
# *** MAIN ***
# ************

def main():
    while True:
        try:
            if Menu.path == None:
                stack.append(new_project.Project())
                current = stack[-1]
                current.run()
                Menu.path = current.path
            else:
                stack.clear()
                break

        except exceptions.Back:
            stack.pop(-1)
        except exceptions.ExitDebugger:
            pass
        except exceptions.NoJsonFile:
            print('No Json File.')
            stack.pop(-1)
        except exceptions.ExitMenu:
            stack.clear()
            stack.append(MainMenu())

    stack.append(MainMenu())

    while stack:
        try:
            current = stack[-1]
            current.run()

        except exceptions.Back:
            stack.pop(-1)
        except exceptions.ExitDebugger:
            pass
        except exceptions.NoJsonFile:
            print('No Json File.')
            stack.pop(-1)
        except exceptions.ExitMenu:
            stack.clear()
            stack.append(MainMenu())


if __name__ == '__main__':
    main()