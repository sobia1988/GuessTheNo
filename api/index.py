from flask import Flask, render_template, request
import random

app = Flask(__name__, template_folder="../templates")

secret_number = random.randint(1, 100)

@app.route("/", methods=["GET", "POST"])
def index():
    global secret_number
    message = ""
    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
            if guess < secret_number:
                message = "Too low! Try again."
            elif guess > secret_number:
                message = "Too high! Try again."
            else:
                message = "Congratulations! You guessed it right!"
                secret_number = random.randint(1, 100)  # Reset
        except:
            message = "Please enter a valid number."
    return render_template("index.html", message=message)
