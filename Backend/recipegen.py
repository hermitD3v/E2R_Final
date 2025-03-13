import csv
import os
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_base_directory(file_path):
    base_dir = os.path.dirname(file_path)
    logging.debug(f"Base directory for {file_path}: {base_dir}")
    return base_dir

def find_mtpl_files(test_dir):
    logging.debug(f"Finding .mtpl files in {test_dir}")
    mtpl_files = []
    for filename in os.listdir(test_dir):
        if filename.endswith('.mtpl'):
            mtpl_files.append(filename)
    logging.debug(f"Found .mtpl files: {mtpl_files}")
    return mtpl_files

def find_stpl_files(mtpl_files):
    logging.debug("Finding .stpl files")
    stpl_files = []
    for stpl_file in find_files_with_extension(root_folder, '.stpl'):
        with open(stpl_file, 'r') as f:
            content = f.read()
            for mtpl in mtpl_files:
                if re.search(r'\b' + re.escape(mtpl) + r'\b', content):
                    stpl_files.append(stpl_file)
                    break
    logging.debug(f"Found .stpl files: {stpl_files}")
    return stpl_files

def find_csv_files(stpl_files):
    logging.debug("Finding .csv files")
    csv_files = []
    for stpl in stpl_files:
        stpl_basename = os.path.basename(stpl)
        for csv_file in find_files_with_extension(root_folder, '.csv'):
            with open(csv_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if re.search(r'\b' + re.escape(stpl_basename) + r'\b', line):
                        csv_files.append(csv_file)
                        break
    logging.debug(f"Found .csv files: {csv_files}")
    return csv_files

def extract_recipes(stpl_files, csv_files):
    logging.debug("Extracting recipes")
    recipes = set()

    for csv_file in csv_files:
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                for stpl in stpl_files:
                    if re.search(r'\b' + re.escape(os.path.basename(stpl)) + r'\b', line):
                        row = line.strip().split(',')
                        # Always add up to the 6th column or the entire line if it has fewer than 6 columns
                        recipes.add(','.join(row[:6]))
                        break

    logging.debug(f"Extracted recipes: {recipes}")
    return recipes

def find_files_with_extension(root_folder, extension):
    logging.debug(f"Finding files with extension {extension} in {root_folder}")
    files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(dirpath, filename))
    logging.debug(f"Found files: {files}")
    return files

def process_csv(input_csv, output_csv):
    logging.debug(f"Processing CSV file {input_csv}")
    cache = {}

    with open(input_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        header.append('Recipe')

        rows = []
        for row in reader:
            test_file = row[1]
            if test_file in cache:
                logging.debug(f"Using cached results for {test_file}")
                recipes = cache[test_file]
            else:
                test_dir = get_base_directory(test_file)
                mtpl_files = find_mtpl_files(test_dir)
                if mtpl_files:
                    stpl_files = find_stpl_files(mtpl_files)
                    if stpl_files:
                        csv_files = find_csv_files(stpl_files)
                        if csv_files:
                            recipes = extract_recipes(stpl_files, csv_files)
                            cache[test_file] = recipes
                        else:
                            recipes = set()
                    else:
                        recipes = set()
                else:
                    recipes = set()

            if recipes:
                for recipe in recipes:
                    new_row = row.copy()
                    new_row.append(recipe)
                    rows.append(new_row)
            else:
                new_row = row.copy()
                new_row.append('')
                rows.append(new_row)

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)
    logging.debug(f"Processed CSV saved to {output_csv}")

def main():
    global root_folder
    root_folder = r'.\PartRepo\HDMTOS\Validation\iVal'
    input_csv = r'.\Test\function_test.csv'
    output_csv = r'.\Test\output_with_recipes.csv'

    process_csv(input_csv, output_csv)
    logging.info(f"Processed CSV and saved to {output_csv}")

if __name__ == '__main__':
    main()