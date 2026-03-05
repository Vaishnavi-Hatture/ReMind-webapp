from flask import Flask, render_template, request, redirect
import json
import random

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/waiting")
def waiting_page():
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


@app.route("/swipe")
def swipe():
    with open("data.json") as file:
        data = json.load(file)

    interests = data.get("interests", [])

    content_map = {
        "Fitness": [
            {"category": "Fitness", "title": "Do 5 Pushups", "text": "Drop and do 5 quick pushups. Move your body for just one minute — it resets your energy."},
            {"category": "Fitness", "title": "Stretch Your Back", "text": "Stand up and stretch your arms overhead, then roll your shoulders back. Your body will thank you."},
            {"category": "Fitness", "title": "Walk for 2 Minutes", "text": "Step away from your screen and take a short walk — even just around the room counts."}
        ],
        "Learning": [
            {"category": "Learning", "title": "Read a Short Article", "text": "Spend 2 minutes reading something new — a Wikipedia page, a blog post, or a news headline that interests you."},
            {"category": "Learning", "title": "Learn One New Word", "text": "Look up one word you've never heard before and try to use it in a sentence today."},
            {"category": "Learning", "title": "Watch a 2-Min Explainer", "text": "Search for a quick explainer video on anything you've been curious about. Knowledge in bite-sized form."}
        ],
        "Career": [
            {"category": "Career", "title": "Write One Small Goal", "text": "Open a notes app and write one tiny career goal — even just 'reply to that email'. Small steps compound."},
            {"category": "Career", "title": "Review Your To-Do List", "text": "Spend 2 minutes skimming your tasks. Cross off one thing or add one new intention for the day."},
            {"category": "Career", "title": "Learn One Skill Tip", "text": "Search for one tip related to your field. Even a single insight from an article can shift your perspective."}
        ],
        "Mental Health": [
            {"category": "Mental Health", "title": "Take 3 Deep Breaths", "text": "Breathe in for 4 seconds, hold for 4, out for 4. Repeat 3 times. Slow breathing calms your nervous system."},
            {"category": "Mental Health", "title": "Write What You're Grateful For", "text": "Name three small things that went well today or that you appreciate. Gratitude rewires your brain."},
            {"category": "Mental Health", "title": "Check In With Yourself", "text": "Ask: how am I really feeling right now? Just naming your emotion — tired, anxious, okay — creates a moment of awareness."}
        ],
        "Music": [
            {"category": "Music", "title": "Listen to One Full Song", "text": "Put on a song you love and just listen — no scrolling, no multitasking. Let the music actually reach you."},
            {"category": "Music", "title": "Hum or Sing Something", "text": "Sing or hum along to anything for 60 seconds. It sounds small, but it genuinely lifts your mood."},
            {"category": "Music", "title": "Discover One New Artist", "text": "Search for a new artist in a genre you enjoy. Give one of their songs a real listen with full attention."}
        ],
        "Reading": [
            {"category": "Reading", "title": "Read 2 Pages", "text": "Pick up any book — even one you've paused — and read just 2 pages. Re-entering a story takes less than a minute."},
            {"category": "Reading", "title": "Read a Poem", "text": "Search for a short poem on any topic. Poems are made to be read in minutes and felt for much longer."},
            {"category": "Reading", "title": "Skim a Newsletter or Article", "text": "Find one piece of writing you've saved but never read. Even skimming gives your mind something real to chew on."}
        ]
    }

    suggestions = []
    for interest in interests:
        interest = interest.strip()
        if interest in content_map:
            suggestions.extend(content_map[interest])

    random.shuffle(suggestions)

    return render_template("swap.html", suggestions=suggestions)


@app.route("/decision")
def decision_page():
    return render_template("decision.html")


if __name__ == "__main__":
    app.run(debug=True)