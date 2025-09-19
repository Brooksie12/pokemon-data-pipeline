import requests
#Extension used to pull data from API URL
import pandas as pd
#Extension used to handle data and save to CSV
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pokemon.log"),
        logging.StreamHandler()
    ]
)
#Set up logging for debugging and information and save to pokemon.log file
import os
#Extension to handle file paths

def fetch_pokemon_data(pokemon_id: int) -> dict | None:
    """
    Function to pull the API data for a given pokemon ID

    Args: 
        pokemon_id (int): The ID (pokemon national number) of the Pokémon to fetch data for.

    Returns: 
        dict or None: The Pokémon data in JSON format if successful, otherwise None.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
#Using an f-string to insert the pokemon ID into the relevant API URL

    try:
        response = requests.get(url, timeout=10)  
#Timeout prevents hanging forever
        response.raise_for_status()  
# Raises an HTTPError if status != 200
        logging.info(f"Fetched data for Pokémon ID {pokemon_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for Pokémon ID {pokemon_id} Status Code: {e}")
        return None

"""For reference, Here are the ones you’ll see most often:

200 OK → Everything worked, you got data.

201 Created → Something new was created (common for POST requests).

400 Bad Request → Your request was invalid (maybe a typo in the URL or parameters).

401 Unauthorized → You need to log in / provide an API key.

403 Forbidden → You don’t have permission.

404 Not Found → The resource doesn’t exist (e.g., Pokémon with that ID doesn’t exist).

500 Internal Server Error → Problem on the server’s side.

503 Service Unavailable → Server is overloaded or under maintenance."""



def clean_pokemon_data(data: dict) -> dict | None:
    """
    Function to clean the raw data fetched from the API

    Args:
        data (dict): The raw Pokémon data fetched from the API.

    Returns:
        dict or None: A cleaned dictionary with selected fields (id/national number, name, height, weight, type(s) and ability(ies)), or None if data is None.
    """

    if not data:
        return None
#Safety check to ensure data is not None
    types=data.get("types", [])
    abilities=data.get("abilities", [])
    stats=data.get("stats", [])
#Extracts types and abilities from the raw data, defaulting to empty lists if not present. Using get here eliminates the need for a try/except block for KeyError (missing values)
    cleaned_data = {
        "id": data.get("id"),
        "name": data.get("name"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "type_1": types[0]["type"]["name"] if len(types) > 0 else "",
        "type_2": types[1]["type"]["name"] if len(types) > 1 else "",
        "ability_1": abilities[0]["ability"]["name"] if len(abilities) > 0 else "",
        "ability_2": abilities[1]["ability"]["name"] if len(abilities) > 1 else "",
        "ability_3": abilities[2]["ability"]["name"] if len(abilities) > 2 else "",
        "HP": stats[0]["base_stat"] if len(stats) > 0 else None,
        "ATK": stats[1]["base_stat"] if len(stats) > 1 else None,
        "DEF": stats[2]["base_stat"] if len(stats) > 2 else None,
        "SP_ATK": stats[3]["base_stat"] if len(stats) > 3 else None,
        "SP_DEF": stats[4]["base_stat"] if len(stats) > 4 else None,
        "Speed": stats[5]["base_stat"] if len(stats) > 5 else None,
}
#Creates a cleaned dictionary with selected fields, handling cases where types or abilities may be missing
    return cleaned_data



def kanto() -> None:
    """
    Function to fetch and clean data for the first 151 Pokémon (Kanto region) and save it to a CSV file.
    Args: 
        None
    Returns: 
        None
    """
    pokemon_list = []
    for pokemon_id in range(1, 152):  
        raw_data = fetch_pokemon_data(pokemon_id)
        cleaned_data = clean_pokemon_data(raw_data)
#Fetch first 151 Pokémon (from the original Kanto region) and clean the data

        if cleaned_data:
            pokemon_list.append(cleaned_data)
#Add the data to the list if it was successfully cleaned
    
    df = pd.DataFrame(pokemon_list)
#Convert the list of cleaned data into a pandas DataFrame

    df.to_csv("pokemon_data.csv", index=False)
    logging.info("Data saved to pokemon_data.csv")
#Save to a CSV file and print a confirmation message

#kanto()
#Calls the Kanto function to fetch, clean, and save data for the first 151 Pokémon

def main() -> None:
    """
    Main function to fetch and clean data for a user-specified range of Pokémon and save it to a CSV file.
    Args: 
        None
    Returns:
        None
    """
    try:
        start_id = int(input("Enter the starting Pokemon ID: "))
    except ValueError:
        logging.error("Invalid input. Please enter a valid integer for the starting Pokemon ID.")
        return
    try:    
        end_id = int(input("Enter the ending Pokemon ID: ")) + 1  
    except ValueError:
        logging.error("Invalid input. Please enter a valid integer for the ending Pokemon ID.")
        return
#Get the user to specify the range of pokemon to select the data for (+1 to end_id to include the end_id in the range) excepting any errors in input

    file_name = input("Enter the output CSV file name (e.g., pokemon_data.csv): ")
#Get the user to specify the output file name
    if not file_name.endswith(".csv"):
        file_name += ".csv"
#Ensure the file name ends with .csv

    pokemon_list = []
    for pokemon_id in range(start_id, end_id):  
        raw_data = fetch_pokemon_data(pokemon_id)
        cleaned_data = clean_pokemon_data(raw_data)
#Fetch Pokémon within the range provided and clean the data

        if cleaned_data:
            pokemon_list.append(cleaned_data)
#Add the data to the list if it was successfully cleaned
    
    df = pd.DataFrame(pokemon_list)
#Convert the list of cleaned data into a pandas DataFrame
    try:
        df.to_csv(file_name, index=False)
#Index set to False to avoid adding an extra index column in the CSV file since the pokemon ID is already present
        csv_path = os.path.abspath(file_name)
        logging.info(f"Data saved to {file_name} at {csv_path} (save this path for SQL import)")
#Save to a CSV file and log a confirmation message
    except Exception as e:
        logging.error(f"Failed to save data to {file_name} {e}")
        return

    

if __name__ == "__main__":
# Run the main function if this script is executed directly but not if imported as a module (safety measure)
    main()
# Calls the main function to fetch, clean, and save data for a user-specified range of Pokémon