import random

def random_movement(event, _, game_map):

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, -1), (1, 1), (-1, 1)
    ]
    
    dy, dx = random.choice(directions)
    
    pos_y = event['Data']['y']
    pos_x = event['Data']['x']
    
    new_dy = pos_y + dy
    new_dx = pos_x + dx

    if new_dy < 0 or new_dy >= len(game_map) or new_dx < 0 or new_dx >= len(game_map[0]):
        return
    else:
        event['Data']['y'] += dy
        event['Data']['x'] += dx
        return
    