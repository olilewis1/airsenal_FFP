import subprocess
import json
fpl_team_id = 9884044
fpl_team_id_me = 3705355
fpl_login = 'olilewis1@hotmail.co.uk'
fpl_login_me = 'oliverlewis1331@gmail.com'
fpl_password = 'Flynn@2020'
fpl_password_me = 'Flynn@1992'

def run_airsenal_commands():
    command_team_id = f"airsenal_env set -k FPL_TEAM_ID -v {fpl_team_id_me}"
    command_login = f"airsenal_env set -k FPL_LOGIN -v {fpl_login_me}"
    command_password = f"airsenal_env set -k FPL_PASSWORD -v {fpl_password_me}"
    # Activate the Conda environment
    subprocess.run(["conda", "activate", "airsenal_env"], shell=True)

    # set up login details
    subprocess.run([command_team_id], capture_output=True, text=True, shell=True)
    subprocess.run([command_login], capture_output=True, text=True, shell=True)
    subprocess.run([command_password], capture_output=True, text=True, shell=True)
    
        #run weekly
    # To stay up to date in the future, you will need to fill three tables: match, player_score, and transaction with more recent data, using the command
    #subprocess.run(["airsenal_update_db"], capture_output=True, text=True, shell=True)

        #run weekly
    # The next step is to use the team- and player-level NumPyro models to predict the expected points for all players for the next fixtures. This is done using the command
    completed_process_next_three = subprocess.run(["airsenal_run_prediction --weeks_ahead 3"], capture_output=True, text=True, shell=True)
    # this gives top 5 for each position

        # Run AIrsenal commands and capture the output
    completed_process = subprocess.run(["airsenal_run_optimization --weeks_ahead 3"], capture_output=True, text=True, shell=True)

    # Check if next three returns successful 
    if completed_process_next_three.returncode == 0:
          # Get the standard output as a string
        next_three_output = completed_process_next_three.stdout

        data_dict = {"next_three_out": next_three_output} 
        data_dict["next_three_out"] += " Pipeline finished OK!"
        data = extract_data(data_dict["next_three_out"])
        data_dict = {"next_three_out" : data}
        print('data dictttt', data_dict)
                # Save the data to a JSON file
        with open("next_three_data.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=2)
        
        print("Data saved to 'next_three_data.json'.")
        command = ["python", "players_next_three.py"]

        # Run the script using subprocess
        try:
            subprocess.run(command, check=True)
            print("players_next_three.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running players_next_three.py: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    else:
        print("Error: AIrsenal command returned a non-zero exit status.")
    # Check if the command was successful
    if completed_process.returncode == 0:
        # Get the standard output as a string
        airsenal_output = completed_process.stdout
        data_dict = {"AIrsenal_Output": airsenal_output}
        data_dict["AIrsenal_Output"] +=  " Pipeline finished OK!"
        # Process the airsenal_output to extract the desired data
        data = extract_data(data_dict["AIrsenal_Output"])

        # Create a dictionary to store the data
        data_dict = {"AIrsenal_Output": data}

        # Save the data to a JSON file
        with open("airsenal_data.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=2)

        print("Data saved to 'airsenal_data.json'.")

        #run optimum strategy script
        command_optimum_strategy = ["python", "optimum_strategy.py"]

        # Run the script using subprocess
        try:
            subprocess.run(command_optimum_strategy, check=True)
            print("optimum_strategy.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running optimum_strategy.py: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

            # run starting eleven script
        command_starting_eleven = ["python", "starting_eleven.py"]

        # Run the script using subprocess
        try:
            subprocess.run(command_starting_eleven, check=True)
            print("starting_eleven.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running starting_eleven.py: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}") 

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
          print('hiii data')
          return data
      else:
          return "Data not found."
if __name__ == "__main__":
    run_airsenal_commands()
