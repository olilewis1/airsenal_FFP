import json

# Define the extract_data function
# Define the extract_data function
# Define the extract_data function
def extract_data(output):
        # Search for the desired data pattern
      start_pattern = "===================================="
      end_pattern = "Pipeline finished OK!"

      # Find the start and end positions of the data
      start_pos = output.find(start_pattern)
      end_pos = output.find(end_pattern)

      # Extract the data
      if start_pos != -1 and end_pos != -1:
          data = output[start_pos:end_pos + len(end_pattern)]
          return data
      else:
          return "Data not found."


# Read the content of the JSON file
with open('NEXT_THREE_DATA.JSON', 'r') as json_file:
    json_data = json.load(json_file)
# Extract the desired section from the JSON data
json_data['next_three_out'] += "\n  Pipeline finished OK!"
desired_section = extract_data(json_data['next_three_out'])

# Print the extracted section
print('hiii', desired_section)
