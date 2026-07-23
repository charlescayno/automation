import requests
import json
import pandas as pd
import os
import xlsxwriter

# Replace with your own Mouser API key
API_KEY = "f82c1f1d-d947-43a1-8d03-21fbcb2dab64"

def get_part_data(part_number):
    url = f"https://api.mouser.com/api/v1.0/search/partnumber?apiKey={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "SearchByPartRequest": {
            "mouserPartNumber": part_number,
            "partSearchOptions": "None"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    if "SearchResults" not in response:
        return None
    return response



import xlsxwriter

def save_to_excel(part_data_list):
    if "part_data.xlsx" in os.listdir():
        df_existing = pd.read_excel("part_data.xlsx", engine="openpyxl")
    else:
        df_existing = pd.DataFrame(columns=["Part Number", "Datasheet URL", "Description"])

    df_new = pd.DataFrame(part_data_list)
    df_final = pd.concat([df_existing, df_new], ignore_index=True)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("part_data.xlsx", engine="xlsxwriter")

    # Convert the DataFrame to an XlsxWriter Excel object.
    df_final.to_excel(writer, index=False, sheet_name="Sheet1")

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Set up the hyperlink format.
    hyperlink_format = workbook.add_format({"font_color": "blue", "underline": True})

    # Apply the hyperlink format to the appropriate cells.
    for row_num, url in enumerate(df_final["Datasheet URL"], start=2):
        worksheet.write_url(f"B{row_num}", url, hyperlink_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()





# Input part numbers
part_numbers = input("Enter the part numbers (separated by commas): ").split(",")

# Initialize list for storing part data
part_data_list = []

# Loop through part numbers and get part data from Mouser API
for part_number in part_numbers:
    part_data = get_part_data(part_number)
    
    if part_data is None or not part_data.get("SearchResults", {}).get("Parts"):
        continue
    
    # Extract datasheet URL and description
    datasheet_url = part_data["SearchResults"]["Parts"][0]["DataSheetUrl"]
    description = part_data["SearchResults"]["Parts"][0]["Description"]
    
    # Append part data to list
    part_data_list.append({"Part Number": part_number, "Datasheet URL": datasheet_url, "Description": description})

# Save part data to an Excel file
save_to_excel(part_data_list)
