import subprocess
import json

def run_airsenal_commands():
    # Activate the Conda environment
    subprocess.run(["conda", "activate", "airsenal_env"], shell=True)

    # Run AIrsenal commands and capture the output
    completed_process = subprocess.run(["airsenal_run_pipeline"], capture_output=True, text=True, shell=True)

    # Check if the command was successful
    if completed_process.returncode == 0:
        # Get the standard output as a string
        airsenal_output = completed_process.stdout

        # Process the airsenal_output to extract the desired data
        data = extract_data(airsenal_output)

        # Create a dictionary to store the data
        data_dict = {"AIrsenal_Output": data}

        # Save the data to a JSON file
        with open("airsenal_data.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=2)

        print("Data saved to 'airsenal_data.json'.")

    else:
        print("Error: AIrsenal command returned a non-zero exit status.")

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

if __name__ == "__main__":
    run_airsenal_commands()
