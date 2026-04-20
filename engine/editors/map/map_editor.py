import os
import json
from ...systems.commands import get_command
from engine.core.exceptions import NoJsonFile
from ...creators.map import tools
import engine.utils.terminal as terminal

MAP_PATH = "engine/data/map/game_map.json"

TILES = {
    "floor": {"solid": False},
    "wall": {"solid": True}
}
MAP_TILES = {}
    
TEXTURES = {
    'wall': "X",
    'floor': "•"
}

class EditMap:
    def __init__(self, game_map, textures):
        self.game_map = game_map['1']
        self.layers_game_map = game_map.keys()
        self.textures = textures

        self.layer_choosed = None
        self.texture_choosed = None
        self.tool_choosed = None
        self.edited_map = []

    @staticmethod
    def menu():
        while True:
            menu_choice = print("Choose: Layer/Te-Texture/To-Tool/Edit/Map/Save")
            manu_choice = menu_choice.strip().upper()
            if menu_choice in ('L', 'LAYER', 'TE', 'TEXTURE', 'TO', 'TOOL', 'E', 'EDIT', 'M', 'MAP', 'S', 'SAVE'):
                return menu_choice
            else:
                print("Wrong choose.")

    def get_layer(self):
        while True:
            print(self.layers_game_map)
            print("Choose layer:")
            layer = get_command()
            if layer in (self.layers_game_map):
                self.layer_choosed = layer
                return 
            else:
                print('Wrong choose.\n')

def load_map():
    if not os.path.exists(MAP_PATH):
        raise NoJsonFile()
    
    with open(MAP_PATH, "r") as f:
        return json.load(f)

def menu():
    while True:
        menu_choice = print("Choose: Layer/Te-Texture/To-Tool/Edit/Map/Save")
        manu_choice = menu_choice.strip().upper()
        if menu_choice in ('L', 'LAYER', 'TE', 'TEXTURE', 'TO', 'TOOL', 'E', 'EDIT', 'M', 'MAP', 'S', 'SAVE'):
            return menu_choice
        else:
            print("Wrong choose.\n")

def layer():
    while True:
        pass
    
    
repeat = True
layer = '2'
tool = "POINTER"

wall = "X"
floor = "•"
textures = (wall, floor)
texture = "•"

# len_map_y = len(game_map['1'])
# len_map_x = len(game_map['1'][0])

def set_layer(game_map):    
    while True:
        print(f"Choose: {game_map.keys()}")
        layer = get_command("Which layer you want to edit?:\n")
        try:
            for k in game_map.keys():
                if layer == k:
                    return layer
                elif layer > max(game_map.keys()) or layer < min(game_map.keys()):
                    print(f"Invalid number! You can choose only these layers: {game_map.keys()}.\n")
                    break
        except Exception:
            print("Invalid number! Type only whole numbers.\n")
            terminal.clear()

def set_texture():
    while True:
        n = 0
        print(f"List of textures:\n")
        for t in textures:
            n += 1
            print(f"{n}. {t}")

        try:
            print(f"\nChoose: from 1 to {len(textures)}")
            texture = get_command("Which texture you choose?:\n")
            texture = int(texture)
            if texture in (1, 2):
                texture = textures[texture-1]
                return texture
            else:
                print(f"'{texture}' is a incorrect texture. You can choose from 1 to {len(textures)}")

        except Exception:
            print(f"Invalid texture. You can choose from 1 to {len(textures)}")
            terminal.clear()

def set_tool():
    pass

def edit_map():
    pass 

def get_export():
    pass

# ************
# *** MAIN ***
# ************

def main():
    game_map = load_map()
    test = EditMap(game_map, TEXTURES)
    print(test.get_layer())

if __name__ == '__main__':
    main()