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

def water_soil():
    # Constants
    TARGET_WATER_LEVEL = 0.5  # Adjusted to be more conservative
    TANK_CAPACITY = 0.25
    MIN_WATER_LEVEL = 0.2  # Water if below this level

    water_level = get_water()
    if water_level < MIN_WATER_LEVEL:
        needed_water = TARGET_WATER_LEVEL - water_level
        tanks_needed = needed_water / TANK_CAPACITY
        # Use tanks only up to a certain limit to conserve resources
        max_tanks_to_use = 5  # Adjust as necessary to balance water usage
        tanks_used = 0
        while tanks_used < tanks_needed and tanks_used < max_tanks_to_use:
            if num_items(Items.Water_Tank) > 0:
                use_item(Items.Water_Tank)
                tanks_used += 1
            else:
                break
    if num_items(Items.Empty_Tank) + num_items(Items.Water_Tank) < 100:
        trade(Items.Empty_Tank)