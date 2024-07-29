def move_to(x, y):
    while get_pos_x() != x or get_pos_y() != y:
        current_x = get_pos_x()
        current_y = get_pos_y()
        moved = False
        if current_x < x and move(East):
            moved = True
        elif current_x > x and move(West):
            moved = True
        elif current_y < y and move(North):
            moved = True
        elif current_y > y and move(South):
            moved = True
        
        # If no move was successful, break to avoid getting stuck
        if not moved:
            return False
    return True

def move_back_direction(direction):
    if direction == North:
        move(South)
    elif direction == South:
        move(North)
    elif direction == East:
        move(West)
    elif direction == West:
        move(East)


def move_back_position(original_position):
    current_x = get_pos_x()
    current_y = get_pos_y()
    original_x = original_position[0]
    original_y = original_position[1]

    if current_x < original_x:
        move(East)
    elif current_x > original_x:
        move(West)
    elif current_y < original_y:
        move(North)
    elif current_y > original_y:
        move(South)
