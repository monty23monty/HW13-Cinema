import requests
import json
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
from geopy import distance
from geopy.geocoders import Nominatim
import urllib
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Bootstrap(app)


allowed_attribute_ids_dict = {"u", "pg", "12", "12a", "15", "18"}
allowed_attribute_ids_list = ["u", "pg", "12", "12a", "15", "18"]
url = "https://www.cineworld.co.uk/uk/data-api-service/v1/quickbook/10108/film-events/in-cinema/019/at-date/2023-04-14?attr=&lang=en_GB"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
json_dict = response.json()
films = json_dict["body"]["films"]
df = pd.read_csv("D:\code for IT\Cinema\postcodes_updated.csv")


while True:
    # age = input("What is your age? Please enter a whole number: ")
    age = 18
    try:
        age = int(age)
        if age < 1 or age > 150:
            print("Please enter a sensible number.")
            continue
        else:
            break
    except:
        print("Please use numeric digits or a whole number.")
        continue

if age <= 4:
    print("You can see U certificate films.")
    allowed_films = allowed_attribute_ids_list[0]

elif age <= 8:
    print("You can see PG and U certificate films.")
    allowed_films = allowed_attribute_ids_list[:2]

elif age <= 12:
    print("You can see PG, U and 12 certificate films.")
    allowed_films = allowed_attribute_ids_list[:3]

elif age >= 18:
    print("You can see films of any certificate.")
    allowed_films = allowed_attribute_ids_list

else:
    print("You cannot see any films.")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/age", methods=["GET", "POST"])
def age():
    if request.method == "POST":
        age = request.form["age"]
        try:
            age = int(age)
            if age < 1 or age > 150:
                print("Please enter a sensible number.")
                flash("Please enter a sensible number.")
                return redirect(url_for("home"))
        except:
            print("Please use numeric digits or a whole number.")
            flash("Please use numeric digits or a whole number.")
            return redirect(url_for("home"))

        if age <= 4:
            print("You can see U certificate films.")
            return render_template("age_u.html", age=age)

        elif age <= 8:
            print("You can see PG and U certificate films.")
            return render_template("age_pg.html", age=age)

        elif age <= 12:
            print("You can see PG, U and 12 certificate films.")
            return render_template("age_12.html", age=age)

        elif age >= 18:
            print("You can see films of any certificate.")
            return render_template("age_18.html", age=age)

        else:
            print("You cannot see any films.")
            return render_template("age.html")

    else:
        return redirect(url_for("home"))


@app.route("/films", methods=["GET", "POST"])
def films():
    if request.method == "POST":
        df = pd.read_csv("D:\code for IT\Cinema\cinemas_with_coords.csv")
        print(df.head())
        user_postcode = request.form["postcode"]
        geolocator = Nominatim(user_agent="cinema_locator")

        def get_coords(address):
            location = geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            else:
                return None

        df = df.dropna(subset=["coords"])

        def get_distance(coords1, coords2):
            return distance.distance(coords1, coords2).km

        user_location = geolocator.geocode(user_postcode)
        if user_location:
            user_coords = (user_location.latitude, user_location.longitude)
        else:
            print("Invalid postcode.")
            exit()

        coords_df = df["coords"].str.split(",", expand=True)
        coords_df.columns = ["lat", "lon"]

        # Join the 'coords' DataFrame back to the original DataFrame
        df = pd.concat([df, coords_df], axis=1)

        # Print the updated DataFrame
        print(df)
        df["lat"] = df["lat"].astype(float)
        df["lon"] = df["lon"].astype(float)
        if user_coords:
            df["distance"] = df.apply(
                lambda row: get_distance((row["lat"], row["lon"]), user_coords), axis=1
            )
            closest_row = df.sort_values(by="distance").iloc[0]
            print(closest_row["location"])
            print(closest_row["address"])
            print(closest_row["url"])
            print(closest_row["code"])
            code = closest_row["code"]
            code = f"{code:03d}"
            print(code)
            data = {"code": code, "name": closest_row["location"]}
            print(data)
            query_string = urllib.parse.urlencode(data)
            return redirect(f"/films/view?{query_string}", code=307)
        else:
            print("Invalid postcode.")
    else:
        return render_template("films.html")


@app.route("/films/view", methods=["GET", "POST"])
def view():
    if request.method == "POST":
        code = request.args.get("code")
        print(code)
        name = request.args.get("name")
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        formatted_date = "2023-04-15"
        print(formatted_date)
        url = f"https://www.cineworld.co.uk/uk/data-api-service/v1/quickbook/10108/film-events/in-cinema/{code}/at-date/{formatted_date}?attr=&lang=en_GB"
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        film_data = {}
        response = requests.get(url, headers=headers)
        print(response.text)
        data_dict = response.json()
        films = data_dict["body"]["films"]
        allowed_attribute_ids_dict = {"U", "PG", "12", "12a", "15", "18"}
        allowed_attribute_ids_list = ["U", "PG", "12", "12a", "15", "18"]
        parsed_data = []
        for film in films:
            for attr_id in film["attributeIds"]:
                if attr_id in allowed_attribute_ids_dict:
                    film_info = {
                        "name": film["name"],
                        "age_rating": attr_id,
                        "booking_link": film["link"],
                        "video_link": film["videoLink"],
                        "poster_link": film["posterLink"],
                    }
                    parsed_data.append(film_info)
                    print(parsed_data)
                    break
        return render_template("location.html", name=name, data={"films": parsed_data})


if __name__ == "__main__":
    app.run(debug=True)
