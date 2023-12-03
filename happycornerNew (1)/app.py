import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required  # Assuming this is a decorator for routes that require login
from cs50 import SQL  # If you're using CS50's SQL module
import random
from flask import jsonify, request


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///happy_corner.db")  # Update the database name accordingly

@app.route("/")
@login_required
def index():
    """ Main page of the website """
    return render_template("index.html")

@app.route("/diy", methods=["GET", "POST"])
@login_required
def diy():
    return render_template("diy.html")


@app.route("/gratitude", methods=["GET", "POST"])
@login_required
def gratitude():
    user_id = session["user_id"]

    if request.method == "POST":
        entry = request.form.get("entry")
        db.execute("INSERT INTO gratitude_entries (user_id, text) VALUES (?, ?)", user_id, entry)
        return redirect("/gratitude")

    entries = db.execute("SELECT text, date FROM gratitude_entries WHERE user_id = ? ORDER BY date DESC", user_id)

    for each_entry in entries:
        each_entry["date"] = each_entry["date"][0:11]
    return render_template("gratitude.html", entries=entries)

@app.route("/kindness", methods=["GET", "POST"])
@login_required
def kindness():
    # Define your questions as before
    question1 = {
        'text': 'What would you like the difficulty level for your act to be?',
        'choices': ['Easy', 'Medium', 'Difficult']
    }
    question2 = {
        'text': 'What is your relationship to the person you would like to help?',
        'choices': ['Stranger', 'Acquaintance', 'Close Friend']
    }
    question3 = {
        'text': 'What is your main goal with this act?',
        'choices': ['Provide Encouragement', 'Show Your Love', 'Improve Relationship']
    }

    if request.method == "POST":
        # Extract responses
        selected_difficulty = request.form.get("difficulty")
        selected_person = request.form.get("person")
        selected_goal = request.form.get("goal")

        # Determine the random act based on the responses
        kindness_name = determine_kindness_name(selected_difficulty, selected_person, selected_goal)
        kindness_desc = determine_kindness_desc(selected_difficulty, selected_person, selected_goal)

        # Display the selected act
        return render_template("kindness_generated.html", kindness_name=kindness_name, kindness_desc=kindness_desc)
    else:
        # Display the form if the method is GET
        return render_template("kindness.html", question1=question1, question2=question2, question3=question3)

def determine_kindness_name(difficulty, person, goal):
    # Expanded categorization of acts based on difficulty, person, and goal

    categorized_name = {
        ('Easy', 'Stranger', 'Provide Encouragement'): [
            "Offer a Genuine Smile"
        ],
        ('Easy', 'Stranger', 'Show Your Love'): [
            "Give Them a Compliment"
        ],
        ('Easy', 'Stranger', 'Improve Relationship'): [
            "Spread Positivity on Social Media"
        ],

        ('Easy', 'Acquaintance', 'Provide Encouragement'): [
            "Share Inspiring Quotes or Stories"
        ],
        ('Easy', 'Acquaintance', 'Show Your Love'): [
            "Share Helpful Resources"
        ],
        ('Easy', 'Acquaintance', 'Improve Relationship'): [
            "Introduce Them to Others"
        ],

        ('Easy', 'Close Friend', 'Provide Encouragement'): [
            "Support Their Goals"
        ],
        ('Easy', 'Close Friend', 'Show Your Love'): [
            "Express Gratitude"
        ],
        ('Easy', 'Close Friend', 'Improve Relationship'): [
            "Practice Active Listening"
        ],

        ('Medium', 'Stranger', 'Provide Encouragement'): [
            "Support Local Businesses"
        ],
        ('Medium', 'Stranger', 'Show Your Love'): [
            "Pay It Forward"
        ],
        ('Medium', 'Stranger', 'Improve Relationship'): [
            "Donate Unused Items/Clothing"
        ],

        ('Medium', 'Acquaintance', 'Provide Encouragement'): [
            "Write a Thank-You Note"
        ],
        ('Medium', 'Acquaintance', 'Show Your Love'): [
            "Offer Pet Care"
        ],
        ('Medium', 'Acquaintance', 'Improve Relationship'): [
            "Offer a Ride"
        ],

        ('Medium', 'Close Friend', 'Provide Encouragement'): [
            "Create a Memory Jar"
        ],
        ('Medium', 'Close Friend', 'Show Your Love'): [
            "Help With Childcare"
        ],
        ('Medium', 'Close Friend', 'Improve Relationship'): [
            "Cook a Meal"
        ],

        ('Difficult', 'Stranger', 'Provide Encouragement'): [
            "Be a Positive Role Model"
        ],
        ('Difficult', 'Stranger', 'Show Your Love'): [
            "Volunteer"
        ],
        ('Difficult', 'Stranger', 'Improve Relationship'): [
            "Contribute to the Environment"
        ],

        ('Difficult', 'Acquaintance', 'Provide Encouragement'): [
            "Surprise Care Package"
        ],
        ('Difficult', 'Acquaintance', 'Show Your Love'): [
            "Offer to Help With Errands"
        ],
        ('Difficult', 'Acquaintance', 'Improve Relationship'): [
            "Organize a Group Volunteer Activity"
        ],

        ('Difficult', 'Close Friend', 'Provide Encouragement'): [
            "Create an Inspiration Board"
        ],
        ('Difficult', 'Close Friend', 'Show Your Love'): [
            "Plan a Surprise Outing"
        ],
        ('Difficult', 'Close Friend', 'Improve Relationship'): [
            "Share your Skills or Knowledge"
        ],
        'default': [
            "Incomplete Answers!"
        ]
    }

    # Find a category that matches the responses or default
    selected_category = categorized_name.get((difficulty, person, goal), categorized_name['default'])

    # Select a random act from the chosen category
    return selected_category[0];

def determine_kindness_desc(difficulty, person, goal):
    # Expanded categorization of acts based on difficulty, person, and goal

    categorized_desc = {
        ('Easy', 'Stranger', 'Provide Encouragement'): [
            "OSmile at strangers you pass by throughout your day. A friendly smile can brighten someone's mood and create a positive connection."
        ],
        ('Easy', 'Stranger', 'Show Your Love'): [
            "Throughout your day, make an effort to give sincere compliments to people you interact with. Acknowledge their strengths, talents, or efforts, and make them feel valued and appreciated"
        ],
        ('Easy', 'Stranger', 'Improve Relationship'): [
            "Use your social media platforms to spread positivity, share inspirational messages, or highlight the achievements of others. Engage in uplifting conversations and promote a supportive online community."
        ],

        ('Easy', 'Acquaintance', 'Provide Encouragement'): [
            "Share uplifting quotes or stories with others that can provide motivation and encouragement. It could be through social media, email, or even a handwritten note."
        ],
        ('Easy', 'Acquaintance', 'Show Your Love'): [
            "If you come across an article, book, or website that you think might be of interest or benefit to them based on their hobbies or interests, share it with them."
        ],
        ('Easy', 'Acquaintance', 'Improve Relationship'): [
            "If you notice that the acquaintance is new to a social gathering or event, take the initiative to introduce them to others and help them feel more comfortable."
        ],

        ('Easy', 'Close Friend', 'Provide Encouragement'): [
            "Encourage your loved one's aspirations and goals. Offer to be their accountability partner, provide constructive feedback, or help them research opportunities or resources to further their ambitions."
        ],
        ('Easy', 'Close Friend', 'Show Your Love'): [
            "Take the time to express your gratitude and appreciation for your friend or family member. Write a heartfelt letter, create a personalized video message, or simply tell them face-to-face how much they mean to you."
        ],
        ('Easy', 'Close Friend', 'Improve Relationship'): [
            "When engaging in conversations with others, practice active listening by giving your full attention and showing genuine interest. Allow others to feel heard and valued."
        ],

        ('Medium', 'Stranger', 'Provide Encouragement'): [
            "Choose to shop at local businesses instead of larger chains whenever possible. Your support helps local economies thrive and shows appreciation for the hard work of small business owners."
        ],
        ('Medium', 'Stranger', 'Show Your Love'): [
            "When you're at a coffee shop or a drive-thru, pay for the order of the person behind you. It can create a chain reaction of kindness."
        ],
        ('Medium', 'Stranger', 'Improve Relationship'): [
            "Declutter your home and donate gently used clothes, books, or household items to a local shelter or charity. Your unwanted items can make a significant difference in someone else's life."
        ],

        ('Medium', 'Acquaintance', 'Provide Encouragement'): [
            "Take a moment to write a heartfelt thank-you note to someone who has made a positive impact on your life. Express your gratitude and let them know how much you appreciate them."
        ],
        ('Medium', 'Acquaintance', 'Show Your Love'): [
            "If you know someone who has a pet and needs assistance, offer to walk their dog, feed their pets, or pet-sit when they are away. It shows care for both the person and their furry companion."
        ],
        ('Medium', 'Acquaintance', 'Improve Relationship'): [
            "If you know someone who needs transportation to an appointment, social event, or any other commitment, offer to give them a ride. It can be a significant help, especially for those without reliable transportation."
        ],

        ('Medium', 'Close Friend', 'Provide Encouragement'): [
            "Fill a jar with handwritten notes that capture favorite memories, inside jokes, or heartfelt messages. Present it as a gift, and your loved one can pick a note from the jar whenever they need a boost of happiness or nostalgia."
        ],
        ('Medium', 'Close Friend', 'Show Your Love'): [
            "If your friend or family member has young children, offer to help with childcare for a day or evening. Give them a break to relax, run errands, or enjoy some quality time on their own."
        ],
        ('Medium', 'Close Friend', 'Improve Relationship'): [
            "Prepare a homemade meal for your friend or family member. Take into account their dietary preferences and any special occasions or milestones they may be celebrating."
        ],

        ('Difficult', 'Stranger', 'Provide Encouragement'): [
            "Lead by example and embody positivity, resilience, and determination. Show others through your actions and attitude that challenges can be overcome and goals can be achieved."
        ],
        ('Difficult', 'Stranger', 'Show Your Love'): [
            "Dedicate your time to a local charity or organization. Offer to help at a homeless shelter, animal shelter, or food bank."
        ],
        ('Difficult', 'Stranger', 'Improve Relationship'): [
            "Contribute to the environment by planting a tree or participating in a community tree-planting initiative. Trees provide numerous benefits to the planet and future generations."
        ],

        ('Difficult', 'Acquaintance', 'Provide Encouragement'): [
            "Put together a thoughtful care package filled with their favorite snacks, self-care items, books, or small gifts. Tailor it to their interests and tastes to show how well you know and appreciate them."
        ],
        ('Difficult', 'Acquaintance', 'Show Your Love'): [
            "If you know someone who is busy or overwhelmed, offer to run errands for them. Whether it's picking up groceries, dropping off dry cleaning, or mailing packages, your assistance can lighten their load."
        ],
        ('Difficult', 'Acquaintance', 'Improve Relationship'): [
            "Rally a group of friends or acquaintances to participate in a volunteer activity together. It could be a community cleanup, working at a food bank, or organizing a fundraiser for a local cause."
        ],

        ('Difficult', 'Close Friend', 'Provide Encouragement'): [
            "Help someone create an inspiration board or vision board that captures their goals, dreams, and aspirations. Encourage them to visualize their success and provide support along the way."
        ],
        ('Difficult', 'Close Friend', 'Show Your Love'): [
            "Organize a surprise outing or activity that your loved one would enjoy. It could be a picnic in the park, a day trip to a nearby town, or tickets to a show they've been wanting to see."
        ],
        ('Difficult', 'Close Friend', 'Improve Relationship'): [
            "Offer to teach someone a skill you possess, whether it's cooking, playing an instrument, or a particular hobby. Sharing your knowledge can be a meaningful act of kindness."
        ],
        'default': [
            "Please go back and fill out all the questions."
        ]
    }

    # Find a category that matches the responses or default
    selected_category = categorized_desc.get((difficulty, person, goal), categorized_desc['default'])

    # Select a random act from the chosen category
    return selected_category[0];


@app.route("/select_difficulty", methods=["GET","POST"])
@login_required
def select_difficulty():
    data = request.get_json()
    selected_difficulty = data['difficulty']
    return jsonify({'selected_difficulty': selected_difficulty})

@app.route("/select_person", methods=["GET","POST"])
@login_required
def select_person():
    data = request.get_json()
    selected_person = data['person']
    return jsonify({'selected_person': selected_person})

@app.route("/select_goal", methods=["GET","POST"])
@login_required
def select_goal():
    data = request.get_json()
    selected_goal = data['goal']
    return jsonify({'selected_goal': selected_goal})

@app.route("/get_random_act", methods=["GET","POST"])
@login_required
def get_random_act():
    data = request.get_json()
    selected_goal = data['goal']
    return jsonify({'selected_goal': selected_goal})

# Other routes for Playlist, Self-Care Checklist, Soothing Game, etc.

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/podcast")
def playlist():
    return render_template('podcast.html')

# Indicating the theme that the user chose
@app.route('/select_theme', methods=['POST'])
def select_theme():
    data = request.get_json()
    selected_theme = data['theme']
    # Can perform server-side logic here with the selected theme
    return jsonify({'selected_theme': selected_theme})

@app.route('/game')
def game():
    return render_template('game.html')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form (or home page)
    return redirect("/login")  # or return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not confirmation:
            return apology("must confirm password", 400)

        # Check if passwords match
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Hash the user's password for security
        hash = generate_password_hash(password)

        # Insert the new user into the database
        try:
            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            if not result:
                return apology("username already exists", 400)
        except Exception as e:
            # Handle any other exceptions
            return apology(f"Error: {e}", 500)

        # Redirect to login page or log the user in directly
        return redirect("/login")
    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")

# Add other necessary routes and functionalities as needed

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False in production