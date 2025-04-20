from flask import Flask, render_template, request
import random
import os

app = Flask(__name__, template_folder='../templates')

rand_bot = random.randint(1, 100)
guess_count = 0

@app.route("/", methods=["GET", "POST"])
def home():
    global guess_count, rand_bot
    message = ""
    
    if request.method == "POST":
        try:
            user_guess = int(request.form["guess"])
            guess_count += 1
            if user_guess < rand_bot:
                message = f"Try a higher number than {user_guess}!"
            elif user_guess > rand_bot:
                message = f"Try a lower number than {user_guess}!"
            else:
                message = f"🎉 Correct! You guessed it in {guess_count} attempts!"
                with open("guess.txt", "w") as f:
                    f.write(f"Attempts: {guess_count}")
                rand_bot = random.randint(1, 100)
                guess_count = 0
        except:
            message = "❌ Please enter a valid number!"
    
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
