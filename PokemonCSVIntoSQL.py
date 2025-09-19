import mysql.connector
#Extension to connect to MySQL to Python
from mysql.connector import MySQLConnection
#For type hinting MySQL connection objects
import pandas as pd
#Extension to handle data and CSV files
import logging
#Extension to handle logging
import os
#Extension to handle file paths

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pokemon_sql.log"),
        logging.StreamHandler()
    ]
)
#Set up logging for debugging and information and save to pokemon_sql.log file

def main() -> None:
    """
    Main function to load a CSV file into a MySQL database.
    Args: 
        None
    Returns:
        None
    """ 
    try:
        csv_path = get_csv_path()
        df = load_csv(csv_path)

    except FileNotFoundError:
        logging.error("Error loading CSV file. Exiting.")
        return

    try:
        conn = connect_to_mysql()
    except mysql.connector.Error:
        logging.error("Error connecting to MySQL. Exiting.")
        return

    
    create_database_and_table(conn)
#Create the database and table if they don't exist
    insert_rows(conn, df)
#Insert rows from the DataFrame into the table
    conn.close() 
#Disconnect from MySQL
    logging.info("MySQL connection closed")

def get_csv_path() -> str:
    """
    Function to get the CSV file path from the user. First ask for a file name in the current directory, then a full path if not found.
    Args:
        None
    Returns:
        str: The path to the CSV file.
    """  
    file_name = input("Enter the CSV file name (e.g., Kanto.csv): ")
    if not file_name.endswith(".csv"):
        file_name += ".csv"
    csv_path = os.path.abspath(file_name)
    
    if os.path.isfile(csv_path):
        logging.info(f"Found CSV file: {csv_path}")
        return csv_path
    else:
        logging.warning(f"File {file_name} not found in current directory.")
        csv_path = input("Enter the full path to the CSV file: ")
        csv_path = os.path.abspath(csv_path)
        if not os.path.isfile(csv_path):
            logging.error(f"CSV file not found at {csv_path}. Exiting.")
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        logging.info(f"Found CSV file: {csv_path}")
        return csv_path

def load_csv(csv_path: str) -> pd.DataFrame:
    """
    Function to load a CSV file into a pandas DataFrame and replace NaN with None for SQL compatibility..
    Args:
        csv_path (str): Absolute path to the CSV file.
    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        df = pd.read_csv(csv_path)
        logging.info(f"Successfully loaded CSV file from {csv_path}")
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_path}")
        return
    except pd.errors.EmptyDataError:
        logging.error(f"CSV file is empty: {csv_path}")
        return
    except Exception as e:
        logging.error(f"Error reading CSV file {csv_path}: {e}")
        return
#Load your CSV with pandas following the csv path and handling errors
#Note: use raw string for Windows paths (to avoid escape issues with \n etc) if using a literal path, e.g., r"C:\path\to\file.csv" and not a dynamically input one
    return df
#Replace NaN with None for SQL compatibility and return

def connect_to_mysql() -> MySQLConnection:
    """
    Function to connect to the MySQL database.
    Args:
        None
    Returns:
        mysql.connector.connect: MySQL connection object.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=input("Enter your MySQL password: "),
            #database="pokemon_db",  
# Uncomment if the database already exists
            allow_local_infile=True  
#Allows LOCAL INFILE if needed, safe for Python
        )
        logging.info("Successfully connected to MySQL")
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return

def create_database_and_table(conn : MySQLConnection) -> None:
    """ 
    Function to create the database and table if they don't exist.
    Args:
        conn: MySQL connection object
    Returns:
        None
    """
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS pokemon_db")
        cursor.execute("USE pokemon_db")

#Wrap SQL in triple quotes and pass it to cursor.execute()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                height INT,
                weight INT,
                type_1 VARCHAR(20),
                type_2 VARCHAR(20),
                ability_1 VARCHAR(30),
                ability_2 VARCHAR(30),
                ability_3 VARCHAR(30),
                HP INT,
                ATK INT,
                DEF INT, 
                SP_ATK INT,
                SP_DEF INT,
                Speed INT
            )"""
        )
        logging.info("Database and table ready")
    except mysql.connector.Error as e:
        logging.error(f"Error setting up database/table: {e}")
        conn.close()
        return
    cursor.close()
#Create table if it doesn't exist with the necessary fields

#Insert rows from the CSV
def insert_rows(conn: MySQLConnection, df : pd.DataFrame) -> None:
    """
    Function to insert rows from the DataFrame into the MySQL table.
    Args:
        conn: MySQL connection object
        df: pandas DataFrame containing the data to insert
    Returns:
        None
    """
    cursor = conn.cursor()
    columns = ["id", "name", "height", "weight",
           "type_1", "type_2", "ability_1", "ability_2", "ability_3",
           "HP", "ATK", "DEF", "SP_ATK", "SP_DEF", "Speed"]
#Define the columns to insert
    for _, row in df.iterrows():
        try:
            cursor.execute("SELECT id FROM pokemon WHERE id = %s", (row['id'],))
            if cursor.fetchone():
                logging.info(f"Skipping duplicate entry for Pokemon ID {row['id']}")
                continue
#Check for duplicates before inserting
            row_values = tuple(None if pd.isna(row[col]) else row[col] for col in columns)
#Create a tuple of values for insertion, converting NaN to None for SQL compatibility
            cursor.execute("""
                INSERT INTO pokemon (id, name, height, weight, type_1, type_2, ability_1, ability_2, ability_3, HP, ATK, DEF, SP_ATK, SP_DEF, Speed)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#Insert data into the table, using placeholders for safety, parsing the row data one by one
            , row_values)
#Use tuple(row) to convert the pandas Series to a tuple (list of items) for insertion
            logging.info(f"Inserted Pokemon ID {row['id']}")
        except mysql.connector.Error as e:
            logging.error(f"Error inserting Pokemon ID {row['id']}: {e}")
    cursor.close()

#Commit and close
    try:
        conn.commit()
        logging.info("All data committed to the database suucessfully")
#Make changes permanent
    except mysql.connector.Error as e:
        logging.error(f"Error committing changes to the database: {e}")

if __name__ == "__main__":
    main()