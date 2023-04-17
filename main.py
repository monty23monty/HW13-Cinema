# Import necessary libraries
import requests
import json
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
from geopy import distance
from geopy.geocoders import Nominatim
import urllib
from flask_bootstrap import Bootstrap

# Create a Flask application instance
app = Flask(__name__)

# Set the secret key for the application to enable flashing of messages
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Initialize Bootstrap
Bootstrap(app)

# Set the allowed certificate attribute IDs as a set and a list
allowed_attribute_ids_dict = {"u", "pg", "12", "12a", "15", "18"}
allowed_attribute_ids_list = ["u", "pg", "12", "12a", "15", "18"]


# Define the home page route
@app.route("/")
def home():
    return render_template("home.html")


# Define the age verification page route
@app.route("/age", methods=["GET", "POST"])
def age():
    # Handle POST request from the age verification form
    if request.method == "POST":
        # Get the age entered by the user from the form
        age = request.form["age"]
        try:
            # Convert the age to an integer
            age = int(age)
            # If the age is not within a sensible range, display an error message and redirect to the home page
            if age < 1 or age > 150:
                print("Please enter a sensible number.")
                flash("Please enter a sensible number.")
                return redirect(url_for("home"))
        except:
            # If the age entered is not a valid number, display an error message and redirect to the home page
            print("Please use numeric digits or a whole number.")
            flash("Please use numeric digits or a whole number.")
            return redirect(url_for("home"))

        # Determine the appropriate film certificates the user can view based on their age, and render the appropriate template
        if age <= 4:
            print("You can see U certificate films.")
            return render_template("age_u.html", age=age)

        elif age <= 8:
            print("You can see PG and U certificate films.")
            return render_template("age_pg.html", age=age)

        elif age <= 12:
            print("You can see PG, U and 12 certificate films.")
            return render_template("age_12.html", age=age)
        elif age < 18:
            print("You can watch, U, PG, 12A and 15 certificate films")
            return render_template("age_15.html", age=age)

        elif age >= 18:
            print("You can see films of any certificate.")
            return render_template("age_18.html", age=age)

        else:
            # If the user's age does not allow them to view any film certificates, render the default age template
            print("You cannot see any films.")
            return render_template("age.html")

    else:
        # If the request is not a POST request, redirect to the home page
        return redirect(url_for("home"))


@app.route("/films", methods=["GET", "POST"])
def films():
    if request.method == "POST":
        # Read the cinema data from a CSV file
        df = pd.read_csv("D:\code for IT\Cinema\cinemas_with_coords.csv")
        print(df.head())
        # Get the user's postcode from the form
        user_postcode = request.form["postcode"]
        # Initialize a geolocator object
        geolocator = Nominatim(user_agent="cinema_locator")

        # Define a function to get the latitude and longitude of an address
        def get_coords(address):
            location = geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            else:
                return None

        # Drop any rows that don't have coordinates
        df = df.dropna(subset=["coords"])

        # Define a function to calculate the distance between two coordinates
        def get_distance(coords1, coords2):
            return distance.distance(coords1, coords2).km

        # Get the latitude and longitude of the user's location
        user_location = geolocator.geocode(user_postcode)
        if user_location:
            user_coords = (user_location.latitude, user_location.longitude)
        else:
            print("Invalid postcode.")
            exit()

        # Split the 'coords' column into separate 'lat' and 'lon' columns
        coords_df = df["coords"].str.split(",", expand=True)
        coords_df.columns = ["lat", "lon"]

        # Join the 'coords' DataFrame back to the original DataFrame
        df = pd.concat([df, coords_df], axis=1)

        # Print the updated DataFrame
        print(df)
        # Convert the 'lat' and 'lon' columns to float data type
        df["lat"] = df["lat"].astype(float)
        df["lon"] = df["lon"].astype(float)

        # Calculate the distance between the user's location and each cinema location
        if user_coords:
            df["distance"] = df.apply(
                lambda row: get_distance((row["lat"], row["lon"]), user_coords), axis=1
            )
            # Find the cinema location closest to the user's location
            closest_row = df.sort_values(by="distance").iloc[0]
            print(closest_row["location"])
            print(closest_row["address"])
            print(closest_row["url"])
            print(closest_row["code"])
            # Format the cinema code with leading zeros
            code = closest_row["code"]
            code = f"{code:03d}"
            print(code)
            # Create a dictionary to hold the cinema code and name
            data = {"code": code, "name": closest_row["location"]}
            print(data)
            # Encode the data dictionary into a query string and redirect to the 'view' route
            query_string = urllib.parse.urlencode(data)
            return redirect(f"/films/view?{query_string}", code=307)
        else:
            print("Invalid postcode.")
    else:
        # Render the 'films' template if the request method is 'GET'
        return render_template("films.html")


@app.route("/films/view", methods=["GET", "POST"])
def view():
    if request.method == "POST":
        # Get the cinema code and cinema name from the previous form
        code = request.args.get("code")
        print(code)
        name = request.args.get("name")
        # Get the current date and format it as required
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        print(formatted_date)
        # Construct the URL to fetch data from
        url = f"https://www.cineworld.co.uk/uk/data-api-service/v1/quickbook/10108/film-events/in-cinema/{code}/at-date/{formatted_date}?attr=&lang=en_GB"
        print(url)
        # Set the headers for the request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        film_data = {}
        # Send a GET request to the URL to get film data
        response = requests.get(url, headers=headers)
        print(response.text)
        # Convert the response data to a Python dictionary
        data_dict = response.json()
        # Extract the list of films from the dictionary
        films = data_dict["body"]["films"]
        # Define a set and a list of allowed age rating codes
        allowed_attribute_ids_dict = {"U", "PG", "12", "12a", "15", "18"}
        allowed_attribute_ids_list = ["U", "PG", "12", "12a", "15", "18"]
        parsed_data = []
        # For each film, check if it has an allowed age rating code
        for film in films:
            for attr_id in film["attributeIds"]:
                if attr_id in allowed_attribute_ids_dict:
                    # If it does, extract its name, age rating, booking link, video link, and poster link
                    film_info = {
                        "name": film["name"],
                        "age_rating": attr_id,
                        "booking_link": film["link"],
                        "video_link": film["videoLink"],
                        "poster_link": film["posterLink"],
                    }
                    # Append the film info to the list of parsed data
                    parsed_data.append(film_info)
                    print(parsed_data)
                    break
        # Pass the cinema name and parsed film data to the location.html template
        return render_template("location.html", name=name, data={"films": parsed_data})


if __name__ == "__main__":
    app.run(debug=True)
