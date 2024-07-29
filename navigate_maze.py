from utils import move_to, move_back_direction

def navigate_maze():
    world_size = get_world_size()
    visited = []
    directions = [
        (North, 0, 1),
        (South, 0, -1),
        (East, 1, 0),
        (West, -1, 0)
    ]

    def dfs(x, y):
        if (x, y) in visited:
            return False
        visited.append((x, y))

        if get_entity_type() == Entities.Treasure:
            quick_print("Found Treasure!")
            return True

        for direction in directions:
            dir, dx, dy = direction
            next_x, next_y = x + dx, y + dy

            if (next_x, next_y) not in visited:
                if move_to(next_x, next_y):  # Check if move_to was successful
                    if dfs(next_x, next_y):
                        return True
                    move_back_direction(dir)  # Only backtrack if the move was successful
        
        return False

    def find_treasure(initial_x, initial_y):
        for direction in directions:
            dir, dx, dy = direction
            next_x, next_y = initial_x + dx, initial_y + dy
            if (next_x, next_y) not in visited:
                if move_to(next_x, next_y):
                    if get_entity_type() == Entities.Hedge:
                        if dfs(next_x, next_y):
                            return True
                    move_to(initial_x, initial_y)  # Return to the starting location if path is not successful
        return False

    # Start the process
    initial_pos_x, initial_pos_y = get_pos_x(), get_pos_y()
    if find_treasure(initial_pos_x, initial_pos_y):
        quick_print("Treasure found in the maze!")
    else:
        quick_print("No treasure found in the maze.")

# Call navigate_maze to start the process
SOLVED_COUNT = 100
for s in range(SOLVED_COUNT):
    navigate_maze()
    quick_print("Maze solved:", s + 1, "times")

    if s < SOLVED_COUNT - 1:
        while get_entity_type() == Entities.Treasure:
            if num_items(Items.Fertilizer) == 0:
                trade(Items.Fertilizer)
            use_item(Items.Fertilizer)

# Harvest after all iterations have completed
harvest()
