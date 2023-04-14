import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Load the CSV file
with open("postcodes.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        # Construct the Cineworld URL
        location_name = row[0].replace(" ", "-")
        print(location_name)
        url = f"https://www.cineworld.co.uk/cinemas/{location_name}"

        # Load the Cineworld page and wait for the "What's On" button to appear
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/section[1]/div/div[1]/div/p/a[2]")
            )
        )
        current_url = driver.current_url
        row.append(current_url)

        # Write the updated row to the output file
        with open("output.csv", mode="a", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(row)

# Close the web driver
driver.quit()
