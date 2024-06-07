import csv

def extract_words(csv_file, txt_file):
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(txt_file, 'a') as txt_file:
            for row in csv_reader:
                if 'day' in row and row['day']:  # Checking if 'day' column exists and has a value
                    if 'word' in row and row['word']:  # Checking if 'word' column exists and has a value
                        txt_file.write(row['word'] + '\n')

# Example usage:
csv_file = r"path to wordle.csv"  # Replace 'data.csv' with your CSV file name
txt_file = r"path to previous_words.txt"  # Replace 'output.txt' with your desired output file name
extract_words(csv_file, txt_file)
