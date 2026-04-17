def eight_move_direction(arg, entity, _):
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