GRASS_MIN = 2000

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
    quick_print("Checking if we have enough of", item, ":", num_items(item), "needed:", amount)
    return num_items(item) >= amount

def ensure_resources_for(seed):
    quick_print("Ensuring resources for", seed)
    for dependency in dependencies:
        dep_seed, dep_list, _ = dependency
        if seed == dep_seed:
            for requirement in dep_list:
                item, amount = requirement
                while not have_enough(item, amount):
                    quick_print("Need more", item, "for", seed, ", planting necessary resources...")
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
                quick_print("Harvesting...")
                harvest()
                do_planting(GRASS_MIN)
            else:
                if not something_growing():
                    quick_print("Nothing growing, planting grass...")
                    plant_grass()
            move(North)
        move(East)

def do_planting(grass_min):
    quick_print("Doing planting...")
    if need_hay(grass_min):
        quick_print("Need hay, planting grass...")
        plant_grass()
    elif need_to_plant(Items.Pumpkin_Seed):
        quick_print("Need pumpkin, planting pumpkin...")
        plant_pumpkin()
    elif need_to_plant(Items.Carrot_Seed):
        quick_print("Need carrot, planting carrot...")
        plant_carrot()
    else:
        quick_print("Default action, planting bush...")
        plant_bush()

def something_growing():
    entity = get_entity_type()
    quick_print("Checking if something is growing:", entity)
    return entity in [Entities.Bush, Entities.Carrots, Entities.Grass, Entities.Pumpkin]

def plant_pumpkin():
    quick_print("Planting pumpkin...")
    if num_items(Items.Pumpkin_Seed) == 0:
        ensure_resources_for(Items.Pumpkin_Seed)
        trade(Items.Pumpkin_Seed)
    
    prepare_ground_for_planting()
    plant(Entities.Pumpkin)
    quick_print("Planted pumpkin.")

def plant_carrot():
    quick_print("Planting carrot...")
    if num_items(Items.Carrot_Seed) == 0:
        ensure_resources_for(Items.Carrot_Seed)
        trade(Items.Carrot_Seed)
    
    prepare_ground_for_planting()
    plant(Entities.Carrots)
    quick_print("Planted carrot.")

def plant_bush():
    quick_print("Planting bush...")
    prepare_ground()
    plant(Entities.Bush)
    quick_print("Planted bush.")

def plant_grass():
    quick_print("Planting grass...")
    prepare_ground()
    plant(Entities.Grass)
    quick_print("Planted grass.")

def prepare_ground_for_planting():
    ground_type = get_ground_type()
    quick_print("Preparing ground for planting:", ground_type)
    if ground_type == Grounds.Turf:
        till()
    if ground_type == Grounds.Soil:
        water_soil()

def water_soil():
    quick_print("Watering soil...")
    have_water = True
    while have_water and get_water() < 0.5:
        if num_items(Items.Water_Tank) > 0:
            use_item(Items.Water_Tank)
        else:
            have_water = False
            
    if num_items(Items.Empty_Tank) + num_items(Items.Water_Tank) < 100:
        trade(Items.Empty_Tank)

def prepare_ground():
    ground_type = get_ground_type()
    quick_print("Preparing ground:", ground_type)
    if ground_type == Grounds.Turf:
        till()
    # No need to water soil for bushes or grass
