from engine.core.colision import colision

def eight_move_direction(arg, entity, _, layers):
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
    entity_layer = entity['Data']['layer']
    entity_y = entity['Data']['y'] + cords[0]
    entity_x = entity['Data']['x'] + cords[1]
    try:
        texture = layers[entity_layer][entity_y][entity_x]
        if entity_y | entity_x < 0:
            return
    except IndexError:
        return

    if texture in colision.keys() and colision[texture] == True:
        return
    else:
        entity['Data']['y'] += cords[0]
        entity['Data']['x'] += cords[1]
        return
    
# def raycasting():
#     def bresenham(y1, x1, y2, x2):
#         points = []

#         dy = abs(y1 - y2)
#         dx = abs(x1 - x2)

#         sy = 1 if y1 < y2 else -1
#         sx = 1 if x1 < x2 else -1

#         err = dx - dy

#         while True:
#             points.append((y1, x1))


#             if y1 == y2 and x1 == x2:
#                 break

#             e2 = 2 * err

#             if e2 > -dy:
#                 err -= dy
#                 x1 += sx

#             if e2 < dx:
#                 err += dx
#                 y1 += sy

#         return points

#     def is_visible(y1, x1, y2, x2):
#         line = bresenham(y1, x1, y2, x2)
#         for (y, x) in line:
#             if (y, x) == (y1, x1):
#                 continue
#             if y < 0 or y >= len_map_y or x < 0 or x >= len_map_x:
#                 return False
#             if entities[y][x] == wall:
#                 return (y, x) == (y2, x2) # Z False działa również ale zostaw z celem

#         return True