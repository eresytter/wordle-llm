import pandas as pd

# Read the CSV file
df = pd.read_csv(r'path.csv')

# Split the words into individual letters and create separate columns for each position
df['first'] = df['word'].str[0]
df['second'] = df['word'].str[1]
df['third'] = df['word'].str[2]
df['fourth'] = df['word'].str[3]
df['fifth'] = df['word'].str[4]

# Save the modified DataFrame back to a CSV file
df.to_csv(r'path.csv', index=False)