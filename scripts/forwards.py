import json
import re

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Initialize forwards_next_three list to store the values as objects
forwards_next_three = []

if airsenal_output:
    # Use regular expressions to find the forwards data
    forwards_data = re.search(r'FWD:\n(.*?)\n-------------------------', airsenal_output, re.DOTALL)

    if forwards_data:
        # Split the forwards data into lines
        forwards_lines = forwards_data.group(1).strip().split('\n')
        
        # Extract all forward values
        for line in forwards_lines:
            # Use regular expressions to extract the desired values
            forward_match = re.match(r'\d+\.\s+(.*?),\s+([\d.]+)pts\s+\(£([\d.]+)m,\s+([A-Z]+)\)', line)
            
            if forward_match:
                # Create a dictionary for the forward
                forward = {
                    "name": forward_match.group(1),
                    "points": float(forward_match.group(2)),
                    "price": f'£{forward_match.group(3)}M',
                    "club": forward_match.group(4),
                    "type": "FWD"
                }
                forwards_next_three.append(forward)

# Print the forward data
print("Forwards:")
for forward in forwards_next_three:
    print(forward)

# Save the forward data as a JSON file
with open("forwards_next_three.json", "w") as forwards_file:
    json.dump(forwards_next_three, forwards_file, indent=4)

print("Data saved to forwards_next_three.json")
