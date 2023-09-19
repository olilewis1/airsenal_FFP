import json
import re

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

# Initialize GK_next_three list to store the values as objects
GK_next_three = []

if airsenal_output:
    # Use regular expressions to find the GK data
    gk_data = re.search(r'GK:(.*?)DEF:', airsenal_output, re.DOTALL)
    
    if gk_data:
        # Split the GK data into lines
        gk_lines = gk_data.group(1).strip().split('\n')
        
        # Extract all goalkeeper values
        for gk_info in gk_lines:
            # Use regular expressions to extract the desired values
            gk_details = re.search(r'(\d+)\.\s+([A-Za-z\s]+),\s+([\d.]+)pts\s+\(£([\d.]+)m,\s+([A-Z]+)\)', gk_info)
            
            if gk_details:
                # Append each goalkeeper info as an object to GK_next_three
                gk_object = {
                    "name": gk_details.group(2).strip(),
                    "points": float(gk_details.group(3)),
                    "price": f'£{gk_details.group(4)}M',
                    "club": gk_details.group(5)
                }
                GK_next_three.append(gk_object)

else:
    print("No AIrsenal data found in the JSON file.")

# Create a dictionary to store the result
result = {
    "AIrsenal_Output": airsenal_output,
    "GK_next_three": GK_next_three
}

# Save the result as a new JSON file
with open("result.json", "w") as result_file:
    json.dump(result, result_file, indent=4)

# Print the GK_next_three objects
print("GK_next_three:")
for gk in GK_next_three:
    print(gk)
