import pandas as pd
from geopy.geocoders import Nominatim

# Load the CSV file into a pandas dataframe
df = pd.read_csv("D:\code for IT\Cinema\postcodes_updated.csv")

# Initialize the geocoder
geolocator = Nominatim(user_agent="cinema_locator")

# Create a function to get the latitude and longitude of an address
def get_coords(address):
    location = geolocator.geocode(address)
    if location:
        return f"{location.latitude}, {location.longitude}"
    else:
        return None


# Add a new column to the dataframe with the latitude and longitude of each cinema's address
df["coords"] = df["address"].apply(lambda x: get_coords(x))

# Write the updated dataframe to a new CSV file
df.to_csv("cinemas_with_coords.csv", index=False)
