import json
import re

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Initialize gameweek list
gameweeks = []

if airsenal_output:
    # Use regular expressions to find the "Gameweek" sections
    gameweek_matches = re.finditer(r'Gameweek (\d+) ={3,}\n+([\s\S]+?)(?=\n\n ===========|$)', airsenal_output, re.DOTALL)

    for gameweek_match in gameweek_matches:
        # Extract the gameweek number
        gameweek_number = int(gameweek_match.group(1))

        # Extract the remaining content
        gameweek_content = gameweek_match.group(2).strip()

        # Split the content into lines
        gameweek_lines = gameweek_content.split('\n')

        # Initialize gameweek data
        gameweek_data = {
            "gameweek": gameweek_number,
            "chips_played": "None",
            "players_in": [],
            "players_out": []
        }

        # Check if there are enough lines to extract "Chips played" and player information
        if len(gameweek_lines) > 4:
            # Extract "Chips played" information from the second line
            chips_played = gameweek_lines[0].strip()
            gameweek_data["chips_played"] = chips_played

            # Extract "Players in" and "Players out" information
            players_in_line = gameweek_lines[4]
            players_in_out = players_in_line.split('\t\t\t')

            # Remove empty strings
            players_in_out = [p.strip() for p in players_in_out if p.strip()]

            # Separate player data into players_in and players_out
            gameweek_data["players_in"] = players_in_out[::2]  # Every even index is a player in
            gameweek_data["players_out"] = players_in_out[1::2]  # Every odd index is a player out

        # Append the gameweek data to the list
        gameweeks.append(gameweek_data)

# Ensure there are three gameweeks, adding empty data if needed
while len(gameweeks) < 3:
    gameweeks.append({
        "gameweek": len(gameweeks) + 5,
        "chips_played": "None",
        "players_in": [],
        "players_out": []
    })

# Print the gameweek data
print(json.dumps(gameweeks, indent=4))
# Specify the output file name
output_file = "gameweeks.json"

# Save the gameweeks array to the JSON file
with open(output_file, "w") as outfile:
    json.dump(gameweeks, outfile, indent=4)

print(f"Data saved to {output_file}")