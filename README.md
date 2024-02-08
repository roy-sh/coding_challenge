# Solution Overview

## Description
This solution provides a Python script for processing instrument prices from a CSV file, calculating statistics, and interacting with a SQLite database to adjust prices using modifiers. Key features include:

 - Modular Design: The solution is modular, with separate functions for reading instrument prices, processing dates, calculating statistics, setting up the database, and retrieving multipliers.

 - Generator Functions: Generator functions are used to efficiently read instrument prices line by line from the CSV file, allowing processing of large files without loading the entire dataset into memory.

 - Database Interaction: The solution uses SQLite as a lightweight database to store instrument price modifiers. Multipliers are retrieved from the database to adjust the prices read from the CSV file.

 - Error Handling: The code includes error handling for parsing dates and checking for business days to ensure data integrity.

 - Command-Line Interface: The script can be executed from the command line, with command-line arguments specifying the input CSV file path, the SQLite database file path, and an optional flag to overwrite the database.

## Running the Solution
To run the solution, follow these steps:

 - Ensure you have Python installed on your system.

 - There is no additional dependencies
 
 - Execute the script from the command line, providing the input CSV file path, the SQLite database file path, and an optional overwrite flag if needed:

```bash
python src/calculation.py input.csv instrument_prices.db [overwrite]
```
 - View the calculated statistics printed to the console.

## Testing
The solution can be tested using various scenarios, including:

 - Providing different input CSV files with varying numbers of instrument prices and formats.
 - Testing edge cases for date parsing and business day validation.
 - Testing database interactions by adding, modifying, or deleting entries in the database and observing the script's behavior.

## Design Decisions
 - Generator Functions: Generator functions were chosen to efficiently process large CSV files line by line, reducing memory consumption.
 - SQLite Database: SQLite was chosen as a lightweight database solution for simplicity and portability. It allows for easy setup and integration within the Python script.
 - Modular Design: The solution is organized into modular functions, promoting code reuse and maintainability. Each function performs a specific task, enhancing readability and clarity.


Overall, this solution provides a flexible and efficient approach for processing instrument prices, calculating statistics, and interacting with a database, suitable for handling large datasets and real-world applications.