import json
import re

# Load the AIrsenal data from the JSON file
with open("airsenal_data.json", "r") as json_file:
    data = json.load(json_file)

# Access the AIrsenal output
airsenal_output = data.get("AIrsenal_Output")

if airsenal_output:
    # Find the starting 11 section
    starting_11_section = airsenal_output.split("starting 11 ===\n\n\n")
    if len(starting_11_section) > 1:
        starting_11_section = starting_11_section[1]  # Take the part after "starting 11 ==="
    else:
        starting_11_section = ""

    # Split the starting 11 section into lines
    starting_11_lines = starting_11_section.strip().split('\n')

    # Initialize a dictionary to store the sections as arrays of lines
    section_lines = {}

    # Initialize a section name
    section_name = ""

    for line in starting_11_lines:
        # Check if the current line is a section header
        if line.startswith("== ") or line.startswith("=== "):
            if section_name:
                # Save the previous section without empty lines and non-player lines
                cleaned_section_content = [x for x in section_content if re.match(r'.*\(.*\)', x.strip())]
                section_lines[section_name] = cleaned_section_content
            # Set the new section name
            section_name = line.strip()
            section_content = []
        else:
            # Add the line to the current section's content
            if section_name:
                section_content.append(line)

    if section_name:
        # Save the last section without empty lines and non-player lines
        cleaned_section_content = [x for x in section_content if re.match(r'.*\(.*\)', x.strip())]
        section_lines[section_name] = cleaned_section_content

    # Print each section and store it as an array of lines
    for section_name, section_content in section_lines.items():
        print(section_name)
        print("\n".join(section_content))
        print("\n=====================\n")

    # Save the section_lines dictionary to a JSON file
    with open("section_lines.json", "w") as outfile:
        json.dump(section_lines, outfile, indent=4)

    print("Section lines saved to section_lines.json")
else:
    print("No AIrsenal output found in the JSON file.")
