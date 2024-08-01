from utils import move_to, swap, measure_at

def quicksort_cactus_positions(q_cactus_positions):
    items = list(q_cactus_positions)

    def partition(arr, low, high):
        i = (low - 1)
        pivot = arr[high][1]

        for j in range(low, high):
            if arr[j][1] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return (i + 1)

    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)

            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    quick_sort(items, 0, len(items) - 1)
    return items

def sort_and_place_cacti(s_cactus_positions):
    sorted_positions = quicksort_cactus_positions(s_cactus_positions)
    world_size = get_world_size()

    index = 0
    for sorted_position in sorted_positions:
        pos, size = sorted_position
        target_x = index % world_size
        target_y = index // world_size
        move_and_swap(pos[0], pos[1], target_x, target_y)
        index += 1

def move_and_swap(from_x, from_y, to_x, to_y):
    move_to(from_x, from_y)
    move_to(to_x, to_y)
    swap()
