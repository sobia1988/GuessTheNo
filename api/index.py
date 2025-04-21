from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__, template_folder='templates')  # Make sure your templates folder is correct
app.secret_key = 'your_secret_key'

@app.route("/", methods=["GET", "POST"])
def home():
    if 'rand_bot' not in session:
        session['rand_bot'] = random.randint(1, 100)
        session['guess_count'] = 0

    message = ""
    guess_count = session.get('guess_count', 0)

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
            session['guess_count'] += 1

            if guess < 1 or guess > 100:
                message = "Kindly select a valid number between 1 and 100."
            elif guess > session['rand_bot']:
                message = f"Please select a number less than {guess}."
            elif guess < session['rand_bot']:
                message = f"Please select a number greater than {guess}."
            else:
                message = f"🎉 Congratulations! You guessed the correct number in {session['guess_count']} attempts!"
                session.pop('rand_bot', None)

        except ValueError:
            message = "Please enter a valid number."

    return render_template("index.html", message=message, guess_count=guess_count)

if __name__ == "__main__":
    app.run(debug=True)
