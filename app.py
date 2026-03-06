from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = "remind_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./remind.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -------------------------------
# DATABASE MODEL
# -------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    interests = db.Column(db.String(200))
    time_limit = db.Column(db.Integer)


# -------------------------------
# LOGIN PAGE
# -------------------------------
@app.route("/login", methods=["GET","POST"])
def login():

    # Always clear previous session
    session.clear()

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Account does not exist. Please signup first."

        elif user.password != password:
            error = "Incorrect password."

        else:
            session["user_id"] = user.id
            return redirect("/index")

    return render_template("login.html", error=error)

@app.route("/index")
def index():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("index.html")


# -------------------------------
# SIGNUP PAGE
# -------------------------------

@app.route("/signup", methods=["GET","POST"])
def signup():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # check if user already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            error = "Account already exists. Please login."

        else:
            new_user = User(username=username, password=password)

            db.session.add(new_user)
            db.session.commit()

            return redirect("/login")

    return render_template("signup.html", error=error)


# -------------------------------
# INDEX PAGE
# -------------------------------

@app.route("/")
def home():
    return redirect("/login")


# -------------------------------
# SAVE USER SETTINGS
# -------------------------------

@app.route("/save", methods=["POST"])
def save():

    if "user_id" not in session:
        return redirect("/login")

    interests = request.form.get("interests")
    time_limit = request.form.get("timeLimit")

    user = User.query.get(session["user_id"])

    user.interests = interests
    user.time_limit = int(time_limit)

    db.session.commit()

    return redirect("/waiting")


@app.route("/admin")
def admin():

    users = User.query.all()

    return render_template("admin.html", users=users)

# -------------------------------
# WAITING TIMER PAGE
# -------------------------------

@app.route("/waiting")
def waiting_page():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    time_limit = user.time_limit

    return render_template("waiting.html", time_limit=time_limit)


# -------------------------------
# BREAK PAGE
# -------------------------------

@app.route("/break")
def break_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("break.html")


# -------------------------------
# SWIPE CONTENT PAGE
# -------------------------------

@app.route("/swipe")
def swipe():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if not user.interests:
        return redirect("/")

    interests = user.interests.split(",")

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
    ]
    }

    suggestions = []

    for interest in interests:
        if interest in content_map:
            suggestions.extend(content_map[interest])

    random.shuffle(suggestions)

    return render_template("swap.html", suggestions=suggestions)


# -------------------------------
# DECISION PAGE
# -------------------------------

@app.route("/decision")
def decision_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("decision.html")


# -------------------------------
# LOGOUT
# -------------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------------------------------
# RUN APP
# -------------------------------

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)