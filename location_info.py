import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Load the driver
driver = webdriver.Chrome()

# Open the locations file and read in the locations
with open("locations.txt", "r") as file:
    locations = file.readlines()

# Remove newline characters from each location
locations = [location.strip() for location in locations]

# Create a dictionary to store the postcodes
postcodes = {}

# Loop through each location and search for the Cineworld
for location in locations:
    # Construct the search query for Google Maps
    search_query = f"Cineworld {location} postcode"

    # Navigate to Google Maps
    driver.get("https://www.google.com/maps/")

    # switch to Google Maps tab
    driver.switch_to.window(driver.window_handles[-1])

    # find search box and enter search query
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(location + " Cineworld" + Keys.ENTER)

    # submit search query
    search_box.submit()

    # Wait for the search results to load
    try:
        location_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(9) > div:nth-child(3) > button > div.AeaXub > div.rogA2c > div.Io6YTe.fontBodyMedium",
                )
            )
        )
        postcodes[location] = location_info.text
        print(f"{location}: {location_info.text}")
    except:
        print(f"No results found for {location}")
        continue

    # Wait for 1 second before searching for the next location
    sleep(1)

# Close the driver
driver.quit()

# Write the postcodes to a CSV file
with open("postcodes.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(postcodes.items())
