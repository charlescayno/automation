import os
import pandas as pd

# Directory containing Excel files
directory = r"C:/Users/ccayno/automation/codes/LIGHTING/database"

# Value to search for
search_value = "0805"  # Replace with the value you are searching for

# Column to search (set to None to search across all columns)
search_column = None  # Replace with the column name if needed, or set to None

# List to store results
results = []

# Iterate through all files in the directory
for file_name in os.listdir(directory):
    print(file_name)
    # Check if the file is an Excel file
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(directory, file_name)
        
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            # print(df)
            # input()
            
            # Search for the value
            if search_column:
                # Search within a specific column
                filtered = df[df[search_column] == search_value]
            else:
                # Search across all columns
                filtered = df[df.apply(lambda row: search_value in row.values, axis=1)]
            
            # If results found, add to the list
            if not filtered.empty:
                filtered['FileName'] = file_name  # Add a column to indicate the file
                results.append(filtered)
        
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

# Combine results into a single DataFrame
if results:
    combined_results = pd.concat(results, ignore_index=True)
    print(combined_results)
    
    # Save results to an Excel file (optional)
    combined_results.to_excel("search_results.xlsx", index=False)
    print("Search results saved to 'search_results.xlsx'")
else:
    print("No matches found.")
