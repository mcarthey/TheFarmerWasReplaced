GRASS_MIN = 2000

while True:
    for i in range(get_world_size()):
        for j in range(get_world_size()):
            if can_harvest():
                harvest()
                do_planting(GRASS_MIN)
            else:
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
    entity = get_entity_type()
    if entity == Entities.Bush or entity == Entities.Carrots or entity == Entities.Grass or entity == Entities.Pumpkin:
        return True
    return False

def plant_pumpkin():
    if num_items(Items.Pumpkin_Seed) == 0:
        if not have_enough_carrots():
            plant_carrot()
        trade(Items.Pumpkin_Seed)

    prepare_ground_for_planting()
    plant(Entities.Pumpkin)

def plant_carrot():
    if num_items(Items.Carrot_Seed) == 0:
        if not have_enough_wood():
            plant_bush()
        if not have_enough_hay():
            plant_grass()
        trade(Items.Carrot_Seed)
    
    prepare_ground_for_planting()
    plant(Entities.Carrots)

def have_enough_wood():
    return num_items(Items.Wood) >= 2

def have_enough_hay():
    return num_items(Items.Hay) >= 2

def have_enough_carrots():
    return num_items(Items.Carrot) >= 1

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
    have_water = True
    while have_water and get_water() < .5:
        if num_items(Items.Water_Tank) > 0:
            use_item(Items.Water_Tank)
        else:
            have_water = False
            
    if num_items(Items.Empty_Tank) + num_items(Items.Water_Tank) < 100:
        trade(Items.Empty_Tank)

def prepare_ground():
    ground_type = get_ground_type()
    if ground_type == Grounds.Turf:
        till()
    # No need to water soil for bushes or grass
