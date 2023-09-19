import json
import re

# Load the AIrsenal data from the JSON file
with open("result.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Initialize GK_next_three list to store the values as objects
GK_next_three = []

if airsenal_output:
    # Use regular expressions to find the GK data
    gk_data = re.search(r'GK:\n(.*?)\n-------------------------', airsenal_output, re.DOTALL)

    if gk_data:
        # Split the GK data into lines
        gk_lines = gk_data.group(1).strip().split('\n')

        # Initialize the type to 'GK'
        current_type = 'GK'

        # Extract all goalkeeper values using the provided regex pattern
        for gk_line in gk_lines:
            if gk_line.startswith('---'):
                # Change the type for the next section
                if current_type == 'GK':
                    current_type = 'DEF'
                elif current_type == 'DEF':
                    current_type = 'MID'
                elif current_type == 'MID':
                    current_type = 'FWD'
            else:
                # Use the provided regex pattern to extract the desired values
                gk_match = re.match(r'(\d+)\.\s+([A-Za-z\sá]+),\s+([\d.]+)pts\s+\(£([\d.]+)m,\s+([A-Z]+)\)', gk_line)

                if gk_match:
                    # Extract the values
                    gk_number = gk_match.group(1).strip()
                    gk_name = gk_match.group(2).strip()
                    gk_points = float(gk_match.group(3))
                    gk_price = '£' + gk_match.group(4).strip() + 'M'
                    gk_club = gk_match.group(5).strip()

                    # Create a dictionary for the goalkeeper
                    gk_dict = {
                        'number': gk_number,
                        'name': gk_name,
                        'points': gk_points,
                        'price': gk_price,
                        'club': gk_club,
                        'type': current_type  # Add the type to the dictionary
                    }

                    # Add the goalkeeper dictionary to the list
                    GK_next_three.append(gk_dict)

else:
    print("No AIrsenal data found in the JSON file.")

# Print the GK_next_three dictionaries
print("Goalkeepers:")
for gk in GK_next_three:
    print(gk)

# Save GK_next_three as a JSON file
with open("goalkeepers.json", "w") as goalkeepers_file:
    json.dump(GK_next_three, goalkeepers_file, indent=4)

print("Goalkeepers saved to goalkeepers.json")
