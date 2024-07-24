# Constants
TARGET_WATER_LEVEL = 0.5  # Adjusted to be more conservative
TANK_CAPACITY = 0.25
MIN_WATER_LEVEL = 0.2  # Water if below this level

# Dependencies and priorities
dependencies = [
    (Items.Carrot_Seed, [(Items.Wood, 2), (Items.Hay, 2)]),
    (Items.Pumpkin_Seed, [(Items.Carrot, 1)]),
    (Items.Sunflower_Seed, [(Items.Carrot, 1)]) 
]

priorities = [
    (Items.Hay, 5000),
    (Items.Carrot, 5000),
    (Items.Pumpkin, 80000),
    (Items.Wood, 5000),
    (Items.Power, 100)
]

# Main management loop
def manage_farm():
    world_size = get_world_size()
    while True:
        for i in range(world_size):
            for j in range(world_size):
                # Check if current position can be harvested
                if can_harvest():
                    handle_harvest()
                else:
                    if not something_growing():
                        do_planting()
                move(North)
            move(East)

# Harvesting functions
def handle_harvest():
    if get_entity_type() == Entities.Sunflower:
        petals = measure()
        if petals == 15:
            harvest()
    else:
        harvest()
    do_planting()

# Planting functions
def do_planting():
    # Check priorities first
    for priority in priorities:
        item, target = priority
        if num_items(item) < target:
            plant_based_on_priority(item)
            return

    # If no priorities, determine the most deficient item
    wood_count = num_items(Items.Wood)
    hay_count = num_items(Items.Hay)
    carrot_count = num_items(Items.Carrot)
    pumpkin_count = num_items(Items.Pumpkin)
    power_count = num_items(Items.Power)

    min_count = min(wood_count, hay_count, carrot_count, pumpkin_count, power_count)
    if min_count == wood_count:
        plant_tree_or_bush()
    elif min_count == hay_count:
        plant_grass()
    elif min_count == carrot_count:
        plant_carrot()
    elif min_count == pumpkin_count:
        plant_pumpkin()
    elif min_count == power_count:
        plant_sunflower()

def plant_based_on_priority(item):
    if item == Items.Wood:
        plant_tree_or_bush()
    elif item == Items.Hay:
        plant_grass()
    elif item == Items.Carrot:
        plant_carrot()
    elif item == Items.Pumpkin:
        plant_pumpkin()
    elif item == Items.Power:
        plant_sunflower()

def plant_tree_or_bush():
    if can_plant_tree():
        plant_tree()
    else:
        plant_bush()

def can_plant_tree():
    original_position = (get_pos_x(), get_pos_y())
    
    directions = [North, South, East, West]
    for direction in directions:
        move(direction)
        if get_entity_type() == Entities.Tree:
            move_back(original_position)
            return False
        move_back(original_position)
    return True

def move_back(original_position):
    current_position = (get_pos_x(), get_pos_y())
    if current_position[0] < original_position[0]:
        move(East)
    elif current_position[0] > original_position[0]:
        move(West)
    if current_position[1] < original_position[1]:
        move(North)
    elif current_position[1] > original_position[1]:
        move(South)

def plant_tree():
    prepare_ground()
    plant(Entities.Tree)

def plant_sunflower():
    if num_items(Items.Sunflower_Seed) == 0:
        ensure_resources_for(Items.Sunflower_Seed)
        trade(Items.Sunflower_Seed)
    prepare_ground_for_planting()
    plant(Entities.Sunflower)

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

# Helper functions
def something_growing():
    entity = get_entity_type()
    return entity in [Entities.Bush, Entities.Carrots, Entities.Grass, Entities.Pumpkin, Entities.Tree, Entities.Sunflower]

def have_enough(item, amount):
    return num_items(item) >= amount

def ensure_resources_for(seed):
    for dependency in dependencies:
        dep_seed, dep_list = dependency
        if seed == dep_seed:
            for requirement in dep_list:
                item, amount = requirement
                if not have_enough(item, amount):
                    plant_based_on_resource(item)

def plant_based_on_resource(item):
    if item == Items.Wood:
        plant_tree_or_bush()
    elif item == Items.Hay:
        plant_grass()
    elif item == Items.Carrot:
        plant_carrot()
    elif item == Items.Power:
        plant_sunflower()

def prepare_ground_for_planting():
    ground_type = get_ground_type()
    if ground_type == Grounds.Turf:
        till()
    if ground_type == Grounds.Soil:
        water_soil()

def prepare_ground():
    ground_type = get_ground_type()
    if ground_type == Grounds.Turf:
        till()
    # No need to water soil for bushes or grass

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

# Start managing the farm
manage_farm()
