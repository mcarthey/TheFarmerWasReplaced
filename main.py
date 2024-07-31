# Dependencies and priorities
dependencies = [
    (Items.Carrot_Seed, [(Items.Wood, 7), (Items.Hay, 7)]),
    (Items.Pumpkin_Seed, [(Items.Carrot, 3)]),
    (Items.Sunflower_Seed, [(Items.Carrot, 1)]),
    (Items.Cactus_Seed, [(Items.Wood, 5), (Items.Hay, 5)]) 
]

priorities = [
    (Items.Hay, 6000),
    (Items.Carrot, 6000),
    (Items.Pumpkin, 6000),
    (Items.Wood, 6000),
    (Items.Cactus, 6000),
    (Items.Power, 100)
]

# Track sunflower positions and petals
sunflower_positions = {}

# Track cactus positions and sizes
cactus_positions = {}

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
                        do_planting((i,j))
                move(North)
            move(East)

# Harvesting functions
def handle_harvest():
    pos = (get_pos_x(), get_pos_y())
    if get_entity_type() == Entities.Sunflower:
        petals = measure()
        sunflower_positions[pos] = petals
        if all_petals_known():
            max_petals = 0
            for pos_key in sunflower_positions:
                if sunflower_positions[pos_key] > max_petals:
                    max_petals = sunflower_positions[pos_key]
            harvest_all_sunflowers_with_max_petals(max_petals)
    elif get_entity_type() == Entities.Cactus:
        sort_cacti()
        if check_sorted_cacti():
            harvest_all_cacti()
    else:
        harvest()

    # plant something new in the harvested position   
    do_planting(pos)

def all_petals_known():
    for pos_key in sunflower_positions:
        if sunflower_positions[pos_key] == None:
            return False
    return True

def harvest_all_sunflowers_with_max_petals(max_petals):
    keys_to_remove = []
    for pos_key in list(sunflower_positions):
        if sunflower_positions[pos_key] == max_petals:
            move_to(pos_key[0], pos_key[1])
            if get_entity_type() == Entities.Sunflower:
                sunflower_positions[pos_key] = measure() # Update the petals count 
                if sunflower_positions[pos_key] == max_petals:           
                    quick_print("Harvesting sunflower with")
                    quick_print(max_petals)
                    quick_print("petals.")
                    harvest()
                    keys_to_remove.append(pos_key)

    # Remove harvested sunflowers from the dictionary
    for key in keys_to_remove:
        sunflower_positions.pop(key)
        do_planting(key) # Plant something new in the harvested position

def harvest_all_cacti():
    quick_print("Harvesting all cacti.")
    harvest()
    # Clear the cactus_positions dictionary manually
    for key in list(cactus_positions):
        cactus_positions.pop(key)

def sort_cacti():
    sort_rows()
    sort_columns()

def check_sorted_cacti():
    world_size = get_world_size()
    for x in range(world_size):
        for y in range(world_size):
            current_size = measure_at(x, y)
            if (y + 1 < world_size and measure_at(x, y + 1) < current_size or
                x + 1 < world_size and measure_at(x + 1, y) < current_size or
                y - 1 >= 0 and measure_at(x, y - 1) > current_size or
                x - 1 >= 0 and measure_at(x - 1, y) > current_size):
                return False
    return True
  
# Planting functions
def do_planting(position):
    # Move to the specified position
    move_to(position[0], position[1])

    # Check priorities first
    for priority in priorities:
        item, target = priority
        if num_items(item) < target:
            plant_based_on_priority(item, position)
            return

    # If no priorities, determine the most deficient item
    wood_count = num_items(Items.Wood)
    hay_count = num_items(Items.Hay)
    carrot_count = num_items(Items.Carrot)
    pumpkin_count = num_items(Items.Pumpkin)
    power_count = num_items(Items.Power)
    cactus_count = num_items(Items.Cactus)

    min_count = min(wood_count, hay_count, carrot_count, pumpkin_count, power_count, cactus_count)
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
    elif min_count == cactus_count:
        plant_cactus(position)

def plant_based_on_priority(item, position):
    if item == Items.Wood:
        plant_tree_or_bush()
    elif item == Items.Hay:
        plant_grass()
    elif item == Items.Carrot:
        plant_carrot()
    elif item == Items.Pumpkin:
        plant_pumpkin()
    elif item == Items.Cactus:
        plant_cactus(position)
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
            move_back_position(original_position)
            return False
        move_back_position(original_position)
    return True

def plant_tree():
    prepare_ground()
    plant(Entities.Tree)

def plant_sunflower():
    if num_items(Items.Sunflower_Seed) == 0:
        ensure_resources_for(Items.Sunflower_Seed)
        trade(Items.Sunflower_Seed)
    prepare_ground_for_planting()
    plant(Entities.Sunflower)
    update_sunflower_positions()  # Track the sunflower position

def update_sunflower_positions():
    pos = (get_pos_x(), get_pos_y())
    petals = measure()
    sunflower_positions[pos] = petals

def update_cactus_positions(position):
    pos = (get_pos_x(), get_pos_y())
    size = measure()
    cactus_positions[pos] = size

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

def plant_cactus(position):
    if num_items(Items.Cactus_Seed) == 0:
        ensure_resources_for(Items.Cactus_Seed)
        trade(Items.Cactus_Seed)
    prepare_ground_for_planting()
    plant(Entities.Cactus)
    update_cactus_positions(position)

# Helper functions
def something_growing():
    entity = get_entity_type()
    return entity in [Entities.Bush, Entities.Carrots, Entities.Grass, Entities.Pumpkin, Entities.Tree, Entities.Sunflower, Entities.Cactus]

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

def sort_rows():
    world_size = get_world_size()
    for y in range(world_size):
        sorted_row = False
        while not sorted_row:
            sorted_row = True
            for x in range(world_size - 1):
                current_size = measure_at(x, y)
                next_size = measure_at(x + 1, y)
                if current_size > next_size:
                    move_to(x, y)
                    swap(East)
                    sorted_row = False

def sort_columns():
    world_size = get_world_size()
    for x in range(world_size):
        sorted_column = False
        while not sorted_column:
            sorted_column = True
            for y in range(world_size - 1):
                current_size = measure_at(x, y)
                next_size = measure_at(x, y + 1)
                if current_size > next_size:
                    move_to(x, y)
                    swap(North)
                    sorted_column = False

def measure_at(x, y):
    move_to(x, y)
    return measure()
           
# Start managing the farm
manage_farm()