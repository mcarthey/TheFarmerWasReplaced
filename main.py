# Constants
TARGET_WATER_LEVEL = 0.5  # Adjusted to be more conservative
TANK_CAPACITY = 0.25
MIN_WATER_LEVEL = 0.2  # Water if below this level

# Dependencies
dependencies = [
    (Items.Carrot_Seed, [(Items.Wood, 2), (Items.Hay, 2)]),
    (Items.Pumpkin_Seed, [(Items.Carrot, 1)])
]

# Main management loop
def manage_farm():
    world_size = get_world_size()
    while True:
        for i in range(world_size):
            for j in range(world_size):
                # Check if current position can be harvested
                if can_harvest():
                    harvest()
                    do_planting()
                else:
                    if not something_growing():
                        do_planting()
                move(North)
            move(East)

# Planting functions
def do_planting():
    wood_count = num_items(Items.Wood)
    hay_count = num_items(Items.Hay)
    carrot_count = num_items(Items.Carrot)
    pumpkin_count = num_items(Items.Pumpkin)

    # Find the most deficient item
    min_count = min(wood_count, hay_count, carrot_count, pumpkin_count)
    if min_count == wood_count:
        plant_bush()
    elif min_count == hay_count:
        plant_grass()
    elif min_count == carrot_count:
        plant_carrot()
    elif min_count == pumpkin_count:
        plant_pumpkin()

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
    return entity in [Entities.Bush, Entities.Carrots, Entities.Grass, Entities.Pumpkin]

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
        plant_bush()
    elif item == Items.Hay:
        plant_grass()
    elif item == Items.Carrot:
        plant_carrot()

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
