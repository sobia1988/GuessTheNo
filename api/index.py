
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'your_secret_key'  # Required to use sessions

@app.route("/", methods=["GET", "POST"])
def home():
    # Start a new game if there's no number in the session
    if 'rand_bot' not in session:
        session['rand_bot'] = random.randint(1, 100)  # Random number to guess
        session['guess_count'] = 0  # Track the number of attempts
    
    message = ""
    guess_count = session.get('guess_count', 0)
    
    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
            session['guess_count'] += 1  # Increment guess count
            
            # Check if the guess is correct or not
            if guess > session['rand_bot']:
                message = f"Please select a number less than {guess}."
            elif guess < session['rand_bot']:
                message = f"Please select a number greater than {guess}."
            elif guess < 1:
                message = f"Kindly select a valid number."
            elif guess > 100:
                message = f"Kindly select a valid number."
            else:
                message = f"Congratulations! You guessed the correct number in {session['guess_count']} attempts!"
                session.pop('rand_bot', None)  # Reset the game state after a correct guess

        except ValueError:
            message = "Please enter a valid number."
    
    return render_template("index.html", message=message, guess_count=guess_count)
    
if __name__ == "__main__":
    app.run(debug=True)

with open(r"guess.txt", "w") as file:
 file.write(str(f"attemps: {{guess_count}}"))