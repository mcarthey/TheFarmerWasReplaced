from utils import move_to, move_back_direction, water_soil

def plant_pumpkin():
    if num_items(Items.Pumpkin_Seed) == 0:
        trade(Items.Pumpkin_Seed)
    if get_ground_type() == Grounds.Turf:
        till()
    if get_ground_type() == Grounds.Soil:
        water_soil()
    plant(Entities.Pumpkin)

def check_and_plant_pumpkin(tracked_positions):
    world_size = get_world_size()
    for i in range(world_size):
        for j in range(world_size):
            move_to(i, j)
            entity_type = get_entity_type()
            if entity_type != Entities.Pumpkin and entity_type != Entities.Treasure:
                plant_pumpkin()
                tracked_positions.append((i, j))

def replant_pumpkins(tracked_positions):
    new_tracked_positions = []
    for position in tracked_positions:
        i, j = position
        move_to(i, j)
        if get_entity_type() != Entities.Pumpkin:
            plant_pumpkin()
            new_tracked_positions.append((i, j))
    return new_tracked_positions

def is_field_filled_with_pumpkins():
    world_size = get_world_size()
    for i in range(world_size):
        for j in range(world_size):
            move_to(i, j)
            if get_entity_type() != Entities.Pumpkin:
                return False
    return True

def manage_pumpkin_field():
    tracked_positions = []
    check_and_plant_pumpkin(tracked_positions)
    quick_print("Initial planting complete.")
    quick_print("Tracking positions of replanted pumpkins.")

    while tracked_positions:
        tracked_positions = replant_pumpkins(tracked_positions)
        quick_print("Replanted pumpkins where necessary.")
        quick_print("Remaining positions to check:")
        quick_print(len(tracked_positions))
        # Optionally, you might want to wait for some time before checking again
        # This is to allow the pumpkins to grow and potentially die if you want to replant in waves
        # sleep(60)  # Example: wait for 60 seconds

# Start the process
manage_pumpkin_field()

# Harvesting once the field is filled with pumpkins
if is_field_filled_with_pumpkins():
    quick_print("Field filled with pumpkins. Harvesting!")
    move_to(0, 0)  # Move to a known location to start harvesting
    if can_harvest():
        harvest()
