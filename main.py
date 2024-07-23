GRASS_MIN = 2000
TARGET_WATER_LEVEL = 0.5  # Adjusted to be more conservative
TANK_CAPACITY = 0.25
MIN_WATER_LEVEL = 0.2  # Water if below this level

# Define dependencies and conditions using lists of tuples
dependencies = [
    (Items.Carrot_Seed, [(Items.Wood, 2), (Items.Hay, 2)], 'need_carrot'),
    (Items.Pumpkin_Seed, [(Items.Carrot, 1)], 'need_pumpkin')
]

def need_hay(grass_min):
    return num_items(Items.Hay) < grass_min

def need_pumpkin():
    # Plant pumpkins when the number of pumpkins is less than half the number of carrots
    pumpkins = num_items(Items.Pumpkin)
    carrots = num_items(Items.Carrot)
    return pumpkins < (carrots / 2)

def need_carrot():
    # Plant carrots when the number of carrots is less than the number of wood and hay combined
    carrots = num_items(Items.Carrot)
    wood = num_items(Items.Wood)
    hay = num_items(Items.Hay)
    return carrots < (wood + hay)

def have_enough(item, amount):
    return num_items(item) >= amount

def ensure_resources_for(seed):
    for dependency in dependencies:
        dep_seed, dep_list, _ = dependency
        if seed == dep_seed:
            for requirement in dep_list:
                item, amount = requirement
                while not have_enough(item, amount):
                    if item == Items.Wood:
                        plant_bush()
                    elif item == Items.Hay:
                        plant_grass()
                    elif item == Items.Carrot:
                        plant_carrot()

def need_to_plant(seed):
    for dependency in dependencies:
        dep_seed, _, condition = dependency
        if seed == dep_seed:
            if condition == 'need_carrot':
                return need_carrot()
            elif condition == 'need_pumpkin':
                return need_pumpkin()
    return False

while True:
    for row in range(get_world_size()):
        for col in range(get_world_size()):
            if can_harvest():
                harvest()
                do_planting(GRASS_MIN)
            else:
                if not something_growing():
                    plant_grass()
            move(North)
        move(East)

def do_planting(grass_min):
    if need_hay(grass_min):
        plant_grass()
    elif need_to_plant(Items.Pumpkin_Seed):
        plant_pumpkin()
    elif need_to_plant(Items.Carrot_Seed):
        plant_carrot()
    else:
        plant_bush()

def something_growing():
    entity = get_entity_type()
    return entity in [Entities.Bush, Entities.Carrots, Entities.Grass, Entities.Pumpkin]

def plant_pumpkin():
    if num_items(Items.Pumpkin_Seed) == 0:
        ensure_resources_for(Items.Pumpkin_Seed)
        trade(Items.Pumpkin_Seed)
    
    prepare_ground_for_planting()
    plant(Entities.Pumpkin)

def plant_carrot():
    if num_items(Items.Carrot_Seed) == 0:
        ensure_resources_for(Items.Carrot_Seed)
        trade(Items.Carrot_Seed)
    
    prepare_ground_for_planting()
    plant(Entities.Carrots)

def plant_bush():
    prepare_ground()
    plant(Entities.Bush)

def plant_grass():
    prepare_ground()
    plant(Entities.Grass)

def prepare_ground_for_planting():
    ground_type = get_ground_type()
    if ground_type == Grounds.Turf:
        till()
    if ground_type == Grounds.Soil:
        water_soil()

def water_soil():
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

def prepare_ground():
    ground_type = get_ground_type()
    if ground_type == Grounds.Turf:
        till()
    # No need to water soil for bushes or grass
