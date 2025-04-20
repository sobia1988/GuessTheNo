from flask import Flask, render_template, request, session, jsonify
import random
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session

# Route to render the frontend page
@app.route('/')
def index():
    # Initialize random number and attempts in session if not present
    if 'rand_bot' not in session:
        session['rand_bot'] = random.randint(1, 100)
        session['guess_count'] = 0
    guess_count = session['guess_count']
    return render_template('index.html', guess_count=guess_count)

# Route to handle the user's guess
@app.route('/guess', methods=['POST'])
def guess():
    try:
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
            # Write attempts to a file
            file_path = os.path.join(os.getcwd(), 'guess.txt')
            with open(file_path, 'w') as f:
                f.write(f"Attempts: {guess_count}")

            result = f"You guessed the correct number in {guess_count} attempts!"
            session.clear()  # Reset the game
            return jsonify(result=result, game_over=True, guess_count=guess_count)
        else:
            return jsonify(result="Invalid guess. Try again.", guess_count=guess_count)
    except Exception as e:
        return jsonify(result=str(e), error=True)

if __name__ == '__main__':
    app.run(debug=True)
