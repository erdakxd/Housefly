def eight_move_direction(arg, entity, entities):
    MOVE_MAP = {
        frozenset(("W")): (-1, 0),
        frozenset(("S")): (1, 0),
        frozenset(("A")): (0, -1),
        frozenset(("D")): (0, 1),
        frozenset(("A", "W")): (-1, -1),
        frozenset(("D", "W")): (-1, 1),
        frozenset(("A", "S")): (1, -1),
        frozenset(("D", "S")): (1, 1),
    }

    # --- NEW MOVEMENT ---
    arg = frozenset(arg)
    cords = MOVE_MAP.get(arg, (0,0))

    entity['Data']['y'] += cords[0]
    entity['Data']['x'] += cords[1]

    return

    # --- OLD MOVEMENT --- XDDDD
    # y_entities = 0
    # for column in entities:
    #     x_entities = 0
    #     for row in column:
    #         if row != 0:
                
    #             entities[y_entities][x_entities][0]['Data']['y'] += cords[0]
    #             entities[y_entities][x_entities][0]['Data']['x'] += cords[1]
                
    #             new_y_entities = y_entities + cords[0]
    #             new_x_entities = x_entities + cords[1]
    #             old_y_entities = y_entities
    #             old_x_entities = x_entities

    #             entities[new_y_entities][new_x_entities] = [entity]
    #             entities[old_y_entities][old_x_entities].remove(entity)
    #             if entities[old_y_entities][old_x_entities] == []:
    #                 entities[old_y_entities][old_x_entities] = 0
                    
    #             return

    #         x_entities += 1
    #     y_entities += 1


# def player_movement(player_y, player_x, y_arg, x_arg):
#     new_y = player_y + y_arg
#     new_x = player_x + x_arg
#     if new_y < 0 or new_y >= len_map_y or new_x < 0 or new_x >= len_map_x:
#         print("You can't move!")
#     elif entities[new_y][new_x] in entities_objects:
#         print("You can't move!")
#     else:
#         entities[player_y][player_x] = ""
#         player_y = player_y + y_arg
#         player_x = player_x + x_arg
#         entities[player_y][player_x] = player
#     return player_y, player_x

MAP_FUCNTION = {"eight_move_direction": eight_move_direction}