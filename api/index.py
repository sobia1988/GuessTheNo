from flask import Flask, render_template, request
import random

app = Flask(__name__)

rand_bot = random.randint(1, 100)
guess_count = 0

@app.route('/', methods=['GET', 'POST'])
def guess_game():
    global rand_bot, guess_count
    message = ""
    if request.method == 'POST':
        try:
            user_guess = int(request.form['guess'])
            guess_count += 1
            if user_guess > rand_bot:
                message = f"Try a smaller number than {user_guess}."  
            elif user_guess < rand_bot:
                message = f"Try a larger number than {user_guess}."
            else:
                message = f"Correct! You guessed it in {guess_count} attempts."
                with open("guess.txt", "w") as file:
                    file.write(f"Attempts: {guess_count}")
                # Reset game
                rand_bot = random.randint(1, 100)
                guess_count = 0
        except ValueError:
            message = "Please enter a valid number."
    return render_template("index.html", message=message)
