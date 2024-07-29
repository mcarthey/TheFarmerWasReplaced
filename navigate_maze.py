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

        while get_entity_type() == Entities.Treasure:
            if num_items(Items.Fertilizer) == 0:
                trade(Items.Fertilizer)
            use_item(Items.Fertilizer)

            if get_entity_type() != Entities.Treasure:
                quick_print("Regenerated!")
                return True

        for direction in directions:
            dir, dx, dy = direction
            next_x, next_y = x + dx, y + dy

            if (next_x, next_y) not in visited:
                if move_to(next_x, next_y):  # Check if move_to was successful
                    if dfs(next_x, next_y):
                        return True
                    move_back_direction(dir)

        return False

    def find_treasure():
        for i in range(world_size):
            for j in range(world_size):
                if (i, j) not in visited:
                    move_to(i, j)
                    if get_entity_type() == Entities.Hedge:
                        if dfs(i, j):
                            return True
        return False

    # Start the process
    if find_treasure():
        quick_print("Treasure found in the maze!")
    else:
        quick_print("No treasure found in the maze.")

# Call navigate_maze to start the process
SOLVED_COUNT = 10
for s in range(SOLVED_COUNT):
    navigate_maze()
    quick_print("Maze solved:", s + 1, "times")
harvest()
