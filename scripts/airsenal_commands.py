import subprocess
import json

def run_airsenal_commands():
    # Activate the Conda environment


    # set team id
    completed_process = subprocess.run(["airsenal_env set -k FPL_TEAM_ID -v 9884044"], capture_output=True, text=True, shell=True)
    completed_login = subprocess.run(["airsenal_env set -k FPL_LOGIN -v olilewis1@hotmail.co.uk"], capture_output=True, text=True, shell=True)
    completed_password = subprocess.run(["airsenal_env set -k FPL_PASSWORD -v Flynn@2020"], capture_output=True, text=True, shell=True)
    
    3705355
    oliverlewis1331@gmail.com 
    Flynn@1992 
    #run weekly
    # To stay up to date in the future, you will need to fill three tables: match, player_score, and transaction with more recent data, using the command
    completed_password = subprocess.run(["airsenal_update_db"], capture_output=True, text=True, shell=True)

    #run weekly
    # The next step is to use the team- and player-level NumPyro models to predict the expected points for all players for the next fixtures. This is done using the command
    completed_password = subprocess.run(["airsenal_run_prediction --weeks_ahead 3"], capture_output=True, text=True, shell=True)
    # this gives top 5 for each position



if __name__ == "__main__":
    run_airsenal_commands()
