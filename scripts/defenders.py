import json
import re

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Initialize defenders_next_three list to store the values as objects
defenders_next_three = []

if airsenal_output:
    # Use regular expressions to find the defenders data
    defenders_data = re.search(r'DEF:\n(.*?)\n-------------------------', airsenal_output, re.DOTALL)

    if defenders_data:
        # Split the defenders data into lines
        defenders_lines = defenders_data.group(1).strip().split('\n')
        
        # Extract all defender values
        for line in defenders_lines:
            # Use regular expressions to extract the desired values
            defender_match = re.match(r'\d+\.\s+([A-Za-z\sá\-]+),\s+([\d.]+)pts\s+\(£([\d.]+)m,\s+([A-Z]+)\)', line)
            
            if defender_match:
                # Create a dictionary for the defender
                defender = {
                    "name": defender_match.group(1),
                    "points": float(defender_match.group(2)),
                    "price": f'£{defender_match.group(3)}M',
                    "club": defender_match.group(4),
                    "type": "DEF"
                }
                defenders_next_three.append(defender)

# Print the defender data
print("Defenders:")
for defender in defenders_next_three:
    print(defender)


# Save the defender data as a JSON file
with open("defenders_next_three.json", "w") as defenders_file:
    json.dump(defenders_next_three, defenders_file, indent=4)

print("Data saved to defenders_next_three.json")
