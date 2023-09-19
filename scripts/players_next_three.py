import json
import re

def extract_player_data(position, airsenal_output):
    # Construct the regular expression pattern based on the position
    pattern = f'{position}:\n(.*?)\n-------------------------'
    
    # Search for the player data
    player_data_match = re.search(pattern, airsenal_output, re.DOTALL)
    
    player_data = []

    if player_data_match:
        # Split the player data into lines
        player_lines = player_data_match.group(1).strip().split('\n')
        
        # Extract all player values
        for line in player_lines:
            # Use regular expressions to extract the desired values
            player_match = re.match(r'\d+\.\s+(.*?),\s+([\d.]+)pts\s+\(£([\d.]+)m,\s+([A-Z]+)\)', line)
            
            if player_match:
                # Create a dictionary for the player
                player = {
                    "name": player_match.group(1),
                    "points": float(player_match.group(2)),
                    "price": f'£{player_match.group(3)}M',
                    "club": player_match.group(4),
                    "type": position
                }
                player_data.append(player)

    return player_data

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Specify the positions you want to extract
positions = ["GK", "DEF", "MID", "FWD"]

# Initialize a dictionary to store player data for each position
player_data_dict = {}

if airsenal_output:
    for position in positions:
        player_data = extract_player_data(position, airsenal_output)
        player_data_dict[position] = player_data

    # Save the player_data_dict to a single JSON file
    with open("player_data_next_three.json", "w") as outfile:
        json.dump(player_data_dict, outfile, indent=4)
    
    print("Player data saved to player_data_next_three.json.")
else:
    print("No AIrsenal output found in the JSON file.")
