from flask import Flask, render_template, request, redirect
import json


from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "remind_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./remind.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    interests = db.Column(db.String(200))
    time_limit = db.Column(db.Integer)






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
    {"category":"Fitness","title":"Do 5 Pushups","text":"Move your body and activate your muscles."},

    {"category":"Fitness","title":"Stretch Your Arms","text":"Stretch your arms and shoulders for 30 seconds."},

    {"category":"Fitness","title":"Neck Relaxation","text":"Slowly rotate your neck to release tension."},

    {"category":"Fitness","title":"Stand and Walk","text":"Take a short walk around your room."},

    {"category":"Fitness","title":"Deep Squats","text":"Do 5 slow squats to activate your legs."},

    {"category":"Fitness","title":"Posture Reset","text":"Straighten your back and relax your shoulders."}
],

   "Learning":[
    {"category":"Learning","title":"Read a short article","text":"Spend 2 minutes learning something."},

    {"category":"Learning","title":"Word: Resilient","text":"Meaning: Able to recover quickly from difficulties."},

    {"category":"Learning","title":"Word: Curiosity","text":"Meaning: A strong desire to learn or know something."},

    {"category":"Learning","title":"Word: Innovation","text":"Meaning: Creating new ideas or improving existing ones."},

    {"category":"Learning","title":"Word: Discipline","text":"Meaning: The ability to control yourself to achieve goals."},

    {"category":"Learning","title":"Word: Insight","text":"Meaning: A deep understanding of a situation or idea."}
],

    "Career":[
    {"category":"Career","title":"Think of One Goal","text":"Write one small career goal for today."},

    {"category":"Career","title":"Skill Reflection","text":"Think about one skill you want to improve."},

    {"category":"Career","title":"Future Planning","text":"Imagine where you want to be in 5 years."},

    {"category":"Career","title":"Quick Learning","text":"Read one paragraph about your field."},

    {"category":"Career","title":"Idea Note","text":"Write down one new idea related to your work."},

    {"category":"Career","title":"Network Thought","text":"Think of one person you can learn from."}
],

    "Mental Health":[
    {"category":"Mental Health","title":"Take 3 Deep Breaths","text":"Slow breathing helps calm your mind."},

    {"category":"Mental Health","title":"Relax Your Eyes","text":"Look away from the screen for 20 seconds."},

    {"category":"Mental Health","title":"Gratitude Moment","text":"Think of one thing you are grateful for."},

    {"category":"Mental Health","title":"Mindful Pause","text":"Close your eyes and focus on your breathing."},

    {"category":"Mental Health","title":"Positive Thought","text":"Think of one positive thing about today."},

    {"category":"Mental Health","title":"Body Awareness","text":"Relax your shoulders and jaw."}
],

    "Music":[
    {"category":"Music","title":"Listen to a Calm Song","text":"Play a relaxing song for a minute."},

    {"category":"Music","title":"Humming Exercise","text":"Hum your favorite tune for relaxation."},

    {"category":"Music","title":"Focus Music","text":"Play instrumental music for better focus."},

    {"category":"Music","title":"Music Memory","text":"Think of a song that motivates you."},

    {"category":"Music","title":"Rhythm Tap","text":"Tap a simple rhythm with your fingers."},

    {"category":"Music","title":"Music Break","text":"Listen to 30 seconds of calming music."}
],

    "Reading":[
    {"category":"Reading","title":"Read One Page","text":"Pick any book and read one page."},

    {"category":"Reading","title":"Quote Reflection","text":"Read an inspiring quote and think about it."},

    {"category":"Reading","title":"Short Story Line","text":"Read one paragraph from a story."},

    {"category":"Reading","title":"Knowledge Snippet","text":"Read one interesting fact."},

    {"category":"Reading","title":"Vocabulary Boost","text":"Learn one new word from a book."},

    {"category":"Reading","title":"Quick Reading","text":"Spend one minute reading something useful."}
],
}

    suggestions = []

    for interest in interests:
        if interest in content_map:
            suggestions.extend(content_map[interest])   

    return render_template("swap.html", suggestions=suggestions)


@app.route("/decision")
def decision_page():
    return render_template("decision.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)