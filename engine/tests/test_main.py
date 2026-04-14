import json
import os
import subprocess
import engine.systems
from engine.systems.commands import get_command
import engine.systems.player_logic.player_logic as player_logic
import engine.systems.player_logic.player_func

GAME_MAP = "engine/data/map/game_map.json"
ENTITIES_FILE = "engine/data/entities/entities.json"
MAP_LOGIC = player_logic.DICT_COMMANDS
GAME_COMMANDS = {}

LAYERS = []
RENDER = []
PLAYERS = []

# *****************
# *** FUNCTIONS ***
# *****************

def load(path):
    with open(path, "r") as f:
        return json.load(f)
    
def func_start(prompt, entity, entities):
    command = frozenset(prompt)
    if command in GAME_COMMANDS.keys():
        func_return = GAME_COMMANDS[command](prompt, entity, entities)
        return func_return

# ************
# *** MAIN ***
# ************

def main():
    # --- IMPORTING JSON FILES
    game_map = load(GAME_MAP)
    ENTITIES = load(ENTITIES_FILE)

    while True:
        LAYERS.clear()
        RENDER.clear()
        PLAYERS.clear()

        # --- PUTTING JSON MAP TO LAYERS LIST ---
        z = 0

        for layer, value in game_map.items():
            y = 0

            LAYERS.append([])
            for column in value:
                LAYERS[z].append([])
                for row in column:
                    if row == '0':
                        LAYERS[z][y].append('0')
                    else:
                        LAYERS[z][y].append(row)
                y += 1
            z += 1

        z = 0

        # --- MIXING ALL LAYERS + ENTITIES ---
        for layer in LAYERS:
            y = 0

            for column in layer:
                x = 0
                if z < 1:
                    RENDER.append([])

                for row in column:
                    if x == len(RENDER[y]):
                        RENDER[y].append(row)
                    else:
                        if LAYERS[z][y][x] == '0' and RENDER[y][x] != '0':
                            pass
                        else:
                            RENDER[y][x] = row

                        if ENTITIES[y][x] == 0:
                            x += 1
                            continue
                        elif ENTITIES[y][x][0]['Data']['layer'] == z and y == ENTITIES[y][x][0]['Data']['y'] and x == ENTITIES[y][x][0]['Data']['x']:
                            y_event = ENTITIES[y][x][0]['Data']['y']
                            x_event = ENTITIES[y][x][0]['Data']['x']
                            print("WORKS")
                            print(y_event)
                            print(x_event)
                            RENDER[y][x] = ENTITIES[y_event][x_event][0]['Data']['symbol']

                    x += 1
                y += 1
            z += 1

        # --- EVENT LOGIC CHECK ---
        for column in ENTITIES:
            for row in column:
                if row == 0:
                    continue
                else:
                    for value in row[0]['Logic'].values():
                        if value == None:
                            continue
                        elif value.upper() + "_COMMANDS" in MAP_LOGIC:
                            GAME_COMMANDS.update(MAP_LOGIC[value.upper() + "_COMMANDS"])                 
                    
        # RENDERING
        for y in RENDER:
            for x in y:
                print(x, end=' ')
            print()
            
        # print()
        # for y in ENTITIES:
        #     for x in y:
        #         print(x, end=" ")
        #     print()
            
        # PLAYER LOGIC
        choose = get_command()
        choose = choose.upper()
        for column in ENTITIES:
            for row in column:
                if row == 0:
                    continue
                else:
                    if row[0]['Data']['type'] == 'player':
                        PLAYERS.append(row[0])
        for player in PLAYERS:
            func_start(choose, player, ENTITIES)

if __name__ == '__main__':
    main()