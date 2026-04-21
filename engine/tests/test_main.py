import json
import engine.systems
import engine.utils.terminal as terminal
from engine.systems.commands import get_command
import engine.systems.player_logic.player_logic as player_logic
import engine.systems.ai_logic.ai_logic as ai_logic

GAME_MAP = "engine/data/map/game_map.json"
ENTITIES_FILE = "engine/data/entities/entities.json"
MAP_LOGIC = player_logic.DICT_COMMANDS
GAME_COMMANDS = {}
AI_LOGIC = ai_logic.AI_LOGIC

# *****************
# *** FUNCTIONS ***
# *****************

def load(path):
    with open(path, "r") as f:
        return json.load(f)
    
def func_start(prompt, entity, entities, game_map, target, layers):
    command = frozenset(prompt)
    if command in GAME_COMMANDS.keys():
        func_return = GAME_COMMANDS[command](prompt, entity, entities, layers)
        return func_return
    if prompt == 'AI':
        for value in entity['Logic'].values(): 
            if value in AI_LOGIC.keys():
                func_return = AI_LOGIC[value](entity, entities, game_map, target)
                return func_return
        

# ************
# *** MAIN ***
# ************

def main():
    # --- IMPORTING JSON FILES
    game_map = load(GAME_MAP)
    ENTITIES = load(ENTITIES_FILE)
    LAYERS = []
    RENDER = []
    PLAYERS = []
    ENEMIES = []

    while True:
        terminal.clear()

        LAYERS.clear()
        RENDER.clear()
        PLAYERS.clear()
        ENEMIES.clear()

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
                        for entity in ENTITIES:
                            e = entity['Data']
                            if e['layer'] == z and e['y'] == y and e['x'] == x:
                                RENDER[y][x] = e['symbol']

                        if LAYERS[z][y][x] == '0' and RENDER[y][x] != '0':
                            pass
                        else:
                            RENDER[y][x] = row

                    x += 1
                y += 1
            z += 1

        # --- EVENT LOGIC CHECK ---
        for entity in ENTITIES:
            for value in entity['Logic'].values():
                if value == None:
                    continue
                elif value + "_commands" in MAP_LOGIC:
                    GAME_COMMANDS.update(MAP_LOGIC[value + "_commands"])    
                    
        # RENDERING
        for y in RENDER:
            for x in y:
                print(x, end=' ')
            print()
            
        # LOGIC
        choose = get_command()
        choose = choose.upper()
        for entity in ENTITIES:
            if entity['Data']['type'] == 'player':
                PLAYERS.append(entity)
            if entity['Data']['type'] == 'enemy':
                ENEMIES.append(entity)

        for player in PLAYERS:
            func_start(choose, player, ENTITIES, RENDER, "_", LAYERS)
            
        for enemy in ENEMIES:
            func_start('AI', enemy, ENTITIES, RENDER, PLAYERS[0], LAYERS)


if __name__ == '__main__':
    main()