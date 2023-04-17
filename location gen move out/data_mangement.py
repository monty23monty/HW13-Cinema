import csv
import re

# Open the CSV file and create a new CSV writer to write the updated rows
with open("output.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = []
    for row in csv_reader:
        rows.append(row)
    with open("postcodes_updated.csv", "w", newline="") as new_csv_file:
        csv_writer = csv.writer(new_csv_file)

        # Loop through each row and extract the cinema code from the URL
        for row in rows:
            url = row[2]
            code_match = re.search(r"/\d{3}", url)
            if code_match:
                cinema_code = code_match.group()[1:]
            else:
                cinema_code = ""

            # Add the cinema code as a new column to the row
            new_row = row + [cinema_code]
            csv_writer.writerow(new_row)
