import binascii
import random

def calculate_treasure_locations(mountain_name, mountain_height):
    """Returns list of (elevation, horizontal_position) for all 5 treasures"""
    random.seed(binascii.crc32(mountain_name.encode('utf-8')))
    prev_height = mountain_height
    prev_horiz = 0
    locations = []
    
    for i in range(5):
        e_delta = random.randint(200, 800)  # Vertical change
        h_delta = random.randint(int(-e_delta/4), int(e_delta/4))  # Horizontal change
        elevation = prev_height - e_delta
        horiz = prev_horiz + h_delta
        
        # Store as (elevation, horizontal_position)
        locations.append((elevation, horiz))
        
        prev_height = elevation
        prev_horiz = horiz
    
    return locations

# Constants from the game
skier_start = 5

# All 7 mountains from the game
mountains = [
    ('Mount Snow', 3586),
    ('Aspen', 11211),
    ('Whistler', 7156),
    ('Mount Baker', 10781),
    ('Mount Norquay', 6998),
    ('Mount Erciyes', 12848),
    ('Dragonmount', 16282)
]

# Calculate and print treasure locations for all mountains
for mountain_name, mountain_height in mountains:
    locations = calculate_treasure_locations(mountain_name, mountain_height)
    print(f"\n{'='*60}")
    print(f"{mountain_name} (Height: {mountain_height})")
    print(f"Treasure locations (elevation, horizontal):")
    print(f"{'-'*60}")
    
    for i, (elev, horiz) in enumerate(locations):
        print(f"  Treasure {i+1}:")
        print(f"    Elevation: {elev}")
        print(f"    Horizontal: {horiz}")
        print(f"    Elevation diff from initial position = {mountain_height - elev - skier_start}")

