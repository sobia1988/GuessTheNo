from flask import Flask, render_template, request, session
import random
import os

# Set the template folder path to one level up from this file
template_path = os.path.join(os.path.dirname(__file__), '../templates')

app = Flask(__name__, template_folder=template_path)
app.secret_key = 'your-secret-key'

@app.route('/')
def index():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    try:
        user_guess = int(request.form['guess'])
        number = session.get('number', random.randint(1, 100))
        if user_guess < number:
            message = "Too low! Try again."
        elif user_guess > number:
            message = "Too high! Try again."
        else:
            message = "Congratulations! You guessed it right."
            session.pop('number', None)  # Reset game
        return render_template('index.html', message=message)
    except Exception as e:
        return render_template('index.html', message="Invalid input. Please enter a number.")

# For debugging the template path (optional)
@app.route('/debug')
def debug():
    return f"Template path: {app.template_folder}"
