import json
import re

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Initialize midfielders_next_three list to store the values as objects
midfielders_next_three = []

if airsenal_output:
    # Use regular expressions to find the midfielders data
    midfielders_data = re.search(r'MID:\n(.*?)\n-------------------------', airsenal_output, re.DOTALL)

    if midfielders_data:
        # Split the midfielders data into lines
        midfielders_lines = midfielders_data.group(1).strip().split('\n')
        
        # Extract all midfielder values
        for line in midfielders_lines:
            # Use regular expressions to extract the desired values
            midfielder_match = re.match(r'\d+\.\s+([A-Za-z\sá\-]+),\s+([\d.]+)pts\s+\(£([\d.]+)m,\s+([A-Z]+)\)', line)
            
            if midfielder_match:
                # Create a dictionary for the midfielder
                midfielder = {
                    "name": midfielder_match.group(1),
                    "points": float(midfielder_match.group(2)),
                    "price": f'£{midfielder_match.group(3)}M',
                    "club": midfielder_match.group(4),
                    "type": "MID"
                }
                midfielders_next_three.append(midfielder)

# Print the midfielder data
print("Midfielders:")
for midfielder in midfielders_next_three:
    print(midfielder)

# Save the midfielder data as a JSON file
with open("midfielders_next_three.json", "w") as midfielders_file:
    json.dump(midfielders_next_three, midfielders_file, indent=4)

print("Data saved to midfielders_next_three.json")
