import pandas as pd

# Read the modified CSV file
df = pd.read_csv(r'path')

# Calculate the top 5 most common letters for each position
top5_first = df['first'].value_counts().head(5)
top5_second = df['second'].value_counts().head(5)
top5_third = df['third'].value_counts().head(5)
top5_fourth = df['fourth'].value_counts().head(5)
top5_fifth = df['fifth'].value_counts().head(5)

# Create a text file and write the results
with open(r'path', 'w') as f:
    f.write("Top 5 most common letters for the first position:\n")
    f.write(top5_first.to_string())
    f.write("\n\nTop 5 most common letters for the second position:\n")
    f.write(top5_second.to_string())
    f.write("\n\nTop 5 most common letters for the third position:\n")
    f.write(top5_third.to_string())
    f.write("\n\nTop 5 most common letters for the fourth position:\n")
    f.write(top5_fourth.to_string())
    f.write("\n\nTop 5 most common letters for the fifth position:\n")
    f.write(top5_fifth.to_string())

print("Results saved to 'top5_most_common_letters.txt'.")