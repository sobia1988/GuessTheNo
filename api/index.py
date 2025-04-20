from flask import Flask, request, render_template
import random
import os

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
)

# Initialize the secret number globally
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
                message = "🎉 Congratulations! You guessed it right!"
                secret_number = random.randint(1, 100)  # reset
        except Exception as e:
            message = f"Error: {str(e)}. Please enter a valid number."

    return render_template("index.html", message=message)
