import csv
import datetime
import statistics
import sqlite3
from collections import defaultdict, deque
import os
import sys


def read_instrument_prices_line(file_path):
    """
    Generator function to read instrument prices from a CSV file.
    
    Parameters:
    - file_path (str): Path to the input CSV file.

    Yields:
    - tuple: Tuple containing instrument name, date, and value.
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            instrument_name, date_str, value = row
            yield instrument_name, date_str, float(value)


def read_instrument_prices(file_path, conn):
    """
    Process instrument prices from the input file using a generator.
    
    Parameters:
    - file_path (str): Path to the input CSV file.
    - conn (sqlite3.Connection): SQLite database connection object.

    Returns:
    - dict: A defaultdict of deques containing instrument prices.
    """
    instrument_prices = defaultdict(deque)
    for instrument_name, date_str, value in read_instrument_prices_line(file_path):
        # Process each instrument price here (e.g., calculate statistics)
        multiplier = get_multiplier(conn, instrument_name)
        value = float(value) * multiplier
        process_date(instrument_prices, instrument_name, date_str, value)
    return instrument_prices


def process_date(instrument_prices, instrument_name, date_str, value):
    """
    Process a single date entry from the CSV file.

    Parameters:
    - instrument_prices (defaultdict): Dictionary containing instrument prices.
    - instrument_name (str): Name of the instrument.
    - date_str (str): Date in string format.
    - value (float): Price value.

    Returns:
    - None
    """
    try:
        date = datetime.datetime.strptime(date_str, '%d-%b-%Y')
    except ValueError:
        return
    
    if is_business_day(date):
        instrument_prices[instrument_name].append((date, value))

def is_business_day(date):
    """
    Check if a given date is a business day (Monday - Friday).

    Parameters:
    - date (datetime.datetime): Date to check.

    Returns:
    - bool: True if the date is a business day, False otherwise.
    """
    return date.weekday() < 5

def calculate_statistics(instrument_prices):
    """
    Calculate statistics for instrument prices.

    Parameters:
    - instrument_prices (dict): Dictionary containing instrument prices.

    Returns:
    - dict: Dictionary containing calculated statistics for each instrument.
    """
    results = {}
    for instrument, prices in instrument_prices.items():
        if instrument == 'INSTRUMENT1':
            results[instrument] = statistics.mean(price for _, price in prices)
        elif instrument == 'INSTRUMENT2':
            nov_2014_prices = [price for date, price in prices if date.year == 2014 and date.month == 11]
            results[instrument] = statistics.mean(nov_2014_prices)
        elif instrument == 'INSTRUMENT3':
            # Median is chosen as the statistical calculation for INSTRUMENT3
            if len(prices) > 1:
                results[instrument] = statistics.median(price for _, price in prices)
        else:
            # Sum of the newest 10 elements
            newest_prices = sorted(prices, key=lambda x: x[0], reverse=True)[: min(10, len(prices))]
            results[instrument] = sum(price for _, price in newest_prices)
    return results

def setup_database(db_file_path, overwrite=True):
    """
    Set up a SQLite database to store instrument price modifiers.

    Parameters:
    - db_file_path (str): Path to the SQLite database file.
    - overwrite (bool): Whether to overwrite the existing database file if it exists.

    Returns:
    - sqlite3.Connection: SQLite database connection object.
    """
    if os.path.exists(db_file_path) and not overwrite:
        return sqlite3.connect(db_file_path)
    
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS INSTRUMENT_PRICE_MODIFIER
                 (ID INTEGER PRIMARY KEY, NAME TEXT, MULTIPLIER REAL)''')
    # Example data
    c.execute("INSERT INTO INSTRUMENT_PRICE_MODIFIER (NAME, MULTIPLIER) VALUES (?, ?)", ('INSTRUMENT1', 1.5))
    conn.commit()
    return conn

def get_multiplier(conn, instrument_name):
    """
    Retrieve the multiplier for a given instrument from the database.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection object.
    - instrument_name (str): Name of the instrument.

    Returns:
    - float: Multiplier value.
    """
    c = conn.cursor()
    c.execute("SELECT MULTIPLIER FROM INSTRUMENT_PRICE_MODIFIER WHERE NAME=?", (instrument_name,))
    result = c.fetchone()
    return result[0] if result else 1.0

def main(input_file, db_file, overwrite):
    """
    Main function to orchestrate the process of reading, calculating, and adjusting instrument prices.

    Parameters:
    - input_file (str): Path to the input CSV file containing instrument prices.
    - db_file (str): Path to the SQLite database file for instrument price modifiers.
    - overwrite (bool): Whether to overwrite the existing database file if it exists.

    Returns:
    - None
    """
    # Step 0: Setup database and adjust values using modifiers
    conn = setup_database(db_file, overwrite)

    # Step 1: Read data from the input file
    instrument_prices = read_instrument_prices(input_file, conn)
    
    # Step 2: Calculate statistics
    results = calculate_statistics(instrument_prices)
    
    # Print or store the final results
    print(results)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input_file_path db_file_path [overwrite]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    db_file_path = sys.argv[2]
    overwrite = False
    if len(sys.argv) == 4 and sys.argv[3].lower() == "overwrite":
        overwrite = True
    
    main(input_file_path, db_file_path, overwrite)
