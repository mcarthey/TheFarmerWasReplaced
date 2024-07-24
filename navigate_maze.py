def navigate_maze():
    world_size = get_world_size()
    m_visited = []

    def m_dfs(x, y):
        if (x, y) in m_visited:
            return False
        m_visited.append((x, y))

        if get_entity_type() == Entities.Treasure:
            quick_print("Treasure found!")
            harvest()
            return True

        # Try moving in all directions
        directions = [North, South, East, West]
        for d in range(4):
            if move(directions[d]):
                next_x, next_y = get_pos_x(), get_pos_y()
                if m_dfs(next_x, next_y):
                    return True
                m_move_back(directions[d])
        
        return False

    def m_move_back(direction):
        if direction == North:
            move(South)
        elif direction == South:
            move(North)
        elif direction == East:
            move(West)
        elif direction == West:
            move(East)

    def m_move_to(x, y):
        while get_pos_x() != x:
            if get_pos_x() < x:
                move(East)
            else:
                move(West)
        while get_pos_y() != y:
            if get_pos_y() < y:
                move(North)
            else:
                move(South)

    # Start DFS from each tile to find the treasure
    for i in range(world_size):
        for j in range(world_size):
            m_move_to(i, j)
            if get_entity_type() == Entities.Hedge:
                if m_dfs(i, j):
                    return

# Call navigate_maze after maze is generated
navigate_maze()
