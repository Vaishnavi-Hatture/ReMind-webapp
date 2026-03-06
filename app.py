from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/waiting")
def waiting_page():
    import json

    with open("data.json", "r") as file:
        data = json.load(file)

    time_limit = data.get("time_limit", "1")

    return render_template("waiting.html", time_limit=time_limit)

@app.route("/save", methods=["POST"])
def save():
    time_limit = request.form.get("timeLimit")
    interests = request.form.get("interests")

    data = {
        "time_limit": time_limit,
        "interests": interests.split(",") if interests else []
    }

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    return redirect("/waiting")



@app.route("/break")
def break_page():
    return render_template("break.html")

import json
import random
from flask import render_template

@app.route("/swipe")
def swipe():

    import json

    with open("data.json") as file:
        data = json.load(file)

    interests = data.get("interests", [])

    content_map = {
        "Fitness":[
            {"category":"Fitness","title":"Do 5 pushups","text":"Move your body for 1 minute."},
            {"category":"Fitness","title":"Stretch","text":"Stretch your arms and back."}
        ],

        "Learning":[
            {"category":"Learning","title":"Read a short article ","text":"Spend 2 minutes learning something."},
            {"category":"Learning","title":"Learn a new word","text":"Find one new English word."}
        ],

        "Career":[
            {"category":"Career","title":"Think of one goal","text":"Write one small career goal."}
        ],

        "Mental Health":[
            {"category":"Focus","title":"Take 3 deep breaths","text":"Slow breathing helps calm your mind."}
        ]
    }

    suggestions = []

    for interest in interests:
        if interest in content_map:
            suggestions.extend(content_map[interest])   # important

    return render_template("swap.html", suggestions=suggestions)


@app.route("/decision")
def decision_page():
    return render_template("decision.html")


if __name__ == "__main__":
    app.run(debug=True)