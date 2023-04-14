import requests
import json
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

allowed_attribute_ids_dict = {"u", "pg", "12", "12a", "15", "18"}
allowed_attribute_ids_list = ["u", "pg", "12", "12a", "15", "18"]
url = "https://www.cineworld.co.uk/uk/data-api-service/v1/quickbook/10108/film-events/in-cinema/019/at-date/2023-04-14?attr=&lang=en_GB"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
json_dict = response.json()
films = json_dict["body"]["films"]


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


for film in films:
    for attr_id in film["attributeIds"]:
        if attr_id in allowed_attribute_ids_dict:
            print(film["name"], attr_id)
            break


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


if __name__ == "__main__":
    app.run(debug=True)
