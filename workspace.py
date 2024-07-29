world_size = get_world_size()
for i in range(world_size):
	for j in range(world_size):
		move_to(i,j)
		harvest()