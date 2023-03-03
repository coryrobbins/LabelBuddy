import pandas as pd

# Read in the CSV file
df = pd.read_csv('../emails.csv')

#save the header
header_row = df.columns.tolist()  # Save the header row

# Drop all the contents in a column except for the header
df = df.drop(columns=['label'])

#Write the new CSV file
df.to_csv('../emails.csv', index=False, header=True)