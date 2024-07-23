GRASS_MIN = 2000
while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
				do_planting(GRASS_MIN)
			else:
				# default
				if not something_growing():
					plant_grass()
			move(North)
		move(East)

def do_planting(grass_min):
	c = num_items(Items.Carrot)
	h = num_items(Items.Hay)
	w = num_items(Items.Wood)
	p = num_items(Items.Pumpkin)
	
	if h < grass_min:
		plant_grass()
	elif p < c / 2:
		plant_pumpkin()
	else:
		if c < w * 2:
			plant_carrot()
		elif w < h:
			plant_bush()
			
def something_growing():
	if get_entity_type() == Entities.Bush or get_entity_type() == Entities.Carrots or get_entity_type() == Entities.Grass or get_entity_type() == Entities.Pumpkin:
		return True
	return False

def plant_pumpkin():
	if num_items(Items.Pumpkin_Seed) == 0:
		if not have_enough_carrots():
			plant_carrot()
		trade(Items.Pumpkin_Seed)

	if get_ground_type() == Grounds.Turf:
		till()
	if get_ground_type() == Grounds.Soil:
		water_soil()
		plant(Entities.Pumpkin)
						
def plant_carrot():
	if num_items(Items.Carrot_Seed) == 0:
		if not have_enough_wood():
			plant_bush()
		if not have_enough_hay():
			plant_grass()
		trade(Items.Carrot_Seed)
	
	if get_ground_type() == Grounds.Turf:
		till()
	if get_ground_type() == Grounds.Soil:
		water_soil()
		plant(Entities.Carrots)
	
def have_enough_wood():
	if num_items(Items.Wood) > 2:
		return True
	return False

def have_enough_hay():
	if num_items(Items.Hay) > 2:
		return True
	return False

def have_enough_carrots():
	if num_items(Items.Carrot) > 2:
		return True
	return False
		
def plant_bush():
	if get_ground_type() == Grounds.Soil:
		till()
	if get_ground_type() == Grounds.Turf:
		plant(Entities.Bush)

def plant_grass():
	if get_ground_type() == Grounds.Soil:
		till()
	if get_ground_type() == Grounds.Turf:
		plant(Entities.Grass)
		
def water_soil():
	have_water = True
	while have_water and get_water() < .5:
		if num_items(Items.Water_Tank) > 0:
			use_item(Items.Water_Tank)
		else:
			have_water = False
			
	if num_items(Items.Empty_Tank) + num_items(Items.Water_Tank) < 100:
		trade(Items.Empty_Tank)
		