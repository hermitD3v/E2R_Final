import csv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_and_save(input_csv):
    # Create sets to hold unique rows for each type
    hdmt_rows = set()
    hbi_rows = set()
    shared_rows = set()
    unknown_rows = set()  # Set for unknown types

    # Open the input CSV file for reading
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header

        # Iterate through each row in the CSV file
        for row in reader:
            # Only keep the relevant columns: Test File, Flow, Recipe
            row = [row[1], row[3], row[4]]

            if len(row) < 3:
                logging.warning(f"Skipping row due to insufficient columns: {row}")
                continue  # Skip rows that don't have enough columns

            # Extract the base name from the Test File column
            row[0] = os.path.basename(row[0].strip())

            recipe = row[2]  # The "Recipe" column

            # Split the recipe into individual paths
            paths = recipe.split(',')

            # Determine the type based on the paths
            type_found = False
            for path in paths:
                if 'HBI\\' in path:
                    hbi_rows.add(tuple(row))
                    type_found = True
                    break
                elif 'HDMT\\' in path:
                    hdmt_rows.add(tuple(row))
                    type_found = True
                    break
                elif 'Shared\\' in path:
                    shared_rows.add(tuple(row))
                    type_found = True
                    break

            if not type_found:
                logging.warning(f"Unknown type in recipe path for row: {row}")
                unknown_rows.add(tuple(row))  # Add to unknown rows

    # Sort the rows based on the "Recipe" column (index 2)
    hdmt_rows = sorted(hdmt_rows, key=lambda x: x[2])
    hbi_rows = sorted(hbi_rows, key=lambda x: x[2])
    shared_rows = sorted(shared_rows, key=lambda x: x[2])
    unknown_rows = sorted(unknown_rows, key=lambda x: x[2])

    # Write the rows to the corresponding output CSV files
    with open(r'.\Chasis\hdmt.csv', 'w', newline='') as hdmt_file:
        writer = csv.writer(hdmt_file)
        writer.writerow(['Test File', 'Flow', 'Recipe'])  # Write the new header
        writer.writerows(hdmt_rows)

    with open(r'.\Chasis\hbi.csv', 'w', newline='') as hbi_file:
        writer = csv.writer(hbi_file)
        writer.writerow(['Test File', 'Flow', 'Recipe'])  # Write the new header
        writer.writerows(hbi_rows)

    with open(r'.\Chasis\shared.csv', 'w', newline='') as shared_file:
        writer = csv.writer(shared_file)
        writer.writerow(['Test File', 'Flow', 'Recipe'])  # Write the new header
        writer.writerows(shared_rows)

    with open(r'.\Chasis\unknown.csv', 'w', newline='') as unknown_file:
        writer = csv.writer(unknown_file)
        writer.writerow(['Test File', 'Flow', 'Recipe'])  # Write the new header
        writer.writerows(unknown_rows)

    logging.info("CSV files have been segregated and saved.")

# Example usage
parse_and_save(r'.\Test\output_with_recipes.csv')