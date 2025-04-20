from flask import Flask, render_template, request, session, jsonify
import random
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a better secret in production

@app.route('/')
def index():
    if 'rand_bot' not in session:
        session['rand_bot'] = random.randint(1, 100)
        session['guess_count'] = 0
    return render_template('index.html', guess_count=session['guess_count'])

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    user_input = int(data['guess'])

    rand_bot = session.get('rand_bot')
    session['guess_count'] += 1
    guess_count = session['guess_count']

    if user_input > rand_bot:
        return jsonify(result=f"Please select a number less than {user_input}.", guess_count=guess_count)
    elif user_input < rand_bot:
        return jsonify(result=f"Please select a number greater than {user_input}.", guess_count=guess_count)
    elif user_input == rand_bot:
        file_path = os.path.join(os.getcwd(), 'guess.txt')
        with open(file_path, 'w') as f:
            f.write(f"Attempts: {guess_count}")
        result = f"You guessed the correct number in {guess_count} attempts!"
        session.clear()
        return jsonify(result=result, game_over=True, guess_count=guess_count)

    return jsonify(result="Invalid guess. Try again.", guess_count=guess_count)

# Required for Vercel to detect this as the entry point
app = app
