from flask import Flask, render_template, request, send_from_directory, jsonify, url_for, render_template_string
import os
import csv
from prompt import generate_food_exercise, generate_important, generate_routine
from map import get_coordinates, get_hospitals, create_map

app = Flask(__name__)

# -----------------------------------------------
# Serve images
# -----------------------------------------------
@app.route('/image/<path:filename>')
def image(filename):
    return send_from_directory('image', filename)

# -----------------------------------------------
# Load diseases
# -----------------------------------------------
def load_diseases():
    diseases = []
    if os.path.exists("disease.csv"):
        with open("disease.csv", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                diseases.append(row[0].strip())
    return diseases

# -----------------------------------------------
# Save user data
# -----------------------------------------------
def save_user_data(name, age, weight, height, disease_list):
    file_exists = os.path.isfile("user_data.csv")
    with open("user_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Age", "Weight", "Height", "Disease"])
        writer.writerow([name, age, weight, height, ";".join(disease_list)])

# -----------------------------------------------
# Base health form
# -----------------------------------------------
@app.route("/base", methods=["GET", "POST"])
def health_form():
    diseases = load_diseases()
    if request.method == "POST":
        form_data = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "weight": request.form.get("weight"),
            "height": request.form.get("height"),
            "sex": request.form.get("sex"),
            "race": request.form.get("race"),
            "disease": request.form.getlist("disease")
        }
        save_user_data(
            form_data["name"],
            form_data["age"],
            form_data["weight"],
            form_data["height"],
            form_data["disease"]
        )
        return render_template("answer.html", form_data=form_data)
    return render_template("base.html", diseases=diseases)

# -----------------------------------------------
# Basic navigation routes
# -----------------------------------------------
@app.route("/")
def home():
    return render_template("base.html", page="home")

@app.route("/ask")
def ask():
    diseases = load_diseases()
    return render_template("ask.html", page="ask", diseases=diseases)

@app.route("/answer")
def answer():
    return render_template("answer.html", page="answer")

@app.route("/about")
def about():
    return render_template("about.html", page="about")

@app.route("/map")
def map():
    return render_template("map.html", page="map")

@app.route("/view-output")
def view_output():
    with open("user_data.csv", "r") as f:
        content = f.read()
    return render_template_string("<pre>{{content}}</pre>", content=content)

# -----------------------------------------------
# Map search logic
# -----------------------------------------------
@app.route('/search_location', methods=['POST'])
def search_location():
    zip_code = request.form.get('zip')
    country = request.form.get('country')
    lat, lon = get_coordinates(zip_code, country)
    if not lat or not lon:
        return render_template("map.html", page="map", error="❌ Could not locate that postal code.", hospitals=[])
    hospitals = get_hospitals(lat, lon, radius=8000)
    map_path = os.path.join('static', 'hospitals_near_me.html')
    create_map(lat, lon, hospitals, zip_code, country)
    if os.path.exists("hospitals_near_me.html"):
        os.replace("hospitals_near_me.html", map_path)
    return render_template(
        "map.html",
        page="map",
        hospitals=hospitals,
        zip_code=zip_code,
        country=country,
        map_file=url_for('static', filename='hospitals_near_me.html')
    )

# -----------------------------------------------
# Dynamic content routes
# -----------------------------------------------
@app.route("/get_content/<category>", methods=["POST"])
def get_content(category):
    if category == "food":
        return jsonify({"content": generate_food_exercise()})
    elif category == "routine":
        return jsonify({"content": generate_routine()})
    elif category == "important":
        return jsonify({"content": generate_important()})
    else:
        return jsonify({"content": "No content available."})

# -----------------------------------------------
# Run app
# -----------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
