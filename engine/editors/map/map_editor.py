import os
import json
from ...systems.commands import get_command
from engine.core.exceptions import NoJsonFile, Back
from ...creators.map import tools
import engine.utils.terminal as terminal
import state

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
        self.game_map = game_map
        self.layers_game_map = game_map.keys()
        self.textures = textures

        self.layer_choosed = None
        self.texture_choosed = None
        self.tool_choosed = None

    def run(self):
        while True:
            print("Choose: Layer/Te-Texture/To-Tool/Edit/Map/Save")
            menu_choice = get_command()
            menu_choice = menu_choice.strip().upper()
            match menu_choice:
                case 'L' | 'LAYER':
                    self.get_layer()
                case 'TE' | 'TEXTURE':
                    self.get_texture()
                case 'TO' | 'TOOL':
                    self.get_tool()
                case 'E' | 'EDIT':
                    if None in (self.texture_choosed, self.texture_choosed, self.tool_choosed):
                        print("Before edit, please choose layer, texture and tool")
                    else:
                        self.edit()
                case 'M' | 'MAP':
                    self.show_map()
                case 'S' | 'SAVE':
                    self.save()
                case _:
                    print("Wrong choose.")
            return

    def get_layer(self):
        while True:
            print(self.layers_game_map)
            print("Choose layer:\n")
            layer = get_command()
            if layer in (self.layers_game_map):
                self.layer_choosed = layer
                return 
            else:
                print('Wrong choose.\n')

    def get_texture(self):
        while True:
            print(self.textures)
            print("Choose texture name:\n")
            texture = get_command()
            if texture in (self.textures):
                self.texture_choosed = self.textures[texture]
                return
            else:
                print('Wrong choose.\n')

    def get_tool(self):
        while True:
            print("Choose: Pointer/Liner/Square")
            tool = get_command()
            tool = tool.strip().upper()
            match tool:
                case 'P' | 'POINTER':
                    self.tool_choosed = 'pointer'
                    return
                case 'L' | 'LINER':
                    self.tool_choosed = 'liner'
                    return
                case 'S' | 'SQUARE':
                    self.tool_choosed = 'square'
                    return
                case _:
                    print("Wrong choose.\n")

    def edit(self):
        terminal.clear()
        print("\nTYPE 'B' OR 'BACK' TO EXIT\n")
        def enter_yx(arg):
            while True:
                print(f"Enter {arg}'Y', 'X':")
                pos = get_command()
                pos = pos.strip().upper()
                if pos in ('B', 'BACK'):
                    return pos, pos
                else:
                    pos = tuple(map(int, pos.split(',')))

                    if pos[0] < 0 or pos[0] >= len(self.game_map[self.layer_choosed]):
                        print("Invalid 'Y'")
                    elif pos[1] < 0 or pos[1] >= len(self.game_map[self.layer_choosed][0]):
                        print("Invalid 'X'")
                    else:
                        y = pos[0]
                        x = pos[1]
                        return y, x

        while True:
            for column in self.game_map[self.layer_choosed]:
                for row in column:
                    print(row, end=" ")
                print()
            match self.tool_choosed:
                case 'pointer':
                    y, x = enter_yx('')
                    if y in ('B', 'BACK') or x in ('B', 'BACK'):
                        return

                    pointer = tools.Pointer(y, x)
                    pointer.place(self.game_map[self.layer_choosed], self.texture_choosed)
                
                case 'liner': 
                    fy, fx = enter_yx('first ')
                    if fy in ('B', 'BACK') or fx in ('B', 'BACK'):
                        return
                    sy, sx = enter_yx('second ')
                    if sy in ('B', 'BACK') or sx in ('B', 'BACK'):
                        return

                    liner = tools.Liner(fy, fx, sy, sx)
                    liner.place(self.game_map[self.layer_choosed], self.texture_choosed)
                 
                case 'square':
                    fy, fx = enter_yx('first ')
                    if fy in ('B', 'BACK') or fx in ('B', 'BACK'):
                        return
                    sy, sx = enter_yx('second ')
                    if sy in ('B', 'BACK') or sx in ('B', 'BACK'):
                        return

                    square = tools.Square(fy, fx, sy, sx)
                    square.place(self.game_map[self.layer_choosed], self.texture_choosed)

    def show_map(self):
        while True:
            print("Choose: All/One")
            print("Do you want to print all layers or only one layer?")
            choice = get_command()
            choice = choice.strip().upper()
            match choice:
                case 'A' | 'ALL':
                    for n, layer in self.game_map.items():
                        print(f"Layer: {n}\n")
                        for column in layer:
                            for row in column:
                                print(row, end=" ")
                            print()
                        print()
                    return
                case 'O' | 'ONE':
                    print([k for k in self.game_map.keys()])
                    print("Choose layer:")
                    layer = get_command()
                    if layer not in self.game_map.keys():
                        print("Invalid number.\n")
                    else:
                        print()
                        for column in self.game_map[layer]:
                            for row in column:
                                print(row, end=" ")
                            print()
                        print()
                    return
                case _:
                    print('Wrong choice.')

    def save(self):
        while True:
            print("Choice: Yes/No")
            print("Do you want to save? It will overwrite previous map.")
            choice = get_command()
            choice = choice.strip().upper()
            match choice:
                case 'Y' | 'YES':
                    data = self.game_map
                    path = map_path()

                    with open(path, 'w') as f:
                        json.dump(data, f, indent=4)
                    return
                case 'N' | 'NO':
                    return
                case _:
                    print("Invalid choice.\n")

def map_path():
    return f"{state.state.path}/data/map/game_map.json"

def load(file):
    if not os.path.exists(file):
        raise NoJsonFile()
    
    with open(file, "r") as f:
        return json.load(f)

# ************
# *** MAIN ***
# ************

def main():
    game_map = load(MAP_PATH)
    test = EditMap(game_map, TEXTURES)
    test.run()

if __name__ == '__main__':
    main()